# -*- coding: utf-8 -*-
r"""_task_jo_ms_notecolor §D 관문 — 데이터 · 칠하기(81 노트) · 고치기 · 켜고 끄기 · 2차 카드 임베드 상자 · 다른 법 무변.

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = --base <파일>(없으면 genie HEAD jo/index.html — omrpop 인도 판)
  헛잣대 = BASE 에 같은 책상 시나리오를 먼저 돌린다 — 새 기능 잣대는 거기서 FAIL 이어야 잣대
  데이터 = genie jo/data + note_color.json(⚙ note_color.py 를 이 하네스가 두 번 돌려 만든 것 · 같은 바이트) — /data/omr/민소/note_color.json 을 그 파일로 준다
  엔진 = chromium 책상 1440×900(마우스) · 폰 390×844(톡) · webkit 책상
  잣대 = DOM 실물(span.nc · 색 · 규칙) · 계산 스타일 · elementFromPoint · 저장소 값(localStorage jopangi.notecolor · jopangi_ui.note_color)

쓰기 : python _harness_jo_ms_notecolor.py [--new 파일] [--base 파일] [--out 폴더] [--only base,desk,other,phone,sync,wk]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · regress = NEW 만(바탕 안 풀고 안 띄움 · ⚙ note_color.py 안 굽고 산출 파일 읽기 · 81 노트는 표본 40 · 세 기기 동기화는 canvas_jari E-6 ⑤ 로 합침) · smoke = 기본 점검 칸만(chromium) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안
_NR = _roots.need_n('⚙ note_color.py · 민소 교재 PDF')   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) 「N: 필요 — 클라우드 불가(…)」 종료 코드 3
import hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
CJH = os.path.dirname(os.path.abspath(__file__))   # env_lanes_fix(9/29) — 같은 폴더(N: · genie _qa 같은 모양 · 옛: N: 고정 자리)
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED(교재·기록 fetch 돌림) · VENDOR · route_filter
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
DATA = os.path.join(JOD, 'data')
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
BASEF = ARG('--base', '')
NCPY = ARG('--nc', os.path.join(_NR, 'jopangi', 'note_color.py'))
WORK = os.path.join(tempfile.gettempdir(), 'h_notecolor')
MB = _roots.mbpdf()
PDFD = os.path.join(_NR, 'jopangi', '민소', '_pdf')
TESTS = io.open(os.path.join(HERE, '_harness_jo_ms_notecolor_tests.js'), encoding='utf-8').read()
PHONE_UA = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
READY = "!!window.__HN&&!!window.__HJ&&typeof render==='function'&&typeof popNote==='function'"
N131 = '1.3.1.{법정}직사토(보독관)'
PROTO = {'dict': 33, 'notes': 53, 'words': 632}                        # 시안(06fd454) 값
CHAT = {'ox': 870, 'loc': 802, 'hb': 236, 'pe': 67, 'dict': 61}       # 채팅 시안 칠한 수(81 노트)
RED, BLUE, PINK = 'rgb(212, 0, 0)', 'rgb(0, 0, 255)', 'rgb(255, 0, 163)'
NAVY, ORANGE = 'rgb(0, 84, 163)', 'rgb(255, 97, 0)'
SERVERS = {}
RES = []
NCJSON = (os.path.join(WORK, 'note_color.json') if QJ.GATE else os.path.join(DATA, 'omr', '민소', 'note_color.json'))


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:300]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s · %s | %s' % (grp, name, d[:300]), flush=True)


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    out = os.path.join(WORK, 'srv_' + tag); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body'); bb = src.index('>', b) + 1
    html = src[:bb] + CJ.SEED + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + CJ.TESTS + '\n</script>\n<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/__book/words/'):
                return os.path.join(MB, 'words', p[len('/__book/words/'):].replace('/', os.sep))
            if p.startswith('/__book/stamp/'):
                return os.path.join(MB, 'stamp', p[len('/__book/stamp/'):].replace('/', os.sep))
            if p.startswith('/__book/pdf/'):
                return os.path.join(PDFD, p[len('/__book/pdf/'):])
            if p.endswith('/omr/민소/note_color.json'):
                return NCJSON
            if p.startswith('/data/'):
                return os.path.join(DATA, p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    def __init__(self, br, eng, tag, src, W, H, phone=False, q='tok=1', who='꼬까'):
        self.eng, self.tag, self.phone, self.who = eng, tag, phone, who
        QJ.launch('base' if tag == 'BASE' else 'new')   # 셈(§B-4) — 바탕(BASE) 판을 띄운 수 · NEW 를 띄운 수
        self.port = serve(tag, src)
        if phone:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=PHONE_UA)
        else:
            self.ctx = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', CJ.route_filter)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.load(q)

    def load(self, q):
        self.pg.goto('http://127.0.0.1:%d/index.html?%s&who=%s' % (self.port, q, urllib.parse.quote(self.who)), wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(900)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def until(self, expr, arg=None, ms=20000):
        t0 = time.time()
        while time.time() - t0 < ms / 1000:
            v = self.ev(expr, arg)
            if v:
                return v
            self.pg.wait_for_timeout(80)
        return self.ev(expr, arg)

    def click(self, at, wait=400):
        if not at or not at.get('on'):
            return False
        if self.phone:
            self.pg.touchscreen.tap(at['cx'], at['cy'])
        else:
            self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def shot(self, name):
        if QJ.REGRESS:   # regress — 눈으로 볼 스크린샷은 안 찍는다(판정 칸 아님 · 찍고 0.5초씩 되읽기)
            return 'regress — 안 찍음'
        d = os.path.join(OUT, '_notecolor_shots'); os.makedirs(d, exist_ok=True)
        f = os.path.join(d, name + '.png')
        try:
            tmp = os.path.join(WORK, name + '.png')
            self.pg.screenshot(path=tmp)
            b = open(tmp, 'rb').read()
            for _ in range(3):
                open(f, 'wb').write(b); time.sleep(0.5)
                if open(f, 'rb').read() == b:
                    break
            return f
        except Exception as e:
            return 'shot 실패 ' + repr(e)[:120]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def find_row(lines, needle, k=0):
    hit = [l for l in lines if needle in l['t']]
    return hit[k] if len(hit) > k else None


def span_at(line, w, k=0):
    """그 줄 보이는 글자에서 w 의 k 번째 자리를 덮는 칠"""
    if not line:
        return None
    i = -1
    for _ in range(k + 1):
        i = line['t'].find(w, i + 1)
        if i < 0:
            return None
    return next((x for x in line['sp'] if x['s'] <= i < x['e']), None)


# ══════════ 데이터 ══════════
def scen_data():
    g = '데이터'
    os.makedirs(WORK, exist_ok=True)
    if QJ.GATE:
        outs = []
        for i in (1, 2):
            o = os.path.join(WORK, 'nc_%d.json' % i)
            r = subprocess.run([sys.executable, NCPY, '--data', DATA, '--out', o], capture_output=True)
            outs.append(o)
            print('  note_color.py', i, r.returncode, r.stdout.decode('utf-8', 'replace').strip()[:200])
        b1, b2 = open(outs[0], 'rb').read(), open(outs[1], 'rb').read()
        shutil.copy(outs[0], NCJSON)
    else:
        b1 = open(NCJSON, 'rb').read()   # regress — note_color.py 두 번 굽기 · 같은 바이트 대조(D2)는 gate 만 → genie 에 올라간 산출 파일(앱이 받는 그 파일)을 읽는다
    d = json.loads(b1)
    st = {'dict': len(d['dict']), 'notes': len(d['loc']), 'words': sum(len(x[2]) for v in d['loc'].values() for x in v)}
    T(g, 'D1 note_color.json 사전 · loc 노트 · 낱말 수 = 시안 값(33 · 53 · 632)', st == PROTO, {'새로': st, '시안': PROTO, 'hash': d.get('hash')})
    if QJ.GATE:
        T(g, 'D2 같은 입력 두 번 = 같은 바이트', b1 == b2, [hashlib.md5(b1).hexdigest()[:12], hashlib.md5(b2).hexdigest()[:12], len(b1)])
    T(g, 'D3 노트 글자는 싣지 않는다(낱말·행 번호만 — 꼴 {v, hash, dict, loc})', set(d) == {'v', 'hash', 'dict', 'loc'}
      and all(len(x) == 3 and isinstance(x[0], int) and isinstance(x[1], int) for v in d['loc'].values() for x in v), sorted(d))
    return d


JS_P6_ONE = """f=>{const out={q:0,pan:0,jo:0,ex:[]};const L=__HN.lines(f)||[];
          L.forEach(l=>{const R=[];const add=(rx,k)=>{let m;rx.lastIndex=0;while((m=rx.exec(l.t)))R.push([m.index,m.index+m[0].length,k]);};
            add(/"[^"]{1,40}"/g,'q');add(/“[^”]{1,40}”/g,'q');add(/<판례>/g,'pan');add(/\\(\\d+조[^)]{0,6}\\)/g,'jo');
            l.sp.forEach(x=>{if(x.r==='loc'||x.r==='dict')return;const h=R.find(r=>x.s>=r[0]&&x.e<=r[1]);if(h){out[h[2]]++;if(out.ex.length<4)out.ex.push(f.slice(0,10)+'|'+l.ri+'|'+x.w+'|'+x.r);}});});return out;}"""   # regress — P6(따옴표 · <판례> · (N조) 를 규칙으로 칠한 수)의 줄 검사 JS(원본과 같은 본문 · 노트 열기 · 노트 for 만 뺐다)


# ══════════ 책상 ══════════
def scen_desk(br, eng, src, tag, CEN):
    g = '%s %s 책상' % (tag, eng)
    p = Pg(br, eng, tag, src, 1440, 900)
    try:
        p.ev("()=>__HN.boot()")
        names = p.ev("async()=>await __HN.noteNames()")
        # ── 칠하기 census(81 노트) ──
        tot = {}
        lines131 = None
        if QJ.REGRESS:   # regress — 표본: 81 노트 가운데 40(씨앗 고정 · 1.3.1 은 늘 든다 — P1~P5 · P7 이 이 노트 줄을 쓴다) · P6 칸의 줄 검사를 같은 노트 열기에 얹는다(81 노트를 또 열지 않는다)
            pick = QJ.sample(names, 40, 'notecolor:P0')
            if N131 not in pick:
                pick = pick + [N131]
            if QJ.SMOKE:   # smoke — 1.3.1 하나만(P1 · P7 칸이 이 줄을 쓴다)
                pick = [N131]
            bad6 = {'q': 0, 'pan': 0, 'jo': 0, 'ex': []}
        for f in (names if QJ.GATE else pick):
            p.ev("async f=>await __HN.note(f)", f)
            c = p.ev("f=>__HN.census(f)", f) or {'c': {}}
            for k, v in c['c'].items():
                tot[k] = tot.get(k, 0) + v
            if f == N131:
                lines131 = p.ev("f=>__HN.lines(f)", f)
            if QJ.REGRESS and not QJ.SMOKE:   # regress — P6 줄 검사(같은 JS · 이미 열린 노트)
                _o = p.ev(JS_P6_ONE, f) or {}
                for _k in ('q', 'pan', 'jo'):
                    bad6[_k] += _o.get(_k, 0)
                for _x in (_o.get('ex') or []):
                    if len(bad6['ex']) < 4:
                        bad6['ex'].append(_x)
        CEN[tag + eng] = tot
        if QJ.GATE:
            T(g, 'P0 81 노트를 모두 열어 칠했다(규칙별 수는 표 · 채팅 값과 나란히)', len(names) == 81 and sum(tot.values()) > 0,
              {'새로': tot, '채팅': CHAT, 'notes': len(names)})
        else:
            if QJ.want('P0'):   # smoke — 81 노트 census 는 안 잰다
                T(g, 'P0 81 노트를 모두 열어 칠했다(규칙별 수는 표 · 채팅 값과 나란히)', len(names) == 81 and sum(tot.values()) > 0,
                  {'새로': tot, '채팅': CHAT, 'notes': len(names), '(표본 %d/%d)' % (len(pick), len(names)): '씨앗 고정 · 1.3.1 포함'})
        L = lines131 or []
        r7 = find_row(L, 'X<-관할-{사}')
        sx = span_at(r7, 'X')
        T(g, 'P1 1.3.1 「X<-관할-{사}…」 X 빨강', bool(sx) and sx['r'] == 'ox' and sx['color'] == RED, {'t': r7 and r7['t'][:30], 'sp': sx})
        r5, r6 = find_row(L, '원칙)'), find_row(L, '예외)')
        s5, s6 = span_at(r5, '원칙)'), span_at(r6, '예외)')
        if QJ.want('P2'):
            T(g, 'P2 「원칙)」 빨강 · 「예외)」 파랑', bool(s5) and bool(s6) and s5['color'] == RED and s6['color'] == BLUE and s5['r'] == 'pe' and s6['r'] == 'pe'
              and s5['w'] == '원칙)' and s6['w'] == '예외)', {'원칙': s5, '예외': s6})
        r14 = find_row(L, 'Ⅲ.{토}')
        s14 = span_at(r14, '토')
        if QJ.want('P3'):
            T(g, 'P3 「Ⅲ.{토}」 토 빨강(괄호 안 글만)', bool(s14) and s14['color'] == RED and s14['r'] == 'hb' and s14['w'] == '토', {'t': r14 and r14['t'][:20], 'sp': s14})
        r20 = find_row(L, '(2) {8조}')
        s20 = span_at(r20, '8조')
        if QJ.want('P4'):
            T(g, 'P4 「(2) {8조}」 는 안 칠함({N조} 뺌)', bool(r20) and s20 is None, {'t': r20 and r20['t'][:20], 'sp': s20})
        r51 = find_row(L, '③ 관할권')
        s51 = span_at(r51, '전속관할')
        if QJ.want('P5'):
            T(g, 'P5 「③ 관할권 … 전속관할」 빨강', bool(s51) and s51['color'] == RED, {'t': r51 and r51['t'][:30], 'sp': s51})
        # 따옴표 · <판례> · (N조) 안 칠 수(규칙 아님 — 81 노트 전체)
        bad = bad6 if QJ.REGRESS else p.ev("""async names=>{const out={q:0,pan:0,jo:0,ex:[]};for(const f of names){await __HN.note(f);const L=__HN.lines(f)||[];
          L.forEach(l=>{const R=[];const add=(rx,k)=>{let m;rx.lastIndex=0;while((m=rx.exec(l.t)))R.push([m.index,m.index+m[0].length,k]);};
            add(/"[^"]{1,40}"/g,'q');add(/“[^”]{1,40}”/g,'q');add(/<판례>/g,'pan');add(/\\(\\d+조[^)]{0,6}\\)/g,'jo');
            l.sp.forEach(x=>{if(x.r==='loc'||x.r==='dict')return;const h=R.find(r=>x.s>=r[0]&&x.e<=r[1]);if(h){out[h[2]]++;if(out.ex.length<4)out.ex.push(f.slice(0,10)+'|'+l.ri+'|'+x.w+'|'+x.r);}});});}return out;}""", names)
        if QJ.want('P6'):
            T(g, 'P6 따옴표 · <판례> · (N조) 를 규칙(O·X·Δ · 원칙)예외) · 두문자)으로 칠한 수 0', bool(bad) and bad['q'] == 0 and bad['pan'] == 0 and bad['jo'] == 0, bad)
        h = p.ev("f=>__HN.head(f)", N131) if p.ev("async f=>await __HN.note(f)", N131) else None
        T(g, 'P7 노트 팝업 머리 「정리 색」(켬 주황 굵게 · 11px · 아이콘 없음) · 「✎ 색 N」 은 0 이면 없음', bool(h) and not h.get('none') and h['on'] and h['onColor'] == 'rgb(180, 83, 9)'
          and int(h['onW']) >= 600 and h['fs'] == '11px' and h['icons'] == 0 and h['me'] == '' and h['t'] == '정리 색', h)
        if QJ.SMOKE:   # smoke — P1 · P7 · Z(책상) 만(P0 census · P2~P6 · 고치기 · 켜고 끄기 · 임베드 상자는 안 잰다)
            er = [x for x in p.errs + (p.ev("()=>__HN.errs()") or []) if not CJ.NOISE(x)]
            T(g, 'Z 페이지 오류 0(잡음 빼고)', not er, er[:6])
            return
        # ── 고치기 ──
        at = p.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r7['ri'] if r7 else 7, 'X'])
        p.click(at, 350)
        pk = p.ev("()=>__HN.pick()")
        T(g, 'F1 칠한 X 누름 → 작은 창(머리 「자동」 · 색 동그라미 여덟 · 지금 색 테두리 · 규칙 설명 글 없음)', bool(pk) and pk['t'] == '자동' and len(pk['sw']) == 8
          and [x['c'] for x in pk['sw'] if x['cur']] == ['red'] and not pk['rv'] and '%' not in pk['text'], pk)
        p.click(p.ev("c=>__HN.pickAt(c)", 'navy'), 400)
        V = p.ev("()=>__HN.ls()") or {}
        k7 = '%s|%d' % (N131, r7['ri'] if r7 else 7)
        L2 = p.ev("f=>__HN.lines(f)", N131) or []
        sx2 = span_at(find_row(L2, 'X<-관할-{사}'), 'X')
        h2 = p.ev("f=>__HN.head(f)", N131)
        T(g, 'F2 남색 → jopangi.notecolor 칸 1 = [[s,e,"navy","X"]] · 점선 밑줄 · 「✎ 색 1」', list(V) == [k7] and len(V[k7]) == 1 and V[k7][0][2:] == ['navy', 'X']
          and bool(sx2) and sx2['r'] == 'me' and sx2['color'] == NAVY and 'dotted' in sx2['deco'] and h2 and h2['me'] == '✎ 색 1', {'v': V, 'sp': sx2, 'head': h2 and h2['me']})
        T(g, 'F3 동기화 — SYNC_KEYS 에 jopangi.notecolor · 이름 · 도장 u', 'jopangi.notecolor' in (p.ev("()=>__HN.syncKeys()") or []) and bool(p.ev("()=>__HN.recName()"))
          and ('jopangi.notecolor|' + k7) in (p.ev("()=>__HN.u()") or []), {'n': len(p.ev("()=>__HN.syncKeys()") or []), 'u': p.ev("()=>__HN.u()")})
        p.load('tok=1&keep=1'); p.ev("()=>__HN.boot()"); p.ev("async f=>await __HN.note(f)", N131)
        L3 = p.ev("f=>__HN.lines(f)", N131) or []
        sx3 = span_at(find_row(L3, 'X<-관할-{사}'), 'X')
        T(g, 'F4 새로고침 뒤 같음', bool(sx3) and sx3['r'] == 'me' and sx3['color'] == NAVY, sx3)
        at = p.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r7['ri'] if r7 else 7, 'X'])
        p.click(at, 350)
        pk = p.ev("()=>__HN.pick()")
        T(g, 'F5 내 고침 누름 → 머리 「✎ 내가 고친 색」 · 「자동으로 되돌리기」', bool(pk) and pk['t'] == '✎ 내가 고친 색' and pk['rv'], pk)
        p.click(p.ev("()=>__HN.pickAt('rv')"), 400)
        V = p.ev("()=>__HN.ls()") or {}
        L4 = p.ev("f=>__HN.lines(f)", N131) or []
        sx4 = span_at(find_row(L4, 'X<-관할-{사}'), 'X')
        T(g, 'F6 되돌리기 → 칸 지움(묘비) · 자동 빨강', k7 not in V and bool(sx4) and sx4['r'] == 'ox' and sx4['color'] == RED and ('jopangi.notecolor|' + k7) in (p.ev("()=>__HN.gone()") or []),
          {'v': V, 'sp': sx4, 'gone': p.ev("()=>__HN.gone()")})
        # 끌어 고르기 → 주황
        r13 = find_row(L4, '심판편의이송')
        a = p.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r13['ri'] if r13 else 13, '심판편의이송'])
        if a:
            p.pg.mouse.move(a['x'] + 1, a['cy']); p.pg.mouse.down(); p.pg.mouse.move(a['x'] + a['w'] * 0.5, a['cy'], steps=4); p.pg.mouse.move(a['r'] - 1, a['cy'], steps=4); p.pg.mouse.up()
            p.pg.wait_for_timeout(400)
        pk = p.ev("()=>__HN.pick()")
        T(g, 'F7 글자 끌어 고르기 → 창 머리 「고른 글자에 색」', bool(pk) and pk['t'] == '고른 글자에 색', pk)
        p.click(p.ev("c=>__HN.pickAt(c)", 'orange'), 400)
        V = p.ev("()=>__HN.ls()") or {}
        k13 = '%s|%d' % (N131, r13['ri'] if r13 else 13)
        L5 = p.ev("f=>__HN.lines(f)", N131) or []
        s13 = span_at(find_row(L5, '심판편의이송'), '심판편의이송')
        T(g, 'F8 주황 → 칸 1 · 그 글자 주황 점선', list(V) == [k13] and len(V[k13]) == 1 and V[k13][0][2] == 'orange' and '심판편의이송' in V[k13][0][3]
          and bool(s13) and s13['color'] == ORANGE and s13['r'] == 'me', {'v': V, 'sp': s13})
        # 검정 → 자동 색 빠짐
        r5b = find_row(L5, '원칙)')
        p.click(p.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r5b['ri'] if r5b else 5, '원칙)']), 350)
        p.click(p.ev("c=>__HN.pickAt(c)", ''), 400)
        L6 = p.ev("f=>__HN.lines(f)", N131) or []
        s5k = span_at(find_row(L6, '원칙)'), '원칙)')
        T(g, 'F9 검정 → 자동 색 빠짐(내 고침 · 색 없음 · 점선)', bool(s5k) and s5k['r'] == 'me' and s5k['c'] == '' and s5k['color'] != RED and 'dotted' in s5k['deco'], s5k)
        # 볼트 줄 앞에 글자가 붙은 픽스처 → 같은 낱말 자리로 옮겨 그림
        V = p.ev("()=>__HN.ls()") or {}
        kk = '%s|%d' % (N131, r5b['ri'] if r5b else 5)
        ent = V.get(kk, [[0, 0, '', '']])[0]
        V[kk] = [[ent[0] + 3, ent[1] + 3, 'purple', ent[3]]]   # 오프셋이 3 밀린 옛 값(볼트 줄 앞에 3글자가 붙은 것과 같다)
        p.ev("v=>__HN.lsSet(v)", V)
        p.ev("async f=>await __HN.note(f)", N131)
        L7 = p.ev("f=>__HN.lines(f)", N131) or []
        s5m = span_at(find_row(L7, '원칙)'), '원칙)')
        T(g, 'F10 오프셋이 밀린 값 → 가장 가까운 같은 낱말 자리로 옮겨 그림(칸은 그대로)', bool(s5m) and s5m['r'] == 'me' and s5m['w'] == '원칙)' and s5m['color'] == 'rgb(156, 0, 255)'
          and (p.ev("()=>__HN.ls()") or {}).get(kk) == V[kk], {'sp': s5m, 'v': (p.ev("()=>__HN.ls()") or {}).get(kk)})
        # 켜고 끄기
        p.click(p.ev("f=>__HN.headAt(f,'on')", N131), 400)
        L8 = p.ev("f=>__HN.lines(f)", N131) or []
        auto = sum(1 for l in L8 for x in l['sp'] if x['r'] != 'me'); me = sum(1 for l in L8 for x in l['sp'] if x['r'] == 'me')
        h8 = p.ev("f=>__HN.head(f)", N131)
        T(g, 'T1 「정리 색」 끔 → 자동 칠 0 · 내 고침은 남음 · 글자 회색', auto == 0 and me >= 2 and h8 and not h8['on'] and h8['onColor'] == 'rgb(154, 149, 139)', {'auto': auto, 'me': me, 'head': h8})
        p.load('tok=1&keep=1'); p.ev("()=>__HN.boot()"); p.ev("async f=>await __HN.note(f)", N131)
        L9 = p.ev("f=>__HN.lines(f)", N131) or []
        auto9 = sum(1 for l in L9 for x in l['sp'] if x['r'] != 'me')
        T(g, 'T2 새로고침 뒤 기억(jopangi_ui.note_color = 0)', auto9 == 0 and (p.ev("()=>__HN.ui()") or {}).get('note_color') == 0, {'auto': auto9, 'ui': p.ev("()=>__HN.ui()")})
        p.click(p.ev("f=>__HN.headAt(f,'on')", N131), 400)
        # 길게 누르기(글줄 메뉴)는 그대로 — 색 창이 안 뜬다
        L10 = p.ev("f=>__HN.lines(f)", N131) or []
        r9 = find_row(L10, '항소심계속중')
        a = p.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r9['ri'] if r9 else 9, 'X'])
        if a:
            p.pg.mouse.move(a['cx'], a['cy']); p.pg.mouse.down(); p.pg.wait_for_timeout(700); p.pg.mouse.up(); p.pg.wait_for_timeout(300)
        T(g, 'L1 칠한 글자 길게 누름 → 글줄 메뉴(🗒 메모 · ✎ 수정) · 색 창 안 뜸', p.ev("()=>__HN.pitOpen()") and not p.ev("()=>__HN.pick()"),
          {'pit': p.ev("()=>__HN.pitOpen()"), 'pick': p.ev("()=>__HN.pick()")})
        p.ev("()=>__HN.pitClose()")
        p.shot('%s_%s_note131' % (tag, eng))
        # 2차 카드 임베드 상자
        cd = p.ev("async c=>await __HN.card(c)", '25-62-4')
        E = p.ev("()=>__HN.embLines()") or []
        em = [l for l in E if l['ncf']]
        same = 0; diff = []
        for l in em:
            p.ev("async f=>await __HN.note(f)", l['ncf'])
            NL = p.ev("f=>__HN.lines(f)", l['ncf']) or []
            ref = NL[l['nri']] if l['nri'] is not None and l['nri'] < len(NL) else None
            a1 = [(x['w'], x['r'], x['color']) for x in l['sp']]   # 낱말 · 규칙 · 색(상자 줄은 줄 앞 탭 처리가 달라 자리 수가 밀릴 수 있다)
            b1 = [(x['w'], x['r'], x['color']) for x in (ref['sp'] if ref else [])]
            if a1 == b1:
                same += 1
            elif len(diff) < 3:
                diff.append({'f': l['ncf'][:12], 'ri': l['nri'], 'emb': a1[:4], 'note': b1[:4]})
        T(g, 'E1 2차 카드(25-62-4) 임베드 상자 민소 노트 줄 = 노트 팝업과 같은 칠', bool(em) and same == len(em) and any(l['sp'] for l in em),
          {'card': cd, 'lines': len(em), 'same': same, 'painted': sum(1 for l in em if l['sp']), 'diff': diff})
        # 다시 칠해도(끄고 켜기 = ncRepaint · 상자가 붙은 뒤) 상자 줄 칠이 그대로 — 줄 바깥(.embx)까지 올라가 가르면 여기서 글자가 0 이 된다
        p.ev("async c=>await __HN.card(c)", '25-62-4')
        sig = lambda E: [(l['ncf'], l['nri'], [(x['w'], x['r'], x['color']) for x in l['sp']]) for l in E if l['ncf']]
        e0 = sig(p.ev("()=>__HN.embLines()") or [])
        p.ev("()=>{S.noteColor=false;ncRepaint();S.noteColor=true;ncRepaint();return 1}")
        e1 = sig(p.ev("()=>__HN.embLines()") or [])
        T(g, 'E2 끄고 켜서 다시 칠해도 상자 줄 칠 그대로(줄 안쪽만 가른다)', bool(e0) and e0 == e1 and any(x[2] for x in e1),
          {'lines': len(e0), 'painted': sum(1 for x in e1 if x[2]), 'same': e0 == e1})
        er = [x for x in p.errs + (p.ev("()=>__HN.errs()") or []) if not CJ.NOISE(x)]
        T(g, 'Z 페이지 오류 0(잡음 빼고)', not er, er[:6])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


# ══════════ 다른 법 무변 · 폰 ══════════
def scen_other(br, base, new):
    g = 'NEW 다른 법 노트 무변'
    out = {}
    for tag, src in ((('BASE', base), ('NEW', new)) if QJ.GATE else (('NEW', new),)):
        p = Pg(br, 'chromium', tag, src, 1440, 900)
        try:
            R = {}
            for law in ('특허법', '상표법', '디자인보호법'):
                p.ev("l=>__HN.boot(l)", law)
                names = p.ev("async()=>await __HN.noteNames()") or []
                for f in names[:6]:
                    p.ev("async f=>await __HN.note(f)", f)
                    R[law + '|' + f] = p.ev("f=>{const w=POPS.find(x=>x._pk==='note|'+PLAW()+'|'+f+'|');return w?w.querySelector('.pb').innerHTML:null}", f)
            out[tag] = R
        finally:
            p.close()
    if QJ.GATE:
        a, b = out.get('BASE', {}), out.get('NEW', {})
        d = [k for k in a if a.get(k) != b.get(k)]
    else:
        b = out.get('NEW', {})
        _md = lambda s: None if s is None else hashlib.md5(s.encode('utf-8')).hexdigest()
        a = QJ.base('O1@chromium/dom', {k: _md(v) for k, v in b.items()})   # regress — 기준 칸: 바탕 노트 팝업 본문 = 기준 스냅샷(노트마다 md5 · 바탕 앱 안 띄움 · 스냅샷 없으면 NEW 값 = 첫 기록)
        d = [k for k in a if a.get(k) != _md(b.get(k))]
    T(g, 'O1 특허 · 상표 · 디보 노트 팝업 본문 DOM = 바탕(법마다 앞 여섯 노트)', bool(a) and a.keys() == b.keys() and not d and not any('class="nc' in (v or '') for v in b.values()),
      {'n': len(a), 'diff': d[:4]})


def scen_phone(br, eng, src):
    g = 'NEW %s 폰 390' % eng
    p = Pg(br, eng, 'NEW', src, 390, 844, phone=True)
    try:
        p.ev("()=>__HN.boot()"); p.ev("async f=>await __HN.note(f)", N131)
        L = p.ev("f=>__HN.lines(f)", N131) or []
        r7 = find_row(L, 'X<-관할-{사}')
        at = p.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r7['ri'] if r7 else 7, 'X'])
        p.click(at, 400)
        pk = p.ev("()=>__HN.pick()")
        T(g, 'M1 칠한 X 톡 → 색 창 · 화면 안', bool(pk) and pk['rect']['x'] >= 0 and pk['rect']['r'] <= 390 and pk['rect']['b'] <= 844, pk)
        p.click(p.ev("c=>__HN.pickAt(c)", 'navy'), 400)
        V = p.ev("()=>__HN.ls()") or {}
        T(g, 'M2 톡 남색 → 칸 1', len(V) == 1 and list(V.values())[0][0][2] == 'navy', V)
        er = [x for x in p.errs + (p.ev("()=>__HN.errs()") or []) if not CJ.NOISE(x)]
        T(g, 'Z 페이지 오류 0(잡음 빼고)', not er, er[:6])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


# ══════════ 동기화 — 새 키 jopangi.notecolor · 옛 판 기기 창(메모: 새 SYNC_KEYS 키는 옛 판 기기가 올릴 때 빠진다) ══════════
def scen_sync(br, base, new):
    g = 'NEW 동기화'
    A = Pg(br, 'chromium', 'NEW', new, 1440, 900, who='꼬까')
    B = Pg(br, 'chromium', 'NEW', new, 1440, 900, who='햄찌')
    C = Pg(br, 'chromium', 'BASE', base, 1440, 900, who='옛판')
    try:
        for x in (A, B, C):
            x.ev("()=>__HJ.quiet()"); x.ev("f=>__HJ.sync(f)", False); x.ev("()=>__HJ.quiet()")
        A.ev("()=>__HN.boot()"); A.ev("async f=>await __HN.note(f)", N131)
        L = A.ev("f=>__HN.lines(f)", N131) or []
        r7 = find_row(L, 'X<-관할-{사}')
        A.click(A.ev("([f,ri,w])=>__HN.at(f,ri,w,0)", [N131, r7['ri'] if r7 else 7, 'X']), 350)
        A.click(A.ev("c=>__HN.pickAt(c)", 'navy'), 500)
        k = '%s|%d' % (N131, r7['ri'] if r7 else 7)
        A.ev("()=>__HJ.quiet()"); A.ev("()=>__HJ.stamp()"); A.ev("([t,h])=>__HJ.remoteSet(t,h)", [None, None])
        A.ev("f=>__HJ.sync(f)", True)
        P1 = A.ev("()=>__HJ.remoteGet()")['text']
        p1 = json.loads(P1) if P1 else {'data': {}, 'u': {}}
        cell = (p1['data'].get('jopangi.notecolor') or {}).get(k)
        T(g, 'S1 새 판 A 고침 → 원격 data[jopangi.notecolor][<노트>|<행>] · 도장 u', cell == [[0, 1, 'navy', 'X']] and ('jopangi.notecolor|' + k) in p1.get('u', {}), cell)
        B.ev("([t,h])=>__HJ.remoteSet(t,h)", [P1, 'S1']); B.ev("f=>__HJ.sync(f)", False); B.ev("()=>__HJ.quiet()")
        B.ev("()=>__HN.boot()"); B.ev("async f=>await __HN.note(f)", N131)
        LB = B.ev("f=>__HN.lines(f)", N131) or []
        sb = span_at(find_row(LB, 'X<-관할-{사}'), 'X')
        T(g, 'S2 새 판 B 가 받으면 같은 칠(남색 점선)', bool(sb) and sb['r'] == 'me' and sb['color'] == NAVY, sb)
        C.ev("([t,h])=>__HJ.remoteSet(t,h)", [P1, 'S1'])
        C.ev("()=>{try{lsWrite('jopangi.editq',[{k:'hz1',target:'note',st:'대기',t:Date.now()}],'수정 큐');}catch(e){}return 1}")
        C.ev("()=>__HJ.quiet()"); C.ev("()=>__HJ.stamp()"); C.ev("f=>__HJ.sync(f)", True)
        p4 = json.loads(C.ev("()=>__HJ.remoteGet()")['text'])
        N(g, 'S3 옛 판 기기가 올린 원격 — 새 키 칸이 빠지는가(창)', {'data에 notecolor': 'jopangi.notecolor' in p4['data'], 'u 도장 남음': ('jopangi.notecolor|' + k) in p4.get('u', {}),
                                                         'gone 묘비': [x for x in (p4.get('gone') or {}) if x.startswith('jopangi.notecolor|')]})
        A.ev("([t,h])=>__HJ.remoteSet(t,h)", [json.dumps(p4, ensure_ascii=False), 'S4']); A.ev("f=>__HJ.sync(f)", False); A.ev("()=>__HJ.quiet()")
        p5 = json.loads(A.ev("()=>__HJ.remoteGet()")['text'])
        c5 = (p5['data'].get('jopangi.notecolor') or {}).get(k)
        T(g, 'S4 새 판 A 가 맞추면 원격에 칸이 되살아난다(묘비 0)', c5 == cell and not [x for x in (p5.get('gone') or {}) if x.startswith('jopangi.notecolor|')], c5)
        er = [y for x in (A, B, C) for y in (x.errs + (x.ev("()=>__HN.errs()") or [])) if not CJ.NOISE(y)]
        T(g, 'Z 페이지 오류 0(세 기기)', not er, er[:6])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        for x in (A, B, C):
            x.close()


def report(t0, newmd5, basemd5, CEN):
    lines = ['# _harness_jo_ms_notecolor — %s' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW md5(LF) %s · BASE md5(LF) %s · 데이터 = genie jo/data + note_color.json(이 하네스가 ⚙ note_color.py 로 만든 것)' % (newmd5, basemd5), '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:700]))
    if CEN:
        lines += ['', '규칙별 칠한 수(81 노트 · 같은 [행·자리·규칙] 을 하나로) — 채팅 시안 값과 나란히']
        for k in ('ox', 'loc', 'hb', 'pe', 'dict'):
            lines.append('  %-5s 채팅 %4d · %s' % (k, CHAT[k], ' · '.join('%s %d' % (t, c.get(k, 0)) for t, c in CEN.items())))
    new = [x for x in RES if x[2] is not None and not x[0].startswith('BASE')]
    base = [x for x in RES if x[2] is not None and x[0].startswith('BASE')]
    lines += ['', '헛잣대(BASE) — PASS %d · FAIL %d (새 기능 잣대는 FAIL 이어야 잣대)' % (sum(1 for x in base if x[2]), sum(1 for x in base if not x[2])),
              '합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (sum(1 for x in new if x[2]), sum(1 for x in new if not x[2]), time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(OUT, '_harness_jo_ms_notecolor_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(lines[-3:]))
    return sum(1 for x in new if not x[2])


def main():
    t0 = time.time()
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    new = io.open(NEWF, encoding='utf-8').read()
    if QJ.GATE:
        base = io.open(BASEF, encoding='utf-8').read() if BASEF else git('show', 'HEAD:jo/index.html').decode('utf-8')
    else:
        base = ''   # regress — 바탕 앱 풀기 0(git show 안 부름)
    md = lambda s: hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    run = lambda x: not ONLY or x in ONLY
    if not QJ.SMOKE:
        scen_data()
    CEN = {}
    with sync_playwright() as pw:
        cr = pw.chromium.launch()
        if run('base') and QJ.GATE:   # regress — 바탕(헛잣대) 책상 장면 0
            scen_desk(cr, 'chromium', base, 'BASE', CEN)
        if run('desk'):
            with QJ.stage('desk NEW chromium'):
                scen_desk(cr, 'chromium', new, 'NEW', CEN)
        if run('other') and not QJ.SMOKE:
            with QJ.stage('other 법 무변'):
                scen_other(cr, base, new)
        if run('phone') and not QJ.SMOKE:
            with QJ.stage('phone chromium'):
                scen_phone(cr, 'chromium', new)
        if run('sync') and QJ.GATE:   # regress — 세 기기 동기화 되살림(S1~S4 · 옛 판 기기 = 바탕 앱)은 canvas_jari E-6 ⑤ 로 합침(옛 31키 모사 기기) · 바탕 띄움 0
            scen_sync(cr, base, new)
        cr.close()
        if run('wk') and not QJ.SMOKE:
            wk = pw.webkit.launch()
            with QJ.stage('desk NEW webkit'):
                scen_desk(wk, 'webkit', new, 'NEW', CEN)
            wk.close()
    return report(t0, md(new), (md(base) if QJ.GATE else '(regress — 바탕 안 풀음)'), CEN)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
