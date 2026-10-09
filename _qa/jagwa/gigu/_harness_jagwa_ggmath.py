# -*- coding: utf-8 -*-
r"""_task_jagwa_ggmath §B 관문 「GM」 — 자과앱 근거 칸 수식 꼴 ggMath (세로 분수 · 위·아래 첨자 · 루트 · ∝ ≠ ≒ ↻ ↺)
(2026-10-04 · 지시서 jagwa/gigu/_task_jagwa_ggmath.md · 표 jagwa/gigu/_ggmath_rows.json · 시안 _ggmath_시안.html)

  python _harness_jagwa_ggmath.py [--root <genie 자리>] [--base <커밋>] [--only B1,B2,B3,B4,B5,B6,B7] [--eng chromium[,webkit]]
                                  [--res <결과>] [--text-only] [--cap <그림 폴더>]

  NEW  = --root 의 jagwa/index.html — 앱을 고치지 않는다(읽기만) · 기본 = genie 워크트리 ggmath(없으면 GENIE_ROOT)
  BASE = 헛잣대 = genie 커밋 --base(기본 4754b1d · 이 판 바로 앞) 의 jagwa/index.html — ggMath 가 없다(근거 글은 esc 로만 그린다)
  결과 줄 = 「PASS | 바탕 FAIL | 엔진 · 칸 | 값」 — 둘째 칸이 바탕 판정(— = 안 잼) · 끝 「== PASS n · FAIL m」(INFO 는 안 센다)
  --text-only = node 칸(B0 · B1 · B2 · B3 글자)만 · 브라우저 0
  --eng       = 기본 chromium · webkit 을 더하면 B6(네 폭)만 WebKit 에서도 돈다(아이패드가 그리는 자리 · :has · inline-flex)
  ⚠ 상태(2026-10-04 첫 판) — node 칸(B0 · B1 · B2 · B3 글자)은 돌려 확인했다 · 브라우저 칸(B3 DOM · B4 ~ B7)은 **짜기만 했고 아직 한 번도 안 돌았다**
    (그날 브라우저 한도 셋이 다 차 있었다) — 첫 실행에서 칸 고침이 나올 수 있다. 쪽 안 스크립트(GJS)는 문법 컴파일 · 판정 함수는 가짜 날값으로 돌려 확인했다.
  ⚠ 결과·출력에 사용자의 근거 글 앞 60 자(B2 ③ 바뀌는 글 목록)가 든다 — N: 에만 둔다. genie 의 _qa 사본으로 돌려도 결과 파일은 N: 로 간다(공개 저장소 보호).

  묶음
    B0  쪽 안 스크립트(GJS) 문법 · 앱에서 esc 줄과 WORD ~ ggMath 를 뽑음                                                       [node]
    B1  표 29 줄 — 앱 ggMath(in) === html(글자 그대로) · keep 6 줄은 esc(in) 과도 같음 · 바탕 = 함수 없음 → 23 줄 FAIL            [node]
    B2  실제 근거 글 전수(studyplandata 물리·지학·생물 data.gg 의 t · parts[].t · 댓글 뺌 · 읽기만)
          ① 글자 잃음 0(꼴 기호를 뺀 글이 같음 · 괄호는 분수 칸 묶음·루트 묶음 하나마다 두 개까지만 빠짐) ② 결과 태그 ∈ {span sup sub svg path}
          ③ 바뀌는 글 목록(과목·uid·원문 앞 60자·바뀐 꼴) · 날짜 꼴 · 밑줄 낀 주소는 따로 표시                                      [node]
    B3  막힘(XSS) — 글 다섯 · 댓글 둘: 글자 판정 [node] · 다섯 자리 DOM(img·script·i 0 · 화면 글 = 친 글자 · alert 0) [Chromium]
    B4  자리마다 — 넣음 5(펼친 근거 · 연결 상자 · 열람 창 · 쓰는 문항 창 · 지우기 확인) · 안 넣음(title · 고치기 칸 · 검색·찾기 .gl 셋 · 댓글) · 물리·지학·생물 [Chromium]
    B5  저장 무변 — 진짜 입력(칸에 쳐서 Enter) → GG · 올리는 몸 · 고치기 칸 · title 이 친 글자 그대로                                 [Chromium]
    B6  네 폭(1440·900·834·390) × 근거 다섯 자리 — 가로 넘침 0 · 폰 줄바꿈 · √ 위 줄과 꺾임 맞닿음 · 물리·지학                      [Chromium · WebKit]
    B7  화면 훑기(규칙 60) — 겹침(elementsFromPoint · 겹친 상자) · 잘림 · 글자 크기 어긋남 + 그림(PC 1440 · 폰 390) · 물리·지학          [Chromium]
  헛잣대 — 바탕에서 FAIL 이어야 하는 칸은 둘째 칸이 「바탕 FAIL」 · 바탕에서도 같아야 하는 칸(무변)은 「바탕 PASS」
    + 안 걸리는 잣대가 아님을 보이는 변이 둘(node): ① v8 꼴(그냥 괄호를 잃음) → B2 ① 이 걸려야 · ② 글자를 esc 안 함 → B3 이 걸려야
  기록 = route 사본(칸 이름만 있는 빈 기록 + 쪽 안에서 앱 함수(saveGG · saveGGREF)로 근거를 심음 · PUT 은 가로채 밖으로 안 나감 · HU 의 INIT) · studyplandata 는 읽기만(fetch · pull · 쓰기 0)
  ⚠ 자과앱 픽셀 IDENTICAL 게이트 없음(CLAUDE.md) — 쌓임 = elementsFromPoint · 그려졌는가 = DOM 개수 · 자리 = getBoundingClientRect · 그림(png)은 사람이 보는 것(게이트 아님)
  ★ 2026-10-09 옛 잣대 고침(jagwa/_task_jagwa_gg3.md §L-1-1 · §C-1 · 근거 = §A-4 표 「근거 줄」 · 「항목 줄」) — 물리 앱에 g3(window.G3)가 있으면
    「펼친 근거(panel)」 판 · 번호 칩([data-ggtog]) · 고치기 단추([data-gged])가 없다 → 그 자리 = 항목 줄 #view .g3list .g3r[data-g3k="uid|key|칸"] .g3tx
    (문항 열 때마다 접힘 #view.g3off → #g3Fold 로 폄 · 연결 상자도 그 안) · 6 번호 칩 title = 「칩 없음」(칩 0 · 항목 줄 있음) · 7 고치기 칸 = 길게 누름 0.55 초 .g3ed textarea ·
    10 댓글 = 「댓」(.g3cm) 펼친 .g3cmb · B-5 같은 꼴 · B0 소스 셈은 g3.js 덩이(패치 #35 · window.G3 를 둔 <script>) 몫을 빼고 셈
    g3 없는 앱(바탕 · 지학 · 생물)은 새 갈래를 안 탄다(옛 줄 그대로 · 바꾼 옛 줄은 「옛 줄:」 주석으로 남김)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · N_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
_roots.need_n('jagwa/gigu/_ggmath_rows.json · studyplandata 근거 글(비공개 기록 — N: 에서만)')
import hashlib, io, itertools, json, os, random, re, shutil, subprocess, sys, tempfile, time   # noqa: E402
from html.parser import HTMLParser   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if (k in sys.argv and sys.argv.index(k) + 1 < len(sys.argv)) else d


TEXT_ONLY = '--text-only' in sys.argv
GENIE = _roots.genie()
_DEF_ROOT = _roots.genie('.claude', 'worktrees', 'ggmath')
ROOT = ARG('--root') or (_DEF_ROOT if os.path.isdir(_DEF_ROOT) else GENIE)
BASE = ARG('--base', '4754b1d')
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
ENGS = [x for x in (ARG('--eng', 'chromium') or '').split(',') if x]
_DEF_OUT = os.path.join(HERE, '_harness_jagwa_ggmath_result.txt')
if (os.sep + '_qa' + os.sep) in (HERE + os.sep):   # genie 공개 저장소의 _qa 사본에서 돌면 결과(사용자 근거 글 든 것)를 N: 로 보낸다
    _DEF_OUT = _roots.n('jagwa', 'gigu', '_harness_jagwa_ggmath_result.txt') or _DEF_OUT
OUTF = ARG('--res', _DEF_OUT)
CAP = ARG('--cap', os.path.join(tempfile.gettempdir(), 'h_ggmath', 'cap'))
WORKD = os.path.join(tempfile.gettempdir(), 'h_ggmath', 'p%d' % os.getpid())   # node 임시 파일 — 실행마다 따로(둘이 겹쳐 돌아도 안 섞임) · 끝에 지움
SPD = _roots.spd()
ROWS_F = _roots.n('jagwa', 'gigu', '_ggmath_rows.json')
ROWS = []
APPS = {}


def want(g):
    return not ONLY or g in ONLY


def vs(v, n=420):
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)
    return s[:n]


def R(eng, name, okn, okb, val):
    """결과 한 줄 — okn = 새 판 · okb = 바탕(헛잣대) · None = INFO(안 센다) · 바탕 None = 「—」(안 잼)"""
    if QC.REGRESS:   # regress — 바탕(4754b1d) 판을 안 돌린다(node · 장면 · 훑기) → 바탕 칸은 늘 「—」
        okb = None
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name, vs(val)), flush=True)


def git(*a):
    return JG.git_HU(ROOT, *a)


# ── qa_slim2(2026-10-08) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작 = gate 에서 안 쓰는 갈래(gate 에서 도는 줄은 원래 글 그대로)
_RG_BOOT = "()=>__J.ready()&&typeof recBusy!=='undefined'&&!recBusy&&(((window.__PUTS||[]).length>0)||!!recErr)"   # 표지 = 앱 recBoot() 첫 syncRecords 끝(recBusy 거짓 · PUT 1 번 이상 또는 recErr) · INIT_HU 가 토큰을 넣어 부팅마다 맞춤 · PUT 을 한다


def _rg_over_base(eng, subj, W, rn):
    """regress — B-6 「바탕에 없던 새 넘침」 의 바탕 = 앞 인도판 NEW 훑기의 넘침 이름 스냅샷(자리마다) — j_over 가 읽는 꼴(places.<자리>.geo.overflow)로"""
    pl = {}
    for kind in PLACES:
        g = _g(rn, kind)
        cur = sorted({o['n'] for o in (g or {}).get('overflow', []) if o.get('bad')}) if g else None
        b = QC.base('B6.over@%s/%s/%d/%s' % (eng, subj, W, kind), cur)
        if isinstance(b, list):
            pl[kind] = {'geo': {'overflow': [{'n': n, 'bad': True} for n in b], 'outside': []}}
    return {'places': pl}


def esc_py(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ═══════════════════════ 글자 판정 도구 ═══════════════════════
FORM_WORDS = ('반시계방향', '시계방향', '=/=', '~=', '루트', '비례')   # 긴 것 먼저(「시계방향」을 품은 「반시계방향」)
FORM_CHARS = '()^_/-−'
FORM_SYMS = '√∝≠≒↺↻'   # √ ∝ ≠ ≒ ↺ ↻
RX_FORM = re.compile('|'.join(re.escape(w) for w in FORM_WORDS) + '|[' + re.escape(FORM_CHARS + FORM_SYMS) + ']')
RX_FORM_NP = re.compile('|'.join(re.escape(w) for w in FORM_WORDS) + '|[' + re.escape(FORM_CHARS.replace('(', '').replace(')', '') + FORM_SYMS) + ']')
ALLOWED_TAGS = {'span', 'sup', 'sub', 'svg', 'path'}
ALLOWED_ATTR = {('span', 'class'), ('svg', 'viewbox'), ('svg', 'preserveaspectratio'), ('svg', 'aria-hidden'), ('path', 'd')}
ALLOWED_CLS = {'gm-frac', 'n', 'd', 'gm-root', 'a'}


def strip_form(s):
    """꼴 기호(( ) ^ _ / - − · 루트 비례 =/= ~= 반시계방향 시계방향 · √ ∝ ≠ ≒ ↺ ↻)를 뺀 글"""
    return RX_FORM.sub('', s)


class HP(HTMLParser):
    """결과 HTML 읽개 — 글(textContent) · 태그 이름 · 속성 · 닫힘 짝"""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []; self.tags = []; self.attrs = []; self.stack = []; self.err = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for k, v in attrs:
            self.attrs.append((tag, k, v))
        if tag != 'path':
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.tags.append(tag)
        for k, v in attrs:
            self.attrs.append((tag, k, v))

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.err.append('닫는 태그 어긋남 </%s>' % tag)

    def handle_data(self, d):
        self.text.append(d)


def parse_html(h):
    p = HP(); p.feed(h); p.close()
    if p.stack:
        p.err.append('안 닫힌 태그 %s' % p.stack)
    return ''.join(p.text), p.tags, p.attrs, p.err


def tag_problems(tags, attrs, err):
    """② 태그 이름 ∈ {span sup sub svg path} 밖 · 속성 밖 · 닫힘 짝"""
    bad = []
    t = sorted(set(tags) - ALLOWED_TAGS)
    if t:
        bad.append('태그 %s' % t)
    a = [(tg, k) for tg, k, v in attrs if (tg, k) not in ALLOWED_ATTR or (k == 'class' and v not in ALLOWED_CLS)]
    if a:
        bad.append('속성 %s' % a[:4])
    if err:
        bad.append('; '.join(err[:2]))
    return bad


def _pairs(s):
    st = []; out = []
    for i, c in enumerate(s):
        if c == '(':
            st.append(i)
        elif c == ')' and st:
            out.append((st.pop(), i))
    return out


def paren_ok(orig, out_text):
    """괄호는 「분수 칸 묶음(/ 바로 앞·뒤) · 루트 묶음(루트 바로 뒤)」 하나마다 두 개(여는 · 닫는)까지만 빠짐 — 그 밖 괄호는 그대로"""
    rm = set()
    for m in RX_FORM_NP.finditer(orig):
        rm.update(range(m.start(), m.end()))
    S = [(c, i) for i, c in enumerate(orig) if i not in rm]
    B = RX_FORM_NP.sub('', out_text)
    cand = [(p, q) for p, q in _pairs(orig) if (p > 0 and orig[p - 1] == '/') or (q + 1 < len(orig) and orig[q + 1] == '/') or orig[max(0, p - 2):p] == '루트']
    nS = sum(1 for c, i in S if c in '()'); nB = sum(1 for c in B if c in '()')
    lost = nS - nB
    if lost < 0 or lost % 2:
        return False, '괄호 수 어긋남(빠짐 %d)' % lost
    need = lost // 2
    if need == 0:
        return ''.join(c for c, i in S) == B, '괄호 그대로' if ''.join(c for c, i in S) == B else '괄호 자리 어긋남'
    if need > len(cand):
        return False, '빠진 괄호쌍 %d > 분수 칸·루트 묶음 후보 %d' % (need, len(cand))
    for comb in itertools.combinations(range(len(cand)), need):
        rem = set()
        for k in comb:
            rem.add(cand[k][0]); rem.add(cand[k][1])
        if ''.join(c for c, i in S if i not in rem) == B:
            return True, '묶음 %d 개 빠짐' % need
    return False, '괄호가 분수 칸·루트 묶음 밖에서 빠짐(빠짐 %d)' % lost


def judge1(s, h):
    """① 글자 잃음 — 이유 목록(빈 목록 = 0)"""
    txt, tags, attrs, err = parse_html(h)
    why = []
    if strip_form(txt) != strip_form(s):
        why.append('꼴 기호 뺀 글이 다름')
    ok, msg = paren_ok(s, txt)
    if not ok:
        why.append(msg)
    return why


def judge2(h):
    """② 태그 · 속성 · 닫힘"""
    txt, tags, attrs, err = parse_html(h)
    return tag_problems(tags, attrs, err)


def kinds_of(s, h):
    k = []
    if 'class="gm-frac"' in h:
        k.append('분수')
    if 'class="gm-root"' in h:
        k.append('루트')
    if '<sup>' in h:
        k.append('위첨자')
    if '<sub>' in h:
        k.append('아래첨자')
    for sym, nm in (('∝', '∝ 비례'), ('≠', '≠'), ('≒', '≒'), ('↺', '↺ 반시계방향'), ('↻', '↻ 시계방향')):
        d = h.count(sym) - s.count(sym)
        if d > 0:
            k.append('%s×%d' % (nm, d))
    return k


# ═══════════════════════ node — 앱에서 뽑은 함수를 그대로 돌린다 ═══════════════════════
NODE_JS = r'''
const fs=require('fs'),vm=require('vm');
const [codeF,inF,outF]=process.argv.slice(2);
const code=fs.readFileSync(codeF,'utf8'),inputs=JSON.parse(fs.readFileSync(inF,'utf8'));
const sb={};vm.createContext(sb);let hasFn=false,initErr=null;
try{vm.runInContext(code+'\n;this.__esc=esc;this.__gm=(typeof ggMath==="function")?ggMath:null;',sb,{timeout:5000});hasFn=!!sb.__gm}catch(e){initErr=String(e)}
const out=[];
for(const s of inputs){try{sb.__inp=s;out.push({h:vm.runInContext('(this.__gm||this.__esc)(this.__inp)',sb,{timeout:3000})})}catch(e){out.push({err:String(e)})}}
fs.writeFileSync(outF,JSON.stringify({hasFn:hasFn,initErr:initErr,out:out}),'utf8');
'''
SYNTAX_JS = r'''
const fs=require('fs'),vm=require('vm');
try{new vm.Script(fs.readFileSync(process.argv[2],'utf8'));fs.writeFileSync(process.argv[3],JSON.stringify({ok:true}),'utf8')}
catch(e){fs.writeFileSync(process.argv[3],JSON.stringify({ok:false,err:String(e)}),'utf8')}
'''


def node_exe():
    p = shutil.which('node')
    if p:
        return p
    try:
        import playwright
        q = os.path.join(os.path.dirname(playwright.__file__), 'driver', 'node.exe' if os.name == 'nt' else 'node')   # 파이썬 playwright 가 싣고 온 node
        if os.path.isfile(q):
            return q
    except Exception:
        pass
    return None


NODE = node_exe()


def _wr(path, text):
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def run_node(code, inputs, tag):
    """code(= esc 줄 + WORD ~ ggMath) 를 vm 에서 돌려 inputs 마다 (ggMath || esc)(입력) 의 결과 HTML — 함수가 없으면 esc(바탕 = 옛 그림)"""
    if code is None and QC.REGRESS:   # regress — 바탕 코드(4754b1d) 없음 → 바탕 node 칸 안 돎(빈 결과 · R 의 바탕 칸 = 「—」)
        return {'out': [{} for _ in inputs], 'hasFn': None, 'initErr': None}
    os.makedirs(WORKD, exist_ok=True)
    cf, inf, outf, jf = [os.path.join(WORKD, '%s_%s' % (tag, n)) for n in ('code.js', 'in.json', 'out.json', 'run.js')]
    _wr(cf, code); _wr(inf, json.dumps(inputs, ensure_ascii=False)); _wr(jf, NODE_JS)
    if os.path.exists(outf):
        os.remove(outf)
    r = subprocess.run([NODE, jf, cf, inf, outf], capture_output=True, text=True, encoding='utf-8', timeout=180)
    if r.returncode != 0 or not os.path.exists(outf):
        raise RuntimeError('node 실패 rc=%s %s' % (r.returncode, (r.stderr or '')[:300]))
    return json.load(io.open(outf, encoding='utf-8'))


def js_syntax(code, tag):
    os.makedirs(WORKD, exist_ok=True)
    cf, jf, outf = [os.path.join(WORKD, '%s_%s' % (tag, n)) for n in ('syn.js', 'syn_run.js', 'syn_out.json')]
    _wr(cf, code); _wr(jf, SYNTAX_JS)
    if os.path.exists(outf):
        os.remove(outf)
    subprocess.run([NODE, jf, cf, outf], capture_output=True, text=True, encoding='utf-8', timeout=60)
    return json.load(io.open(outf, encoding='utf-8')) if os.path.exists(outf) else {'ok': False, 'err': '결과 없음'}


def extract(app):
    """앱(LF) → (code, meta) — code = 「const esc=…」 한 줄 + 「var WORD=」 ~ ggMath 끝 · 함수가 없으면 esc 줄만(바탕)"""
    L = app.split('\n')
    esc_l = [l for l in L if l.startswith('const esc=')]
    meta = {'esc줄': len(esc_l), 'ggMath': 0, '줄수': 0, 'md5': ''}
    if not esc_l:
        return None, meta
    code = esc_l[0] + '\n'
    fn = next((i for i, l in enumerate(L) if l.startswith('function ggMath(')), None)
    if fn is not None:
        a = next((i for i in range(max(0, fn - 6), fn + 1) if L[i].startswith('var WORD=')), fn)
        b = next((j for j in range(fn + 1, len(L)) if L[j] and not L[j][0].isspace() and not L[j].startswith('}')), len(L))
        code += '\n'.join(L[a:b]) + '\n'
        meta.update({'ggMath': sum(1 for l in L if l.startswith('function ggMath(')), '줄수': b - a})
    meta['md5'] = hashlib.md5(code.encode('utf-8')).hexdigest()[:8]
    return code, meta


def mutate(code, old, new):
    return code.replace(old, new) if (code and old in code) else None


MUT_V8 = ("plain='('+g.html+')'+tail}", "plain=g.html+tail}")        # 그냥 괄호를 잃음(시안 v8 꼴)
MUT_ESC = ("out+=esc(c);i++}", "out+=c;i++}")                       # 글자를 esc 안 함(막힘이 뚫림)


def load_apps():
    p = os.path.join(ROOT, 'jagwa', 'index.html')
    APPS['NEW'] = open(p, 'rb').read().replace(b'\r\n', b'\n')
    if QC.GATE:
        QC.sub('git:show-app')
        b = git('show', '%s:jagwa/index.html' % BASE)
        if not b:
            b = JG.git_HU(GENIE, 'show', '%s:jagwa/index.html' % BASE)
    else:   # regress · smoke — 바탕(4754b1d) 앱 풀기 0 · 바탕 node 칸 · 장면 · 훑기 0
        b = b''
    APPS['BASE'] = b


# ═══════════════════════ B0 · B1 · B2 · B3(글자) — node ═══════════════════════
XSS = ['<img src=x onerror=alert(1)>', 'a<b/c>d', '루트(<script>x</script>)', '1/<i>2</i>', '&amp;']
XSSC = ['<img src=x onerror=alert(1)>', 'a<b/c>d']          # 댓글 둘(첫째·둘째 근거에)
CODE = {}


def b0():
    app = {w: APPS[w].decode('utf-8') for w in ('NEW', 'BASE')}
    meta = {}
    for w in ('NEW', 'BASE'):
        CODE[w], meta[w] = extract(app[w])
    R('node', 'B0 앱에서 뽑기 — esc 줄 1 · var WORD ~ ggMath 함수 1(바탕 = 함수 없음)',
      bool(CODE['NEW']) and meta['NEW']['esc줄'] == 1 and meta['NEW']['ggMath'] == 1,
      bool(CODE['BASE']) and meta['BASE']['esc줄'] == 1 and meta['BASE']['ggMath'] == 1,
      {'NEW': meta['NEW'], '바탕': meta['BASE']})
    if QC.GATE:   # 관문만 — INFO(판정 없음) · 바탕 크기 · md5 · git rev-parse
        R('node', 'B0 앱 파일 — 새 판 LF %d B · 바탕 %s LF %d B' % (len(APPS['NEW']), BASE, len(APPS['BASE'])), None, None,
          {'NEW md5': hashlib.md5(APPS['NEW']).hexdigest()[:8], '바탕 md5': hashlib.md5(APPS['BASE']).hexdigest()[:8], 'root HEAD': git('rev-parse', '--short', 'HEAD').decode('utf-8', 'replace').strip()})
    CODE['MUT_V8'] = mutate(CODE['NEW'], *MUT_V8)
    CODE['MUT_ESC'] = mutate(CODE['NEW'], *MUT_ESC)
    sy = js_syntax(GJS, 'gjs')
    R('node', 'B0 쪽 안 스크립트(GJS) 문법 — 컴파일', bool(sy.get('ok')), None, sy.get('err', 'ok'))
    b0_static(app['NEW'], app['BASE'])


PATCH_F = _roots.n('jagwa', 'gigu', '_ggmath_patch.py')   # 채팅이 만든 패치 — FN_BLOCK · CSS_BLOCK 글자를 맞댄다(읽기만)


def patch_blocks():
    import ast
    if not PATCH_F or not os.path.isfile(PATCH_F):
        return None
    src = io.open(PATCH_F, encoding='utf-8').read()
    out = {}
    for name in ('FN_BLOCK', 'CSS_BLOCK'):
        m = re.search(r'^%s=(.*)$' % name, src, re.M)
        out[name] = ast.literal_eval(m.group(1)) if m else None
    return out


def g3_seg(t):
    """★ gg3(10/9) — 앱 글에서 g3.js 덩이(패치 #35 가 </body> 앞에 넣은 <script> · window.G3 를 둔 것) · 없으면 ''(바탕 · 지학·생물 판과 같은 글)"""
    i = t.find('window.G3={')
    if i < 0:
        return ''
    a, b = t.rfind('<script', 0, i), t.find('</script>', i)
    return t[a:b] if (a >= 0 and b > i) else ''


def b0_static(new, base):
    """B0 정적 칸 — 앱 글(소스)만 본다(브라우저 0): 글자 그대로 · 바뀐 곳 전수 · 이름 충돌 · 자리 다섯"""
    import difflib
    # ① 지시서 A-1 · A-2 「글자 그대로」 — 앱 안 함수 · CSS 가 패치 스크립트의 FN_BLOCK · CSS_BLOCK 과 같다(딱 1 번씩)
    if QC.GATE:   # 관문만 — ① 지시서 패치 글자 · ② 고정 바탕(4754b1d) 대비 diff 전수 = 그 판 인도 때만 뜻(뒤 판이 같은 자리를 고치면 거짓 FAIL)
        pb = patch_blocks()
        if pb and pb.get('FN_BLOCK') and pb.get('CSS_BLOCK'):
            cn, cb = new.count(pb['FN_BLOCK']), new.count(pb['CSS_BLOCK'])
            R('node', 'B0 글자 그대로 — 앱 안 ggMath 함수 · CSS 가 지시서 패치(_ggmath_patch.py)의 FN_BLOCK · CSS_BLOCK 과 같음(딱 1 번씩)', cn == 1 and cb == 1,
              base.count(pb['FN_BLOCK']) == 1 and base.count(pb['CSS_BLOCK']) == 1, {'새 판 FN · CSS 횟수': [cn, cb], '바탕': [base.count(pb['FN_BLOCK']), base.count(pb['CSS_BLOCK'])]})
        else:
            R('node', 'B0 글자 그대로 — 패치 스크립트를 못 읽음(건너뜀)', None, None, PATCH_F)
        # ② 바뀐 곳 전수 — 바탕 대비 차이가 ggMath 함수 · CSS · 자리 다섯(+ gtextH)뿐(저장 · 동기화 · 검색 · 한도 · KaTeX 줄은 한 줄도 안 바뀜 = A-4)
        a, b = base.split('\n'), new.split('\n')
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        rem, add = [], []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                continue
            rem += [(i + 1, a[i]) for i in range(i1, i2)]
            add += [(j + 1, b[j]) for j in range(j1, j2)]
        addset = {t for _n, t in add}
        swapped, unmatched, swaps = 0, [], set()
        for n, r in rem:   # 지운 줄마다 「esc( 한 곳 → ggMath(」 (또는 esc(gtext) → gtextH) 로 바꾼 짝이 더한 줄에 있어야
            cands = [r[:m.start()] + 'ggMath(' + r[m.end():] for m in re.finditer(r'esc\(', r)] + ([r.replace('esc(gtext)', 'gtextH')] if 'esc(gtext)' in r else [])
            hit = [c for c in cands if c in addset]
            if hit:
                swapped += 1; swaps.update(hit)
            else:
                unmatched.append((n, r.strip()[:60]))
        fa = next((i for i, l in enumerate(b) if l.startswith('/* ★ jagwa_ggmath (2026-10-04')), None)   # 함수 덩이 = 머리 주석 3 줄 + var WORD ~ ggMath 끝
        wa = next((i for i, l in enumerate(b) if l.startswith('var WORD=')), None)
        meta = extract(new)[1]
        fb = (wa + meta['줄수']) if wa is not None else None
        stray = []
        for n, t in add:
            if t.startswith('.gm-') or t.lstrip().startswith('/* ★ jagwa_ggmath'):
                continue                                                   # CSS 덩이
            if fa is not None and fb is not None and fa <= n - 1 < fb:
                continue                                                   # 함수 덩이
            if 'gtextH' in t or "esc('\\n'+g.cs.map(c=>'  ↳ '" in t:
                continue                                                   # 쓰는 문항 창 gtextH(근거 줄 = ggMath · 댓글 줄 = esc)
            if t in swaps:
                continue                                                   # 바꾼 줄 자신
            stray.append((n, t.strip()[:60]))
        ok = len(rem) == 6 and swapped == 6 and not unmatched and not stray and len(add) > 0
        R('node', 'B0 바뀐 곳 전수 — 바탕 대비 지운 줄 6(esc → ggMath 자리 다섯 + 패널 두 줄) · 더한 줄은 함수 · CSS · gtextH 뿐(그 밖 한 줄도 안 바뀜)', ok, None,
          {'지운 줄': len(rem), '바꾼 줄 짝': swapped, '짝 없는 지운 줄': unmatched[:3], '더한 줄': len(add), '밖의 더한 줄': stray[:4]})
    # ③ 이름 충돌 — WORD · ggMath 정의가 하나씩(뒤엣것이 이겨 조용히 엉뚱하게 그려지는 것 방지)
    def names(t):
        return {'WORD 정의': len(re.findall(r'\b(?:var|let|const|function)\s+WORD\b', t)), 'ggMath 정의': len(re.findall(r'\bfunction\s+ggMath\s*\(|\b(?:var|let|const)\s+ggMath\b', t)),
                'ggMath 대입': len(re.findall(r'\bggMath\s*=(?!=)', t)), 'gm- 클래스 CSS': len(re.findall(r'^\.gm-', t, re.M))}
    nn, nb = names(new), names(base)
    R('node', 'B0 이름 충돌 0 — WORD · ggMath 정의 하나씩 · 다시 대입 0 · .gm- CSS 규칙 9', nn['WORD 정의'] == 1 and nn['ggMath 정의'] == 1 and nn['ggMath 대입'] == 0 and nn['gm- 클래스 CSS'] == 9,
      nb['WORD 정의'] == 1 and nb['ggMath 정의'] == 1 and nb['ggMath 대입'] == 0 and nb['gm- 클래스 CSS'] == 9, {'새 판': nn, '바탕': nb})
    # ④ 자리 — 넣음 다섯은 ggMath · 안 넣음(title · 고치기 칸 · .gl · 댓글)은 esc/ea 그대로
    def sites(t):
        # 옛 줄: return {'ggMath(p.t)': t.count("ggMath(p.t)"), "ggMath(g.t||'')": t.count("ggMath(g.t||'')"), 'ggMath(ggFlat(g))': t.count('ggMath(ggFlat(g))'),
        # 옛 줄:         'ggMath(첫 줄)': t.count("ggMath(ggFlat(g).split('\\n')[0])"), 'esc(ggFlat(g)) 남음': t.count('esc(ggFlat(g))'),
        # 옛 줄:         'esc(첫 줄) 남음': t.count("esc(ggFlat(g).split('\\n')[0])")}
        g3 = g3_seg(t)   # ★ gg3(10/9) — g3.js 덩이(패치 #35)는 자리 다섯 밖(물리 g3 근거 줄 · 작은 창 · 쓰인 문항 창이 ggMath(ggFlat(g)) 를 4 곳 더 부름 · 3 → 7) → 빼고 셈 · 없으면 ''(옛 셈 그대로)
        t0 = t.replace(g3, '') if g3 else t
        d = {'ggMath(p.t)': t0.count("ggMath(p.t)"), "ggMath(g.t||'')": t0.count("ggMath(g.t||'')"), 'ggMath(ggFlat(g))': t0.count('ggMath(ggFlat(g))'),
             'ggMath(첫 줄)': t0.count("ggMath(ggFlat(g).split('\\n')[0])"), 'esc(ggFlat(g)) 남음': t0.count('esc(ggFlat(g))'),
             'esc(첫 줄) 남음': t0.count("esc(ggFlat(g).split('\\n')[0])")}
        if g3:
            d['g3.js 덩이 몫(뺌) ggMath(ggFlat(g))'] = g3.count('ggMath(ggFlat(g))')
        return d
    keep = lambda t: {'title ea(ggFlat)': t.count('ea(ggFlat(g))'), '댓글 esc(c.t)': t.count("esc(c.t||'')"), '상자 댓글 esc': t.count("esc((c&&c.t)||'')"), '.gl mark': t.count("'<div class=\"gl\">'+mark(line)+'</div>'")}
    sn, sb, kn, kb = sites(new), sites(base), keep(new), keep(base)
    if QC.REGRESS:   # regress — 기준 칸: 안 넣음 자리 글자 셈의 바탕 = 앞 인도판 스냅샷(바탕 앱 0)
        kb = QC.base('B0.keep', kn)
    ok_n = sn['ggMath(p.t)'] == 1 and sn["ggMath(g.t||'')"] == 1 and sn['ggMath(ggFlat(g))'] == 3 and sn['ggMath(첫 줄)'] == 1 and sn['esc(ggFlat(g)) 남음'] == 0 and sn['esc(첫 줄) 남음'] == 0
    R('node', 'B0 자리 다섯(§0-4 표 1~5) — ggMath 호출 p.t 1 · g.t 1 · ggFlat 3 · 지우기 첫 줄 1 · esc(ggFlat) 남음 0', ok_n,
      sb['ggMath(p.t)'] == 1 and sb['esc(ggFlat(g)) 남음'] == 0, {'새 판': sn, '바탕': sb})
    ok_k = kn == kb and all(v >= 1 for v in kn.values())
    R('node', 'B0 안 넣음 자리(표 6 · 9 · 10) — title ea(ggFlat) · 댓글 esc · 상자 댓글 esc · .gl mark 줄이 바탕과 같음(무변)', ok_k, ok_k, {'새 판': kn, '바탕': kb})


def b1():
    rows = json.load(io.open(ROWS_F, encoding='utf-8-sig'))['rows']
    ins = [r['in'] for r in rows]
    oN, oB = run_node(CODE['NEW'], ins, 'b1n'), run_node(CODE['BASE'], ins, 'b1b')
    R('node', 'B1 실행 — 앱에 ggMath 함수가 있다(바탕 = 없음 → esc 로 대신 그린다 = 옛 그림)', bool(oN['hasFn']) and not oN['initErr'], bool(oB['hasFn']), {'새 판 hasFn': oN['hasFn'], '바탕 hasFn': oB['hasFn']})
    an = ab = nk = 0
    for n, (r, on, ob) in enumerate(zip(rows, oN['out'], oB['out']), 1):
        hn, hb = on.get('h'), ob.get('h')
        okn = hn == r['html'] and (not r['keep'] or hn == esc_py(r['in']))
        okb = hb == r['html'] and (not r['keep'] or hb == esc_py(r['in']))
        an += okn; ab += okb; nk += bool(r['keep'])
        R('node', 'B1 표 %02d 「%s」 — %s%s' % (n, r['in'], r['what'], ' (keep)' if r['keep'] else ''), okn, okb,
          ('= ' + r['html']) if okn else {'새 판': hn if hn is not None else on.get('err'), '기대': r['html']})
    R('node', 'B1 합계 — 표 %d 줄 중 새 판 맞음 · 바탕 맞음(= keep %d 줄뿐이어야)' % (len(rows), nk), an == len(rows), ab == len(rows),
      {'줄': len(rows), '새 판 맞음': an, '바탕 맞음': ab, 'keep': nk, '바탕 FAIL 줄': len(rows) - ab})


def load_gg():
    """studyplandata 지금 판 — 물리 · 지학 · 생물 data.gg (읽기만)"""
    out = {}
    for s, label in (('phys', '물리'), ('earth', '지학'), ('bio', '생물')):
        d = json.loads(open(os.path.join(SPD, s, '기록.json'), 'rb').read().decode('utf-8'))
        items = []
        for uid, L in ((d.get('data') or {}).get('gg') or {}).items():
            for g in (L or []):
                if isinstance(g, dict):
                    items.append((uid, g))
        out[s] = (label, items, d.get('savedAt'))
    return out


def flat_of(g):
    p = g.get('parts')
    if isinstance(p, list) and p:
        return '\n'.join(((x.get('l') + ' ') if x.get('l') else '') + str(x.get('t', '')) for x in p)
    return str(g.get('t') or '')


def strings_of(g):
    """앱이 ggMath 에 넣는 글 — ggPanelHTML 은 parts[].t(없으면 t) · 나머지 넷은 ggFlat(g)"""
    out = []
    p = g.get('parts')
    out += [str(x.get('t', '')) for x in p] if (isinstance(p, list) and p) else [str(g.get('t') or '')]
    out.append(flat_of(g))
    seen = []
    for x in out:
        if x not in seen:
            seen.append(x)
    return seen


RX_DATE = re.compile(r'(?<![\w.])(\d{1,4})/(\d{1,2})(?:/(\d{1,4}))?(?![\w])')
RX_UND = re.compile(r'\S*[A-Za-z0-9가-힣]_[A-Za-z0-9가-힣(]\S*')


def b2():
    GG = load_gg()
    order = ['phys', 'earth', 'bio']
    allstr, owner, idx_of = [], [], {}
    for si, s in enumerate(order):
        for ii, (uid, g) in enumerate(GG[s][1]):
            for t in strings_of(g):
                idx_of.setdefault((s, ii), []).append(len(allstr))
                allstr.append(t); owner.append((s, ii))
    R('node', 'B2 재료 — studyplandata 기록.json data.gg(읽기만) 글 수', None, None,
      {GG[s][0]: {'uid': len({u for u, g in GG[s][1]}), '글': len(GG[s][1]), 'savedAt': GG[s][2]} for s in order})
    oN, oB = run_node(CODE['NEW'], allstr, 'b2n'), run_node(CODE['BASE'], allstr, 'b2b')
    oV = run_node(CODE['MUT_V8'], allstr, 'b2v') if CODE.get('MUT_V8') else None
    # 글(근거 하나)마다 모은다
    per = {}   # (subj, idx) -> dict
    for (s, ii), t, rn, rb in zip(owner, allstr, oN['out'], oB['out']):
        d = per.setdefault((s, ii), {'bad1': [], 'bad2': [], 'chg': False, 'kinds': [], 'bad1b': [], 'bad2b': [], 'err': []})
        if 'h' not in rn:
            d['err'].append(rn.get('err')); continue
        h = rn['h']
        w1 = judge1(t, h)
        if w1:
            d['bad1'].append((t[:40], w1))
        w2 = judge2(h)
        if w2:
            d['bad2'].append((t[:40], w2))
        if h != esc_py(t):
            d['chg'] = True
            for k in kinds_of(t, h):
                if k.split('×')[0] not in [x.split('×')[0] for x in d['kinds']]:
                    d['kinds'].append(k)
        hb = rb.get('h', '')
        if judge1(t, hb):
            d['bad1b'].append(t[:40])
        if judge2(hb):
            d['bad2b'].append(t[:40])
    v8 = {}
    if oV:
        for (s, ii), t, rv in zip(owner, allstr, oV['out']):
            if 'h' in rv and judge1(t, rv['h']):
                v8.setdefault(s, set()).add(ii)
    chg_all = []
    for s in order:
        label, items, _sa = GG[s]
        if not items:
            R('node', 'B2 %s — 근거 0글(기록이 비어 있다 — 잴 글 없음 · 판정 칸 아님)' % label, None, None, '')
            continue
        P = [per[(s, ii)] for ii in range(len(items))]
        b1n = [(items[ii][0], p['bad1'][:2]) for ii, p in enumerate(P) if p['bad1']]
        b2n = [(items[ii][0], p['bad2'][:2]) for ii, p in enumerate(P) if p['bad2']]
        er = [(items[ii][0], p['err'][:1]) for ii, p in enumerate(P) if p['err']]
        R('node', 'B2 ① 글자 잃음 0 — %s %d글(꼴 기호 뺀 글 같음 · 괄호는 분수 칸·루트 묶음 밖에서 안 빠짐)' % (label, len(items)),
          not b1n and not er, not any(p['bad1b'] for p in P), {'걸린 글': len(b1n), '예': b1n[:3], '오류': er[:2]})
        R('node', 'B2 ② 결과 태그 ∈ {span sup sub svg path}(속성 · 닫힘 포함) 밖 0 — %s %d글' % (label, len(items)),
          not b2n and not er, not any(p['bad2b'] for p in P), {'걸린 글': len(b2n), '예': b2n[:3]})
        ch = [(items[ii][0], items[ii][1], P[ii]['kinds']) for ii in range(len(items)) if P[ii]['chg']]
        chg_all.append((s, label, ch))
        cnt = {}
        for _u, _g, ks in ch:
            for k in ks:
                cnt[k.split('×')[0]] = cnt.get(k.split('×')[0], 0) + 1
        nb_chg = sum(1 for ii in range(len(items)) if any(('h' in oB['out'][k] and oB['out'][k]['h'] != esc_py(allstr[k])) for k in idx_of[(s, ii)]))
        R('node', 'B2 ③ 바뀌는 글 — %s %d글 중 %d글(꼴별 글 수 아래)' % (label, len(items), len(ch)), None, None,
          {'꼴별 글 수': cnt, '글 수': len(items), '바탕에서 바뀌는 글(함수 없음 = 0)': nb_chg})
        for uid, g, ks in ch:
            R('node', 'B2 ③ 바뀌는 글 · %s %s #%s' % (label, uid, g.get('i')), None, None,
              '「%s」 · 꼴: %s' % (flat_of(g)[:60].replace('\n', '⏎'), ' · '.join(ks)))
    n_v8 = sum(len(v) for v in v8.values())
    R('node', 'B2 ① 헛잣대 — 시안 v8 꼴 변이(그냥 괄호를 잃음)에서 ① 이 걸림(걸려야 이 잣대가 산다)', n_v8 > 0 if CODE.get('MUT_V8') else None, None,
      {'걸린 글': {GG[s][0]: len(v) for s, v in v8.items()}, '합': n_v8} if CODE.get('MUT_V8') else '변이를 못 만듦(앱 글이 바뀜)')
    # 날짜 꼴 · 밑줄 낀 주소 — 사용자 확인 거리(막을지는 사용자)
    outmap = {}
    for t, rn in zip(allstr, oN['out']):
        if 'h' in rn:
            outmap[t] = rn['h']
    dates, unders, toks = [], [], []
    for s in order:
        for uid, g in GG[s][1]:
            for m in RX_UND.finditer(flat_of(g)):
                toks.append((s, uid, m.group(0)))
    outT = run_node(CODE['NEW'], [x[2] for x in toks], 'b2u') if toks else {'out': []}
    for (s, uid, tok), r in zip(toks, outT['out']):
        if '<sub>' in (r.get('h') or ''):
            unders.append((GG[s][0], uid, tok, bool(re.search(r'[/.:@]', tok))))
    for s in order:
        for uid, g in GG[s][1]:
            t = flat_of(g)
            h = outmap.get(t, '')
            for m in RX_DATE.finditer(t):
                a, b = m.group(1), m.group(2)
                if ('<span class="gm-frac"><span class="n">%s</span><span class="d">%s</span></span>' % (a, b)) in h:
                    dates.append((GG[s][0], uid, m.group(0)))
    R('node', 'B2 날짜 꼴 — 「10/4」 「2024/10/04」 꼴이 분수로 바뀌는 글(사용자 확인 거리)', None, None, {'건': len(dates), '목록': dates[:12]})
    R('node', 'B2 밑줄 낀 주소 — 「a_b」 가 아래첨자로 바뀌는 낱말(사용자 확인 거리)', None, None,
      {'건': len(unders), '주소 꼴(/ . : @ 낌)': sum(1 for x in unders if x[3]), '목록': unders[:12]})
    return chg_all


def fuzz_inputs(n=600, seed=20261004):
    """난수 입력 — 절반은 낱자(꼴 기호 · < > & 섞음) · 절반은 식 조각을 이어 붙임(분수 · 루트 · 첨자 · 괄호가 자주 걸리게) · 씨앗 고정"""
    rnd = random.Random(seed)
    alpha = ['(', ')', '(', ')', '^', '_', '/', '/', '-', '−', '=', '~', '<', '>', '&', '"', "'", ' ', ' ', '1', '2', '10', '0.5', 'a', 'b', 'x', 'r', 'Δ', 'α', 'O', 'X', 'A', 'G', 'M',
             '루트', '비례', '시계방향', '반시계방향', '=/=', '~=', '가', '나', '\n', '.', ',', ':', '·', '↻', '√']
    pieces = ['1/2', 'v/c', '(GMm)/(r^2)', '루트(2)', '루트2', '루트(2GM/r)', 'F 비례 1/r^2', 'a =/= b', 'x_1', 'v_max', '10^-11', 'e^(x+1)', '(x+1)^2', 'O/X', 'X/O', 'km/h',
              'ΔT/Δt', '(a)/(b)', '((a))/b', '1/(2)/(3)', '루트(', '루트()', '^(', '_(', '(', ')', '/', '^', '_', ' ', ' ', ' ', '시계방향', '반시계방향', '~=', '<b>', '&', '"', 'abc', '가나다',
              '2GM', 'r2', 'A/B', '(1)', 'ㄱ', '\n', ' = ', ' + ', '-0.5y', '(T=Td)', '3/4', '루트(루트(2))', '1/루트(2)', '(루트(2))/3', '2^3^4', 'a_b_c', '10/4', '루트 2', '루트(2', '비례']
    out = [''.join(rnd.choice(alpha) for _ in range(rnd.randint(1, 18))) for _ in range(n // 2)]
    out += [''.join(rnd.choice(pieces) for _ in range(rnd.randint(2, 6))) for _ in range(n - n // 2)]
    return out


def b3_text():
    oN, oB = run_node(CODE['NEW'], XSS, 'b3n'), run_node(CODE['BASE'], XSS, 'b3b')
    oM = run_node(CODE['MUT_ESC'], XSS, 'b3m') if CODE.get('MUT_ESC') else None

    def safe(t, o):
        if 'h' not in o:
            return False, o.get('err')
        h = o['h']; txt, tags, attrs, err = parse_html(h)
        why = tag_problems(tags, attrs, err)
        if strip_form(txt) != strip_form(t):
            why.append('화면 글이 친 글자와 다름(꼴 기호 뺀 뒤) 「%s」' % txt[:40])
        return not why, why
    for t, on, ob in zip(XSS, oN['out'], oB['out']):
        okn, wn = safe(t, on); okb, wb = safe(t, ob)
        R('node', 'B3 막힘 글자 「%s」 — 태그 img·script·i 0 · 화면 글 = 친 글자(꼴 기호 빼고)' % t, okn, okb, '안전' if okn else wn)
    if oM:
        bad = [t for t, o in zip(XSS, oM['out']) if not safe(t, o)[0]]
        R('node', 'B3 헛잣대 — 글자를 esc 안 하는 변이에서 막힘 잣대가 걸림(걸려야 이 잣대가 산다)', len(bad) > 0, None, {'걸린 입력': bad})
    else:
        R('node', 'B3 헛잣대 — 변이를 못 만듦(앱 글이 바뀜)', None, None, '')
    fz = fuzz_inputs()
    oF, oFb = run_node(CODE['NEW'], fz, 'b3f'), run_node(CODE['BASE'], fz, 'b3fb')

    def fuzz_bad(ins, outs):
        bad = []
        for t, o in zip(ins, outs):
            if 'h' not in o:
                bad.append((t, 'throw ' + str(o.get('err'))[:60])); continue
            w = judge1(t, o['h']) + judge2(o['h'])
            if w:
                bad.append((t, w))
        return bad
    bn, bb = fuzz_bad(fz, oF['out']), fuzz_bad(fz, oFb['out'])
    R('node', 'B3 난수 입력 %d개(꼴 기호 · < > & 섞음 · 씨앗 고정) — 예외 0 · 태그 ∈ 화이트리스트 · 글자 잃음 0' % len(fz), not bn, not bb,
      {'걸린 입력': len(bn), '예': [(t[:30], w) for t, w in bn[:4]]})


# ═══════════════════════ 브라우저 — 쪽 안 도우미 ═══════════════════════
GJS = r"""
window.__G=(()=>{
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const tx=e=>e?String(e.textContent||''):'';
const vis=e=>!!e&&e.isConnected&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
const Rc=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {l:+r.left.toFixed(1),t:+r.top.toFixed(1),r:+r.right.toFixed(1),b:+r.bottom.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)}};
const shape=e=>{
  if(!e)return null;
  const q=s=>e.querySelectorAll(s);
  const f=e.querySelector('.gm-frac'),r=e.querySelector('.gm-root');
  return {frac:q('.gm-frac').length,root:q('.gm-root').length,sup:q('sup').length,sub:q('sub').length,svg:q('svg').length,
    img:q('img').length,script:q('script').length,i:q('i').length,
    fn:f?tx(f.querySelector('.n')):null,fd:f?tx(f.querySelector('.d')):null,ra:r?tx(r.querySelector('.a')):null,
    txt:tx(e),html:String(e.innerHTML).slice(0,300)}};
const secFor=u=>Object.keys(TOC.sec).find(s=>((TOC.sec[s]||{}).units||[]).includes(u))||'';
const XK=[1,2,3,4,5].map(i=>'g_ggm_x'+i);
const G={ctx:null,cur:null,shape:shape};
/* ★ gg3(10/9 · _task_jagwa_gg3 §A-4 「근거 줄」 · 「항목 줄」) — 물리 앱에 g3(window.G3)가 있으면 펼친 근거 판 · 번호 칩 · 고치기 단추가 없다:
   항목 줄 = #view .g3list .g3r[data-g3k="uid|key|칸"] .g3tx(심은 근거는 칸 f 없음 = 트리거 t) · 문항 열 때마다 접힘(#view.g3off → #g3Fold 로 폄) ·
   댓글 = 「댓」(.g3cm) 누르면 그 줄 밑 .g3cmb · 고치기 = 길게 누름 0.55 초 → .g3ed textarea — g3 없는 앱(바탕 · 지학 · 생물)은 아래 옛 길 그대로 */
const g3on=()=>!!(window.G3&&typeof window.G3==='object'&&typeof window.G3.push==='function');
const g3row=(u,k)=>document.querySelector('#view .g3list .g3r[data-g3k^="'+u+'|'+k+'|"]');
G.g3on=g3on;
G.g3unfold=async ()=>{const v=document.getElementById('view'),b=document.getElementById('g3Fold');
  if(v&&b&&v.classList.contains('g3off')){b.click();await sleep(150)}
  return !!v&&!v.classList.contains('g3off')};
G.g3cs=async (u,ks)=>{const out=[];
  for(const kk of ks){const r=g3row(u,kk);if(!r)continue;
    const ck=u+'|'+kk+'|qp-'+(String(r.getAttribute('data-g3k')).split('|')[2]||'t'),sel='#view .g3cm[data-g3cm="'+ck+'"]';
    const b=document.querySelector(sel);if(!b)continue;
    b.click();await sleep(150);
    [...document.querySelectorAll('#view .g3cmb [data-ggcs="'+ck+'"] .ggcs .t')].forEach(e=>out.push({txt:tx(e),sh:shape(e)}));
    const b2=document.querySelector(sel);if(b2&&document.querySelector('#view .g3cmb')){b2.click();await sleep(150)}}
  return out};
G.g3edit=async (u,k)=>{
  const row=g3row(u,k),t=row?row.querySelector('.g3tx'):null;if(!t)return {err:'g3 항목 줄 없음 '+u+'-'+k};
  try{t.scrollIntoView({block:'center'})}catch(e){}
  const rc=t.getBoundingClientRect(),x=rc.left+Math.min(8,rc.width/2),y=rc.top+rc.height/2;
  const pe=ty=>new PointerEvent(ty,{bubbles:true,cancelable:true,composed:true,clientX:x,clientY:y,pointerId:7,pointerType:'mouse',isPrimary:true,button:0,buttons:ty==='pointerup'?0:1});
  t.dispatchEvent(pe('pointerdown'));await sleep(700);t.dispatchEvent(pe('pointerup'));await sleep(120);
  let how='길게 누름 0.7초',r2=g3row(u,k),ta=r2?r2.querySelector('.g3ed textarea'):null;
  if(!ta&&r2&&typeof window.g3EditInline==='function'&&window.g3EditInline(r2)){how='g3EditInline 직접';await sleep(80);ta=r2.querySelector('.g3ed textarea')}
  const lab=ta?ta.closest('.g3ed').querySelector('input.lab'):null;
  const out={ta:ta?ta.value:null,lab:lab?lab.value:null,how:how};
  if(ta){ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}));await sleep(150)}
  out.left=document.querySelectorAll('#view .g3list .g3ed').length;
  return out};

/* 한 절 안에서 근거 없는 문항 넷을 골라(A 식 · B 연결 · X 막힘 · C 입력) 앱의 GG · GGREF 에 심는다 — 앱 함수(saveGG · saveGGREF)로 저장 */
G.plant=async spec=>{
  const bySec={};
  DATA.forEach(r=>{
    if(isC(r))return;
    if(!showKind(r))return;
    if(typeof phPast==='function'&&!phPast(r))return;
    const no=r[F.NO],u=unitOf(no);if(!u)return;
    const sec=secFor(u);if(!sec)return;
    const ua=(TOC.sec[sec].units||[]),us=ua.some(x=>x!==sec)?ua.filter(x=>x!==sec):ua;   /* 열람 창(jnOpen)이 그리는 단원만 — 지학은 절 자신을 뺀다 */
    if(!us.includes(u))return;
    if(ggOf(GGU(r)).length)return;
    if(typeof GGNOTE_F6!=='undefined'&&GGNOTE_F6[String(no)])return;
    (bySec[sec]=bySec[sec]||[]).push(no)});
  let pick=null;
  for(const sec of Object.keys(bySec)){if(bySec[sec].length>=4){pick={sec:sec,nos:bySec[sec].slice(0,4)};break}}
  if(!pick)return {err:'근거 없는 문항 4 개가 든 절이 없다',secs:Object.keys(bySec).length};
  const nos=pick.nos,uid=n=>GGU(rec(n));
  const c={sec:pick.sec,nA:nos[0],nB:nos[1],nX:nos[2],nC:nos[3]};
  c.uA=uid(c.nA);c.uB=uid(c.nB);c.uX=uid(c.nX);c.uC=uid(c.nC);
  const T0=Date.now()-60000;
  GG[c.uA]=[{k:'g_ggm_a1',i:1,t:spec.formula,ok:null,ts:T0,cs:[{k:'c_ggm_a1',t:spec.comment,ts:T0}]}];
  GG[c.uX]=spec.xss.map((t,n)=>({k:'g_ggm_x'+(n+1),i:n+1,t:t,ok:null,ts:T0,cs:n<spec.xssc.length?[{k:'c_ggm_x'+(n+1),t:spec.xssc[n],ts:T0}]:[]}));
  GGREF[c.uB]=[c.uA,c.uX];
  await saveGG();await saveGGREF();
  if(!(ggOf(c.uA).length===1&&ggOf(c.uX).length===spec.xss.length&&ggRefOf(c.uB).length===2))return {err:'심은 근거가 앱에 안 보임',ctx:c};
  G.ctx=c;return c};

/* 물리는 PDF 가 없으면 설정 창이 400ms 뒤 저절로 뜬다(앱 시동) — 덮개가 되니 닫는다(「닫기」= #bClose · 앱 몫 그대로) */
G.noSet=()=>{const x=document.getElementById('bClose');if(x&&document.getElementById('fi'))x.click()};
G.open=async no=>{
  G.noSet();try{closeView()}catch(e){}await sleep(150);
  let err='';
  try{await openView(no)}catch(e){err='ERR '+e}
  /* 물리 PDF 쪽이 안 그려져 showProblem 이 던져도 근거 줄(ggPhysPaint)은 그 뒤 몫이다 — 안 그려졌으면 앱 함수로 그린다(근거 줄만 잰다) */
  if(!HASBOOK&&!document.getElementById('ggphys')){try{ggPhysPaint()}catch(e){}}
  /* 옛 줄: await sleep(1400);G.noSet();return err||'ok'}; */
  await sleep(1400);G.noSet();
  if(g3on())await G.g3unfold();   /* ★ gg3 — 문항을 열면 근거 줄이 접혀 있다(#view.g3off · 연결 상자도 그 안) → 사람처럼 ▾ 로 편다 */
  return err||'ok'};

G.pPanel=async (u,k)=>{
  if(g3on()){const on=await G.g3unfold(),r=g3row(u,k);await sleep(100);   /* ★ gg3 — 펼친 판 · 번호 칩 없음 → 그 항목 줄(편 근거 줄 안) */
    return r?{how:'g3 항목 줄'+(on?'':' · 접힘'),vis:vis(r),title:null}:{err:'g3 항목 줄 없음 '+u+'-'+k}}
  const p=document.getElementById('qp-gg-pan-'+u+'-'+k);
  if(!p)return {err:'panel 없음 '+u+'-'+k};
  const chip=document.querySelector('[data-ggtog="'+u+'|'+k+'|qp-"]');
  let how='already';
  if(p.classList.contains('hide')){how='';if(chip){chip.click();how='click'}
    if(p.classList.contains('hide')){p.classList.remove('hide');how+='+force'}}
  await sleep(100);
  return {how:how,vis:vis(p),title:chip?chip.getAttribute('title'):null};};

G.closePlace=()=>{['jnw','gguw'].forEach(id=>{const e=document.getElementById(id);if(e)e.remove()});const x=document.getElementById('ggdX');if(x)x.click();G.cur=null};

G.items=()=>{
  const cur=G.cur;if(!cur||!cur.el)return null;
  const c=G.ctx,u=c['u'+cur.tgt];const out={rows:null,cs:null,whole:shape(cur.el)};
  if(cur.kind==='panel'){
    const ks=(cur.tgt==='A')?['g_ggm_a1']:XK;out.rows=[];out.cs=[];
    if(cur.g3){ks.forEach(kk=>{const r=g3row(u,kk);out.rows.push(shape(r?r.querySelector('.g3tx'):null))});out.cs=(cur.cs||[]).slice()}else   /* ★ gg3 — 항목 줄 .g3tx · 댓글 = 열 때 「댓」 으로 모은 것 · 아래 옛 줄 = g3 없는 앱 */
    ks.forEach(kk=>{const p=document.getElementById('qp-gg-pan-'+u+'-'+kk);
      out.rows.push(shape(p?p.querySelector('.hd .t'):null));
      (p?[...p.querySelectorAll('.ggcs .t')]:[]).forEach(e=>out.cs.push({txt:tx(e),sh:shape(e)}))})}
  else if(cur.kind==='refbox'){
    out.rows=[...cur.clip.querySelectorAll('.ggrr .t')].map(shape);
    out.cs=[...cur.clip.querySelectorAll('.ggrcl > span:first-child')].map(e=>({txt:tx(e),sh:shape(e)}))}
  else if(cur.kind==='jn'){out.rows=[...cur.el.querySelectorAll(':scope>div')].map(shape)}
  return out};

/* 자리 하나를 연다 — kind = panel(펼친 근거) · refbox(연결한 근거 상자) · jn(열람 창) · use(쓰는 문항 창) · del(지우기 확인 창) · tgt = A(식) · X(막힘 글) */
G.openPlace=async (kind,tgt)=>{
  const c=G.ctx,n=c['n'+tgt],u=c['u'+tgt],k=(tgt==='A')?'g_ggm_a1':'g_ggm_x1';
  G.closePlace();G.noSet();
  let el=null,clip=null,note='',title=null;
  let g3=null;   /* ★ gg3 — panel 자리가 g3 항목 줄이면 {cs · chips} */
  if(kind==='panel'){
    note=await G.open(n);
    const ks=(tgt==='A')?['g_ggm_a1']:XK;const hows=[];
    for(const kk of ks){const r=await G.pPanel(u,kk);hows.push(r.how||r.err)}
    note+=' '+hows.join(',');
    if(g3on()){   /* ★ gg3 — 번호 칩 0 · 펼친 판 = 그 항목 줄 .g3tx(판 = 그 줄) · 댓글은 「댓」 으로 모음(다시 그려지니 줄은 그 뒤에 다시 찾음) */
      g3={cs:await G.g3cs(u,ks),chips:document.querySelectorAll('#view [data-ggtog^="'+u+'|"]').length};
      const row=g3row(u,k);clip=row;el=row?row.querySelector('.g3tx'):null;
    }else{
    const chip=document.querySelector('[data-ggtog="'+u+'|'+k+'|qp-"]');title=chip?chip.getAttribute('title'):null;
    const p=document.getElementById('qp-gg-pan-'+u+'-'+k);clip=p;el=p?p.querySelector('.hd .t'):null;
    }
  }else if(kind==='refbox'){
    note=await G.open(c.nB);
    const b=document.getElementById('qp-gg-refbox-'+c.uB+'-'+u);
    if(b&&b.classList.contains('hide')){const chip=document.querySelector('[data-ggrt="'+c.uB+'|'+u+'|qp-"]');if(chip)chip.click();
      if(b.classList.contains('hide')){b.classList.remove('hide');note+=' force'}}
    clip=b;el=b?b.querySelector('.ggrr .t'):null;
  }else if(kind==='jn'){
    jnOpen(c.sec);await sleep(600);
    const row=document.querySelector('#jnw .jnrow[data-no="'+n+'"]');
    el=row?row.querySelector('.ggmine'):null;clip=document.querySelector('#jnw .panel');
  }else if(kind==='use'){
    ggUseWin(u);await sleep(400);
    el=document.querySelector('#gguw .gguh .gg');clip=document.querySelector('#gguw .panel');
  }else if(kind==='del'){
    ggDelAsk(u,k,'qp-');await sleep(250);
    const go=document.getElementById('ggdGo'),sh=go?go.closest('.sheet'):null;
    el=sh?sh.querySelector('small'):null;clip=sh?sh.querySelector('.panel'):null;
  }
  G.cur={kind:kind,tgt:tgt,el:el,clip:clip};
  if(g3){G.cur.g3=true;G.cur.cs=g3.cs;return {found:!!el,note:note,title:title,vis:vis(el),items:G.items(),g3:true,chips:g3.chips}}   /* ★ gg3 */
  return {found:!!el,note:note,title:title,vis:vis(el),items:G.items()}};

/* 자리 모양 — 가로 넘침 · 줄 수 · 겹침 · 맨 위 요소 · 잘림 · 글자 크기 · √ 꺾임(getBoundingClientRect · elementFromPoint) */
G.geo=()=>{
  const cur=G.cur;if(!cur||!cur.el)return {err:'식 칸 요소 없음'};
  const el=cur.el,clip=cur.clip||el;
  try{el.scrollIntoView({block:'center',inline:'nearest'})}catch(e){}
  const inF=n=>{const p=n.parentElement;const f=p?p.closest('.gm-frac,.gm-root'):null;return !!f&&el.contains(f)};
  const forms=[...el.querySelectorAll('.gm-frac,.gm-root')];
  const top=forms.filter(f=>!inF(f));
  const holder=el.closest('#card,#ggphys');
  const ov=(n,e)=>e?{n:n,sw:e.scrollWidth,cw:e.clientWidth,bad:e.scrollWidth-e.clientWidth>1}:null;
  const overflow=[ov('식 칸',el),ov('패널·창',clip),ov('카드',holder),
    {n:'쪽',sw:document.documentElement.scrollWidth,cw:innerWidth,bad:document.documentElement.scrollWidth-innerWidth>1}].filter(Boolean);
  const rk=clip.getBoundingClientRect();
  const outside=[];
  top.forEach((f,i)=>{const r=f.getBoundingClientRect();if(r.left<rk.left-1||r.right>rk.right+1)outside.push({i:i,l:+r.left.toFixed(1),r:+r.right.toFixed(1),cl:+rk.left.toFixed(1),cr:+rk.right.toFixed(1)})});
  const tr=[];
  const tw=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);let tn;
  while((tn=tw.nextNode())){
    if(!String(tn.nodeValue).trim())continue;
    const pe=tn.parentElement;
    if(pe){const pf=pe.closest('.gm-frac,.gm-root');if(pf&&el.contains(pf))continue}
    const rg=document.createRange();rg.selectNodeContents(tn);
    for(const r of rg.getClientRects()){if(r.width>0&&r.height>0)tr.push(r)}}
  const members=tr.concat(top.map(f=>f.getBoundingClientRect()).filter(r=>r.width>0&&r.height>0)).sort((a,b)=>a.top-b.top);
  const lines=[];
  members.forEach(r=>{const c=lines[lines.length-1];
    if(c&&r.top<(c.t+c.b)/2){c.t=Math.min(c.t,r.top);c.b=Math.max(c.b,r.bottom)}else lines.push({t:r.top,b:r.bottom})});
  const inter=(a,b)=>Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left))*Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
  const overlaps=[];
  top.forEach((f,i)=>{const fr=f.getBoundingClientRect();
    tr.forEach(t=>{const a=inter(fr,t);if(a>2)overlaps.push({f:i,area:+a.toFixed(1)})});
    top.forEach((g,j)=>{if(j>i){const a=inter(fr,g.getBoundingClientRect());if(a>2)overlaps.push({f:i,g:j,area:+a.toFixed(1)})}})});
  const cover=top.map((f,i)=>{
    const r=f.getBoundingClientRect();
    const on=r.width>0&&r.height>0&&r.top>=0&&r.bottom<=innerHeight&&r.left>=0&&r.right<=innerWidth;
    const pts=[[r.left+r.width/2,r.top+r.height/2]];
    if(f.classList.contains('gm-frac')){[':scope>.n',':scope>.d'].forEach(s=>{const x=f.querySelector(s);if(x){const q=x.getBoundingClientRect();pts.push([q.left+q.width/2,q.top+q.height/2])}})}
    const res=pts.map(p=>{const t=document.elementFromPoint(p[0],p[1]);return {in:!!t&&(f===t||f.contains(t)),top:t?(t.tagName+'.'+String(t.className||'').slice(0,20)):null}});
    return {i:i,on:on,ok:on&&res.every(x=>x.in),res:res}});
  const clipv=[];
  top.forEach((f,i)=>{const r=f.getBoundingClientRect();let a=f.parentElement;
    while(a&&a!==document.documentElement){const cs=getComputedStyle(a),ox=cs.overflowX,oy=cs.overflowY;
      if(ox!=='visible'||oy!=='visible'){const ar=a.getBoundingClientRect(),nm=String(a.id||a.className||a.tagName).slice(0,24);
        if(ox!=='visible'&&(r.left<ar.left-1||r.right>ar.right+1))clipv.push({i:i,anc:nm,dir:'x',f:[+r.left.toFixed(1),+r.right.toFixed(1)],a:[+ar.left.toFixed(1),+ar.right.toFixed(1)]});
        if(oy==='hidden'&&(r.top<ar.top-1||r.bottom>ar.bottom+1))clipv.push({i:i,anc:nm,dir:'y',f:[+r.top.toFixed(1),+r.bottom.toFixed(1)],a:[+ar.top.toFixed(1),+ar.bottom.toFixed(1)]})}
      a=a.parentElement}});
  const fz=e=>parseFloat(getComputedStyle(e).fontSize);
  const fonts=[];
  el.querySelectorAll('.gm-frac').forEach(f=>fonts.push({k:'분수',r:+(fz(f)/fz(f.parentElement)).toFixed(3)}));
  el.querySelectorAll('.gm-root').forEach(f=>{fonts.push({k:'루트',r:+(fz(f)/fz(f.parentElement)).toFixed(3)});
    const a=f.querySelector(':scope>.a');if(a)fonts.push({k:'루트 안',r:+(fz(a)/fz(f)).toFixed(3)})});
  el.querySelectorAll('sup,sub').forEach(f=>fonts.push({k:f.tagName.toLowerCase(),r:+(fz(f)/fz(f.parentElement)).toFixed(3)}));
  const roots=[...el.querySelectorAll('.gm-root')].map(rt=>{
    const s=rt.querySelector(':scope>svg'),a=rt.querySelector(':scope>.a');
    if(!s||!a)return {err:'svg 또는 .a 없음'};
    const sr=s.getBoundingClientRect(),ar=a.getBoundingClientRect();
    const xe=sr.left+sr.width*10.6/10,ye=sr.top+sr.height*0.55/20;
    return {sh:+sr.height.toFixed(2),ah:+ar.height.toFixed(2),dTop:+(sr.top-ar.top).toFixed(2),dBot:+(sr.bottom-ar.bottom).toFixed(2),
      gap:+(ar.left-sr.right).toFixed(2),dx:+(xe-ar.left).toFixed(2),dy:+(ye-ar.top).toFixed(2),
      touch:Math.abs(sr.top-ar.top)<=1&&Math.abs(sr.bottom-ar.bottom)<=1&&Math.abs(ar.left-sr.right)<=1&&xe>=ar.left-0.6&&xe<=ar.left+3&&ye>=ar.top-0.6&&ye<=ar.top+1.7}});
  return {n:top.length,fracAll:el.querySelectorAll('.gm-frac').length,rootAll:el.querySelectorAll('.gm-root').length,overflow:overflow,outside:outside,
    lines:lines.length,overlaps:overlaps,cover:cover,clipv:clipv,fonts:fonts,roots:roots,vw:innerWidth,vh:innerHeight,el:Rc(el),clip:Rc(clip)}};

G.shotRect=()=>{const cur=G.cur;if(!cur)return null;const e=cur.clip||cur.el;if(!e)return null;const r=e.getBoundingClientRect();
  const x=Math.max(0,Math.floor(r.left-4)),y=Math.max(0,Math.floor(r.top-4));
  const w=Math.min(innerWidth-x,Math.ceil(r.width+8)),h=Math.min(innerHeight-y,Math.ceil(r.height+8));
  return (w>0&&h>0)?{x:x,y:y,width:w,height:h}:null};

/* 안 넣음 7 — 고치기 칸(펼친 근거 · 연결 상자의 「✎ 여기서 고치기」)의 textarea 값 */
G.editBoxes=async ()=>{
  const c=G.ctx,u=c.uA,k='g_ggm_a1',out={};
  await G.open(c.nA);await G.pPanel(u,k);
  if(g3on()){out.panel=await G.g3edit(u,k);out.g3=true}else{   /* ★ gg3 — 고치기 단추 없음 → 항목 줄 길게 누름 0.55 초 = 그 자리 고치기 칸(.g3ed textarea · ㄱ·(1) 칸 없음) */
  const eb=document.querySelector('[data-gged="'+u+'|'+k+'|qp-"]');
  if(eb){eb.click();await sleep(150);
    const box=document.querySelector('[data-gged-box="'+u+'|'+k+'|qp-"]');
    const ta=box?box.querySelector('textarea.txt'):null,lab=box?box.querySelector('input.lab'):null;
    out.panel={ta:ta?ta.value:null,lab:lab?lab.value:null,rows:box?box.querySelectorAll('.ggrow').length:0};
    eb.click();await sleep(80)}else out.panel={err:'고치기 단추 없음'};
  }   /* ★ gg3 — 위 else 닫음 */
  await G.open(c.nB);
  const b=document.getElementById('qp-gg-refbox-'+c.uB+'-'+u);
  if(b&&b.classList.contains('hide')){const chip=document.querySelector('[data-ggrt="'+c.uB+'|'+u+'|qp-"]');if(chip)chip.click();if(b.classList.contains('hide'))b.classList.remove('hide')}
  const re=document.querySelector('[data-ggre="'+c.uB+'|'+u+'|'+k+'|qp-"]');
  if(re){re.click();await sleep(150);
    const rb=document.querySelector('[data-ggre-box="'+c.uB+'|'+u+'|'+k+'|qp-"]');const rta=rb?rb.querySelector('textarea.txt'):null;
    out.refbox={ta:rta?rta.value:null};re.click();await sleep(80)}else out.refbox={err:'연결 상자 고치기 단추 없음'};
  return out};

/* 안 넣음 9 — 검색·찾기 결과 .gl 셋: (a) 위 검색 줄 근거 모드 (b) 근거 단원 분포 → 단원 줄 (c) 카드 안 🔍 찾기 */
G.search9=async q=>{
  const c=G.ctx,out={a:null,b:null,c:null,err:[]};
  const gl=row=>row?[...row.querySelectorAll('.gl')].map(e=>({txt:tx(e),sh:shape(e)})):null;
  try{ggSearchMode('g');const inp=document.getElementById('q');inp.value=q;esSearch();await sleep(450);
    out.a=gl(document.querySelector('#esres [data-ggres="'+c.nA+'"]'));out.aN=document.querySelectorAll('#esres [data-ggres]').length}catch(e){out.err.push('a '+e)}
  try{const inp=document.getElementById('q');if(inp)inp.value='';ggSearchMode('q')}catch(e){}
  try{esDist();const i=ES_DK.indexOf(unitOf(c.nA));out.bi=i;esDistList(i);await sleep(350);
    out.b=gl(document.querySelector('#esres [data-ggres="'+c.nA+'"]'))}catch(e){out.err.push('b '+e)}
  try{const box=document.getElementById('esres');if(box){box.classList.add('hide');box.innerHTML=''}}catch(e){}
  try{await G.open(c.nB);
    const btn=document.querySelector('[data-ggfind="'+c.uB+'|qp-"]');if(btn)btn.click();
    const fb=document.querySelector('[data-ggfindbox="'+c.uB+'|qp-"]');const i2=fb?fb.querySelector('input'):null;
    if(i2){i2.value=q;ggFindRun(c.uB,'qp-');await sleep(250)}
    const rr=fb?[...fb.querySelectorAll('.res [data-ggpick]')].find(e=>String(e.getAttribute('data-ggpick')).indexOf(c.uB+'|'+c.uA+'|')===0):null;
    out.c=gl(rr)}catch(e){out.err.push('c '+e)}
  return out};

/* B-5 — 칸에 쳐서 Enter 한 뒤: 저장 값(GG) · SYNC 몸 · title · 펼친 근거 · 고치기 칸 */
G.afterAdd=async ()=>{
  const c=G.ctx,u=c.uC,L=ggOf(u),g=L[0]||null;
  if(!g)return {err:'GG 에 안 들어감',n:L.length};
  const sg=SYNC_REF.gg.g()||{};
  const out={n:L.length,t:g.t,parts:g.parts||null,k:g.k,sync:(sg[u]&&sg[u][0])?sg[u][0].t:null};
  if(g3on()){   /* ★ gg3 — 번호 칩 없음(title 칸 → 칩 0) · 아래 근거 줄 = 그 항목 줄 .g3tx · 고치기 칸 = 길게 누름 */
    out.g3=true;out.chips=document.querySelectorAll('#view [data-ggtog^="'+u+'|"]').length;out.title=null;
    const pr=await G.pPanel(u,g.k);out.how=pr.how||pr.err;
    const r=g3row(u,g.k);out.panel=shape(r?r.querySelector('.g3tx'):null);
    const e=await G.g3edit(u,g.k);out.edit=e.ta;out.editHow=e.how||e.err;
    return out}
  const chip=document.querySelector('[data-ggtog^="'+u+'|'+g.k+'|"]');out.title=chip?chip.getAttribute('title'):null;
  const pr=await G.pPanel(u,g.k);out.how=pr.how||pr.err;
  const p=document.getElementById('qp-gg-pan-'+u+'-'+g.k);out.panel=shape(p?p.querySelector('.hd .t'):null);
  const eb=document.querySelector('[data-gged="'+u+'|'+g.k+'|qp-"]');
  if(eb){eb.click();await sleep(150);const box=document.querySelector('[data-gged-box="'+u+'|'+g.k+'|qp-"]');const ta=box?box.querySelector('textarea.txt'):null;out.edit=ta?ta.value:null;eb.click()}
  return out};

G.dbg=()=>({vno:(typeof VNO!=='undefined')?VNO:null,ctx:G.ctx,gg:Object.keys(GG||{}).length,ggref:Object.keys(GGREF||{}).length,alerts:(window.__alerts||[]).length});
return G})();
"""

INIT2 = r"""
window.__alerts=[];window.alert=function(m){window.__alerts.push(String(m))};
window.confirm=function(){return false};window.prompt=function(){return null};
"""

FORMULA = '1/2 · 루트(2) · 북 시계방향'
CMT = '댓글 1/2 루트(2) 시계방향'
LONG = '(GMm)/(r^2) = 루트(2GM/r) 그리고 F 비례 1/r^2 이고 v_max ~= 10^-11'
SPEC = {'formula': FORMULA, 'comment': CMT, 'xss': XSS, 'xssc': XSSC}
SPEC_LONG = {'formula': LONG, 'comment': CMT, 'xss': XSS, 'xssc': XSSC}
PLACES = ('panel', 'refbox', 'jn', 'use', 'del')
PLACE_KO = {'panel': '펼친 근거', 'refbox': '연결한 근거 상자', 'jn': '열람 창', 'use': '쓰는 문항 창', 'del': '지우기 확인 창'}
VP = {1440: 900, 900: 1000, 834: 1112, 390: 844}
SUBJ_KO = {'earth': '지학', 'bio': '생물', 'phys': '물리'}


class GDev(JG.Dev):
    """기기 하나 — HU.Dev 와 같되 창 크기 · 대화 상자 가로채기 · 쪽 안 도우미 얹기"""
    def __init__(self, br, eng, vp=None):
        self.eng = eng; self.S = JG.Srv()
        self.vp = vp or {'width': 1553, 'height': 900}
        mobile = bool(self.vp['width'] <= 1100 and eng == 'chromium')
        self.ctx = br.new_context(viewport=self.vp, device_scale_factor=1, has_touch=True, is_mobile=mobile)
        OK = ('http://127.0.0.1', 'https://cdnjs.cloudflare.com/', 'https://cdn.jsdelivr.net/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')
        self.ctx.route('**/*', lambda rt: rt.continue_() if rt.request.url.startswith(OK) else rt.abort())
        self.ctx.add_init_script(INIT2)
        self.pg = None; self.errs = []; self.dialogs = []

    def _dialog(self, d):
        self.dialogs.append('%s: %s' % (d.type, str(d.message)[:80]))
        try:
            d.dismiss()
        except Exception:
            pass

    def load(self, app, spd, subj, rec=None, static=None):
        QC.launch('base' if (APPS.get('BASE') and app is APPS.get('BASE')) else 'new')   # 셈(§B-4)
        self.S.app = app; self.S.spd = spd; self.S.rec = dict(rec or {}); self.S.static = dict(static or {})
        if self.pg:
            self.pg.close()
        self.ctx.clear_cookies()
        self.pg = self.ctx.new_page(); self.pg.set_default_timeout(150000)
        self.pg.add_init_script(JG.INIT_HU.replace('__SUBJ__', subj))
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:200]))
        self.pg.on('dialog', self._dialog)
        self.pg.goto('http://127.0.0.1:%d/app.html' % self.S.port, wait_until='load')
        self.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
        self.pg.evaluate(JG.JS_HU)
        for _ in range(120):
            if self.ev("()=>__J.ready()"):
                break
            self.pg.wait_for_timeout(250)
        for _ in range(40):   # 기록 맞춤이 끝나기를(물리 빈 기기의 되살림 포함)
            if not self.ev("()=>typeof recBusy!=='undefined'&&recBusy"):
                break
            self.pg.wait_for_timeout(250)
        if QC.GATE:
            self.pg.wait_for_timeout(2500)
        else:   # regress — 고정 2.5 초 대신 표지(첫 기록 맞춤 끝) · 상한 = 같은 2.5 초
            QC.until(self.pg, _RG_BOOT, 2500, 'ggmath 부팅 뒤 첫 syncRecords 끝(recBusy 거짓 · PUT 1+ 또는 recErr)')
        self.pg.evaluate(GJS)


def blank_rec(subj):
    """그 과목 기록.json 의 칸 이름만 가진 빈 기록 — 근거는 쪽 안에서 앱 함수로 심는다(기록 route 사본 · 밖으로 안 나감)"""
    real = json.loads(open(os.path.join(SPD, subj, '기록.json'), 'rb').read().decode('utf-8'))
    d = {'v': real.get('v', 1), 'savedAt': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()), 'by': '검산',
         'data': {k: {} for k in (real.get('data') or {})}, 'u': {}, 'gone': {}}
    return {'%s/기록.json' % subj: json.dumps(d, ensure_ascii=False).encode('utf-8')}


def jsd(x, n=200):
    return vs(x, n)


# ═══════════════════════ 브라우저 — 장면 하나(B3 · B4 · B5 몫을 한 번에) ═══════════════════════
def scene(br, eng, who, subj, do):
    """기기 하나를 열어 근거를 심고(식 A · 연결 B · 막힘 X · 입력 C) 자리마다 재어 날값을 모은다"""
    raw = {'subj': subj, 'who': who}
    dv = GDev(br, eng)
    try:
        dv.load(APPS[who], SPD, subj, rec=blank_rec(subj))
        ctx = dv.ev("s=>__G.plant(s)", SPEC)
        raw['ctx'] = ctx
        if not ctx or ctx.get('err'):
            return raw
        if 'B4' in do:
            b4 = {}
            for kind in PLACES:
                b4[kind] = dv.ev("a=>__G.openPlace(a[0],a[1])", [kind, 'A'])
                dv.ev("()=>__G.closePlace()")
            raw['b4'] = b4
            raw['edit'] = dv.ev("()=>__G.editBoxes()")
            raw['search'] = dv.ev("q=>__G.search9(q)", '시계방향')
        if 'B3' in do:
            b3 = {}
            for kind in PLACES:
                b3[kind] = dv.ev("a=>__G.openPlace(a[0],a[1])", [kind, 'X'])
                dv.ev("()=>__G.closePlace()")
            raw['b3'] = b3
        if 'B5' in do:
            dv.ev("n=>__G.open(n)", ctx['nC'])
            # 옛 줄: loc = dv.pg.locator('[data-ggrows="%s|qp-"] .ggrow .txt' % ctx['uC']).first
            loc = dv.pg.locator('[data-ggrows="%s|qp-%s"] .ggrow .txt' % (ctx['uC'], 't' if dv.ev("()=>__G.g3on()") else '')).first   # ★ gg3 — 물리 g3 적는 칸 = 「uid|qp-t」(토글 기본 트리거 칸 · g3LineHTML) · 없으면 옛 「uid|qp-」
            loc.fill(FORMULA, timeout=15000)
            loc.press('Enter', timeout=15000)
            dv.pg.wait_for_timeout(1200)
            raw['b5'] = dv.ev("()=>__G.afterAdd()")
            n = dv.ev("()=>__J.sync()")
            body = dv.ev("p=>__J.lastPut(p)", '%s/기록.json' % subj)
            try:
                bj = json.loads(body) if body else None
            except Exception:
                bj = None
            L5 = ((((bj or {}).get('data') or {}).get('gg') or {}).get(ctx['uC']) or [{}]) if bj else [{}]
            raw['b5']['put'] = {'n': n, 'body': bool(body), 't': (L5[0] or {}).get('t')}
        raw['alerts'] = dv.ev("()=>window.__alerts")
        raw['imgx'] = dv.ev("()=>document.querySelectorAll('img[src=x]').length")   # 막힘 글 「<img src=x …>」 가 쪽 어디에도 그림 요소가 되지 않았다
        raw['dialogs'] = list(dv.dialogs)
        raw['errs'] = dv.errs[:4]
    finally:
        dv.close()
    return raw


def fm_ok(sh, first_line=False):
    """식 하나가 그려졌나 — 분수 1(1 / 2) · 루트 1(루트 2) · ↻ 하나 · 친 꼴(1/2 · 루트 · 시계방향)이 글에 안 남음"""
    if not sh:
        return False
    t = (sh.get('txt') or '').split('\n')[0] if first_line else (sh.get('txt') or '')
    return (sh.get('frac') == 1 and sh.get('root') == 1 and sh.get('fn') == '1' and sh.get('fd') == '2' and sh.get('ra') == '2'
            and t.count('↻') == 1 and '1/2' not in t and '루트' not in t and '시계방향' not in t)


def plain_ok(sh, want_txt=None, first_line=False):
    """친 글자 그대로인가 — 식 요소 0 · (알면) 글이 같음"""
    if not sh:
        return False
    t = (sh.get('txt') or '').split('\n')[0] if first_line else (sh.get('txt') or '')
    return sh.get('frac') == 0 and sh.get('root') == 0 and sh.get('sup') == 0 and sh.get('sub') == 0 and (want_txt is None or t == want_txt)


def sh1(o, kind):
    """자리 열기 결과 → 식 칸 모양 하나"""
    if not o or not o.get('found'):
        return None
    it = o.get('items') or {}
    if kind in ('panel', 'refbox', 'jn'):
        r = it.get('rows') or []
        return r[0] if r else None
    return it.get('whole')


def cells_b4(raw, who):
    """B-4 — 칸 목록 [(이름, ok, 값)]"""
    sj = SUBJ_KO[raw['subj']]
    out = []
    if not raw.get('ctx') or raw['ctx'].get('err'):
        return [('B-4 %s 장면 — 근거 없는 문항 넷이 든 절을 못 찾음' % sj, False, raw.get('ctx'))]
    b4 = raw.get('b4') or {}
    for n, kind in enumerate(PLACES, 1):
        o = b4.get(kind)
        sh = sh1(o, kind)
        ok = fm_ok(sh, first_line=(kind == 'use'))
        out.append(('B-4 %s 넣음 %d %s — 식 하나: 분수 1(1/2) · 루트 1(루트 2) · ↻ 보임 · 친 꼴은 안 보임' % (sj, n, PLACE_KO[kind]), ok,
                    {k: (sh or {}).get(k) for k in ('frac', 'root', 'fn', 'fd', 'ra', 'txt')} if sh else (o or '자리 못 염')))
    # 안 넣음 6 — title
    t6 = (b4.get('panel') or {}).get('title')
    # 옛 줄: out.append(('B-4 %s 안 넣음 6 번호 칩 title — 친 글자 그대로(HTML 못 그림)' % sj, t6 == FORMULA, t6))
    p6 = b4.get('panel') or {}   # ★ gg3(10/9) — 물리 g3 = 번호 칩 없음(§A-4 항목 줄 v37 「번호·상자 없음」) → 그 문항 번호 칩 0 · 항목 줄 있음(표본 0 거저 참 막이)
    out.append(('B-4 %s 안 넣음 6 번호 칩 title — 친 글자 그대로(HTML 못 그림)' % sj, (t6 == FORMULA) if not p6.get('g3') else (p6.get('chips') == 0 and bool(p6.get('found'))),
                t6 if not p6.get('g3') else {'g3': '칩 없음(§A-4 항목 줄 v37 번호·상자 없음)', '번호 칩': p6.get('chips'), '항목 줄': bool(p6.get('found')), 'title': t6}))
    # 안 넣음 7 — 고치기 칸
    ed = raw.get('edit') or {}
    p7, r7 = (ed.get('panel') or {}), (ed.get('refbox') or {})
    # 옛 줄: out.append(('B-4 %s 안 넣음 7 고치기 칸 textarea — 친 글자 그대로(펼친 근거 · 연결 상자 둘 다)' % sj, p7.get('ta') == FORMULA and r7.get('ta') == FORMULA and p7.get('lab') == '', {'펼친 근거': p7, '연결 상자': r7}))
    g7 = bool(ed.get('g3'))   # ★ gg3(10/9) — 물리 g3: 고치기 단추 없음 → 항목 줄 길게 누름 0.55 초 그 자리 고치기 칸(.g3ed textarea · ㄱ·(1) 칸 없음 = lab 없음 · §A-4 근거 줄 · 항목 줄)
    out.append(('B-4 %s 안 넣음 7 고치기 칸 textarea — 친 글자 그대로(펼친 근거 · 연결 상자 둘 다)' % sj, p7.get('ta') == FORMULA and r7.get('ta') == FORMULA and ((p7.get('lab') is None) if g7 else (p7.get('lab') == '')),
                {'펼친 근거': p7, '연결 상자': r7} if not g7 else {'펼친 근거(g3 길게 누름 칸)': p7, '연결 상자': r7}))
    # 안 넣음 9 — 검색·찾기 결과 .gl 셋
    se = raw.get('search') or {}
    gls = {}
    for key, nm in (('a', '위 검색 줄'), ('b', '근거 단원 분포'), ('c', '카드 안 🔍 찾기')):
        L = se.get(key)
        gls[nm] = bool(L) and all(plain_ok(x.get('sh'), '1. ' + FORMULA) for x in L)
    out.append(('B-4 %s 안 넣음 9 검색·찾기 결과 .gl 셋(위 검색 줄 · 근거 단원 분포 · 카드 안 찾기) — 친 글자 그대로' % sj, all(gls.values()) and not se.get('err'),
                {'판정': gls, '글': {k: [x['txt'] for x in (se.get(k) or [])][:1] for k in ('a', 'b', 'c')}, 'err': se.get('err')}))
    # 안 넣음 10 — 댓글
    pc = ((b4.get('panel') or {}).get('items') or {}).get('cs') or []
    rc = ((b4.get('refbox') or {}).get('items') or {}).get('cs') or []
    uw = ((b4.get('use') or {}).get('items') or {}).get('whole') or {}
    ul = (uw.get('txt') or '').split('\n')
    ok10 = (len(pc) == 1 and pc[0]['txt'] == CMT and plain_ok(pc[0]['sh'], CMT)
            and len(rc) == 1 and rc[0]['txt'] == '↳ ' + CMT and plain_ok(rc[0]['sh'], '↳ ' + CMT)
            and len(ul) >= 2 and ul[1] == '  ↳ ' + CMT)
    out.append(('B-4 %s 안 넣음 10 댓글(펼친 근거 · 연결 상자 ↳ · 쓰는 문항 창 ↳ 줄) — 친 글자 그대로' % sj, ok10,
                {'펼친': [x['txt'] for x in pc][:1], '상자': [x['txt'] for x in rc][:1], '쓰는 창 둘째 줄': ul[1] if len(ul) > 1 else None}))
    return out


def cells_b3_dom(raw):
    out = []
    if not raw.get('ctx') or raw['ctx'].get('err'):
        return [('B-3 DOM 장면 — 근거 없는 문항 넷이 든 절을 못 찾음', False, raw.get('ctx'))]
    b3 = raw.get('b3') or {}

    def safe(sh):
        return bool(sh) and sh.get('img') == 0 and sh.get('script') == 0 and sh.get('i') == 0

    def same(sh, t):
        return bool(sh) and strip_form(sh.get('txt') or '') == strip_form(t)
    for kind, nm in (('panel', '펼친 근거'), ('refbox', '연결한 근거 상자'), ('jn', '열람 창')):
        it = (b3.get(kind) or {}).get('items') or {}
        rows = it.get('rows') or []
        ok = len(rows) == 5 and all(safe(r) and same(r, t) for r, t in zip(rows, XSS))
        cs = it.get('cs') or []
        pre = '↳ ' if kind == 'refbox' else ''
        okc = True
        if kind in ('panel', 'refbox'):
            okc = len(cs) == 2 and all(safe(c['sh']) and c['txt'] == pre + XSSC[n] for n, c in enumerate(cs))
        out.append(('B-3 DOM %s — 글 다섯 · 댓글 둘: img·script·i 0 · 화면 글 = 친 글자(꼴 기호 빼고) · 댓글은 글자 그대로' % nm, ok and okc,
                    {'줄': len(rows), '글자 같음': [same(r, t) for r, t in zip(rows, XSS)], '안전': [safe(r) for r in rows], '댓글': [c['txt'][:40] for c in cs]}))
    items = [{'i': n + 1, 't': t, 'cs': ([XSSC[n]] if n < len(XSSC) else [])} for n, t in enumerate(XSS)]
    want_use = '\n'.join('%d. %s' % (g['i'], g['t']) + ('\n' + '\n'.join('  ↳ ' + c for c in g['cs']) if g['cs'] else '') for g in items)
    uw = ((b3.get('use') or {}).get('items') or {}).get('whole')
    out.append(('B-3 DOM 쓰는 문항 창 — 글 다섯 · 댓글 둘: img·script·i 0 · 글 줄 = 친 글자(꼴 기호 빼고) · 댓글 줄은 글자 그대로',
                safe(uw) and strip_form(uw.get('txt') or '') == strip_form(want_use), {'글자 같음': strip_form((uw or {}).get('txt') or '') == strip_form(want_use), '안전': safe(uw), '앞 80자': ((uw or {}).get('txt') or '')[:80]}))
    dw = ((b3.get('del') or {}).get('items') or {}).get('whole')
    out.append(('B-3 DOM 지우기 확인 창 — 첫 줄 = 친 글자(꼴 기호 빼고) · img·script·i 0', safe(dw) and same(dw, XSS[0]), {'글': (dw or {}).get('txt'), '안전': safe(dw)}))
    al = raw.get('alerts') or []
    out.append(('B-3 alert 0 — window.alert 호출 0 · dialog 이벤트 0 · 쪽 어디에도 img[src=x] 0 · 페이지 오류 0', not al and not raw.get('dialogs') and not raw.get('errs') and not raw.get('imgx'),
                {'alert': al[:3], 'dialog': (raw.get('dialogs') or [])[:3], 'img[src=x]': raw.get('imgx'), 'pageerror': (raw.get('errs') or [])[:3]}))
    return out


def cells_b5(raw):
    out = []
    b5 = raw.get('b5')
    if not b5 or b5.get('err'):
        return [('B-5 저장 무변 — 입력 뒤 GG 에 들어감', False, b5)], False
    put = b5.get('put') or {}
    # 옛 줄: ok = (b5.get('n') == 1 and b5.get('t') == FORMULA and not b5.get('parts') and b5.get('sync') == FORMULA and put.get('t') == FORMULA
    # 옛 줄:       and b5.get('edit') == FORMULA and b5.get('title') == FORMULA)
    ok = (b5.get('n') == 1 and b5.get('t') == FORMULA and not b5.get('parts') and b5.get('sync') == FORMULA and put.get('t') == FORMULA
          and b5.get('edit') == FORMULA and ((b5.get('title') == FORMULA) if not b5.get('g3') else (b5.get('chips') == 0)))   # ★ gg3(10/9) — 물리 g3 = 번호 칩 없음(title 칸 → 칩 0) · 고치기 칸 = 길게 누름 칸
    out.append(('B-5 저장 무변 — 칸에 쳐서 Enter: GG[uid][0].t · 동기화 올릴 몸(SYNC gg · PUT 몸통) · 고치기 칸 · title 이 친 글자 그대로(근거 하나)', ok,
                {'GG 개수': b5.get('n'), 'GG t': b5.get('t'), 'SYNC gg': b5.get('sync'), 'PUT 몸통 t': put.get('t'), '고치기 칸': b5.get('edit'), 'title': b5.get('title'), 'PUT 수': put.get('n')}))
    if b5.get('g3'):   # ★ gg3 — 값에 g3 길(칩 수 · 고치기 길)
        out[-1][2].update({'g3': '칩 없음 · 고치기 = 길게 누름 칸', '번호 칩': b5.get('chips'), '고치기 길': b5.get('editHow')})
    sh = b5.get('panel')
    out.append(('B-5 입력 → 아래 근거 줄이 수식 꼴 — 펼친 근거에 분수 1 · 루트 1 · ↻', fm_ok(sh), {k: (sh or {}).get(k) for k in ('frac', 'root', 'fn', 'fd', 'ra', 'txt')}))
    return out, True


# ═══════════════════════ 브라우저 — 네 폭 훑기(B6 · B7) ═══════════════════════
def sweep(br, eng, who, subj, W, cap=True):
    H = VP[W]
    raw = {'subj': subj, 'W': W, 'who': who, 'places': {}}
    dv = GDev(br, eng, {'width': W, 'height': H})
    try:
        dv.load(APPS[who], SPD, subj, rec=blank_rec(subj))
        ctx = dv.ev("s=>__G.plant(s)", SPEC_LONG)
        raw['ctx'] = ctx
        if not ctx or ctx.get('err'):
            return raw
        for kind in PLACES:
            pr = {}
            try:
                o = dv.ev("a=>__G.openPlace(a[0],a[1])", [kind, 'A'])
                pr['open'] = {k: o.get(k) for k in ('found', 'note', 'vis')}
                pr['sh'] = sh1(o, kind)
                pr['geo'] = dv.ev("()=>__G.geo()")
                if cap and QC.GATE:   # regress — 사람 눈용 그림(게이트 아님) 안 찍음
                    rc = dv.ev("()=>__G.shotRect()")
                    if rc:
                        os.makedirs(CAP, exist_ok=True)
                        fn = os.path.join(CAP, '%s_%s_%s_%dpx_%s.png' % (eng, who, subj, W, kind))
                        try:
                            dv.pg.screenshot(path=fn, clip=rc, timeout=20000)
                            pr['png'] = fn
                        except Exception as e:
                            pr['png_err'] = repr(e)[:100]
            except Exception as e:
                pr['err'] = repr(e)[:200]
            try:
                dv.ev("()=>__G.closePlace()")
            except Exception:
                pass
            raw['places'][kind] = pr
        raw['errs'] = dv.errs[:3]
    finally:
        dv.close()
    return raw


def _g(raw, kind):
    pr = raw['places'].get(kind) or {}
    g = pr.get('geo')
    return g if (g and not g.get('err') and not pr.get('err')) else None


def j_over(raw, base=None):
    """가로 넘침 0 — 식 칸 · 패널·창 · 식이 창 밖은 늘 0(절대) · 카드 · 쪽은 base(같은 폭 바탕 판)를 주면 「바탕에 없던 새 넘침」만 센다(앱이 옛날부터 가진 넘침은 이 판 탓이 아니다)"""
    bad, miss, pre = [], [], []
    for kind in PLACES:
        g = _g(raw, kind)
        if not g:
            miss.append(kind); continue
        gb = _g(base, kind) if base else None
        for o in g['overflow']:
            if not o['bad']:
                continue
            msg = '%s·%s %d>%d' % (PLACE_KO[kind], o['n'], o['sw'], o['cw'])
            if o['n'] in ('카드', '쪽') and gb is not None and any(x['n'] == o['n'] and x['bad'] for x in gb['overflow']):
                pre.append(msg)
            else:
                bad.append(msg)
        if g['outside']:
            bad.append('%s·식이 창 밖 %d' % (PLACE_KO[kind], len(g['outside'])))
    d = {'넘침': bad[:6], '못 잰 자리': miss}
    if pre:
        d['바탕에도 있던 넘침(이 판 탓 아님)'] = pre[:4]
    return (not bad and not miss), d


def j_kink(raw):
    per, miss = {}, []
    for kind in PLACES:
        g = _g(raw, kind)
        if not g:
            miss.append(kind); continue
        rs = g['roots']
        per[kind] = {'√': len(rs), '맞닿음': sum(1 for r in rs if r.get('touch'))}
    ok = not miss and all(v['√'] >= 1 and v['맞닿음'] == v['√'] for v in per.values())
    d = {'자리별': per, '못 잰 자리': miss}
    if per:
        k0 = next(iter(per))
        g0 = _g(raw, k0)
        if g0 and g0['roots']:
            d['첫 √ 자리값'] = {k: g0['roots'][0].get(k) for k in ('sh', 'ah', 'dTop', 'dBot', 'gap', 'dx', 'dy')}
    return ok, d


def j_wrap(raw):
    """폰 390 줄바꿈 — 펼친 근거 · 연결 상자(한 줄에 단추가 같이 앉아 칸이 좁다)는 두 줄 이상 · 그 밖 창은 줄 수만 적는다(식이 줄어들어 한 줄에 들 수도 있다)"""
    ln = {}
    for kind in PLACES:
        g = _g(raw, kind)
        ln[kind] = g['lines'] if g else None
    # 옛 줄: ok = all((ln[k] or 0) >= 2 for k in ('panel', 'refbox')) if raw['W'] == 390 else None
    ok = all((ln[k] or 0) >= 1 for k in ('panel', 'refbox')) if raw['W'] == 390 else None   # ★ 10/4 첫 실행 뒤 — 지시서 식이 390 칸에 한 줄로 든다(바탕 · 새 판 둘 다 1 줄) → 두 줄 이상 또는 한 줄에 다 듦 · 가로 넘침 0 은 부르는 쪽에서 같이 봄
    return ok, {'줄 수': ln}


def j_overlap(raw):
    per, bad = {}, []
    for kind in PLACES:
        g = _g(raw, kind)
        if not g:
            bad.append('%s 못 잼' % kind); continue
        cv = g['cover']
        per[kind] = {'식': g['n'], '겹침': len(g['overlaps']), '맨 위 아님': sum(1 for c in cv if not c['ok'])}
        if g['n'] < 1:
            bad.append('%s 식 0개(표본 0 = 거저 참)' % PLACE_KO[kind])
        if g['overlaps']:
            bad.append('%s 겹침 %s' % (PLACE_KO[kind], g['overlaps'][:2]))
        for c in cv:
            if not c['ok']:
                bad.append('%s 식 %d 맨 위 아님/화면 밖 %s' % (PLACE_KO[kind], c['i'], c['res'][:2] if c['on'] else '화면 밖'))
    return not bad, {'자리별': per, '걸림': bad[:5]}


def j_clip(raw):
    bad = []
    for kind in PLACES:
        g = _g(raw, kind)
        if not g:
            bad.append('%s 못 잼' % kind); continue
        if g['n'] < 1:
            bad.append('%s 식 0개' % PLACE_KO[kind])
        if g['clipv'] or g['outside']:
            bad.append('%s 잘림 %s' % (PLACE_KO[kind], (g['clipv'] or g['outside'])[:2]))
        for r in g['roots']:
            if r.get('err') or r.get('sh', 0) <= 0 or abs(r.get('sh', 0) - r.get('ah', 0)) > 1:
                bad.append('%s √ 선 높이 어긋남 %s' % (PLACE_KO[kind], {k: r.get(k) for k in ('sh', 'ah')}))
    return not bad, {'걸림': bad[:5]}


FONT_RANGE = {'분수': (0.84, 0.88), '루트': (0.98, 1.02), '루트 안': (0.98, 1.02), 'sup': (0.70, 0.95), 'sub': (0.70, 0.95)}


def j_font(raw):
    bad, seen = [], {}
    for kind in PLACES:
        g = _g(raw, kind)
        if not g:
            bad.append('%s 못 잼' % kind); continue
        for f in g['fonts']:
            lo, hi = FONT_RANGE[f['k']]
            seen.setdefault(f['k'], []).append(f['r'])
            if not (lo <= f['r'] <= hi):
                bad.append('%s %s 배율 %s(기대 %s~%s)' % (PLACE_KO[kind], f['k'], f['r'], lo, hi))
    need = all(seen.get(k) for k in ('분수', '루트', 'sup', 'sub'))
    if not need:
        bad.append('분수·루트·위·아래첨자 가운데 안 재진 것 %s(표본 0 = 거저 참)' % [k for k in ('분수', '루트', 'sup', 'sub') if not seen.get(k)])
    return not bad, {'걸림': bad[:5], '배율 범위': {k: [min(v), max(v)] for k, v in seen.items()}}


# ═══════════════════════ 실행 ═══════════════════════
def run_browser():
    from playwright.sync_api import sync_playwright
    do_b3, do_b4, do_b5, do_b6, do_b7 = want('B3'), want('B4'), want('B5'), want('B6'), want('B7')
    chromium = [e for e in ENGS if e == 'chromium']
    scene_plan = []   # (subj, do-set)
    if do_b4:
        scene_plan += [('earth', {'B4'} | ({'B3'} if do_b3 else set()) | ({'B5'} if do_b5 else set())), ('bio', {'B4'}), ('phys', {'B4'})]
    elif do_b3 or do_b5:
        scene_plan += [('earth', ({'B3'} if do_b3 else set()) | ({'B5'} if do_b5 else set()))]
    widths = []
    if do_b6:
        widths = [1440, 900, 834, 390]
    if do_b7:
        widths = sorted(set(widths) | {1440, 390}, reverse=True)
    SW = [('earth', widths), ('phys', widths)]
    if QC.SMOKE:   # smoke — 지학 장면 하나(B-4 넣음 자리 식 꼴 · B-3 alert 0)만 · 훑기 안 돎
        scene_plan, widths = [('earth', {'B4', 'B3'})], []
    shots = []
    with sync_playwright() as pw:
        for eng in ENGS:
            try:
                br = getattr(pw, eng).launch()
            except Exception as e:
                R(eng, '브라우저 띄우기 실패', False, None, repr(e)[:300]); continue
            try:
                if eng == 'chromium':
                    for subj, do in scene_plan:
                        print('── %s · 장면 %s %s' % (eng, subj, sorted(do)), flush=True)
                        raws = {}
                        for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):   # regress — 바탕 장면(헛잣대 판정) 안 돎
                            try:
                                raws[who] = scene(br, eng, who, subj, do)
                            except Exception as e:
                                raws[who] = {'subj': subj, 'who': who, 'exc': repr(e)[:300]}
                                R(eng, 'B-x %s %s 장면 멈춤' % (SUBJ_KO[subj], who), False, None, repr(e)[:400])
                        rn, rb = raws['NEW'], raws['BASE'] if QC.GATE else {'exc': '(regress — 바탕 안 띄움)'}
                        if 'B4' in do and 'exc' not in rn:
                            cn = cells_b4(rn, 'NEW')
                            cbm = {}
                            if 'exc' not in rb:
                                for n, o, v in cells_b4(rb, 'BASE'):
                                    cbm[n] = o
                            for n, o, v in cn:
                                if not QC.want(n, smoke=(' 넣음 ' in n and '안 넣음' not in n)):   # smoke — B-4 넣음 자리 식 꼴만
                                    continue
                                R(eng, n, o, cbm.get(n), v)
                        if 'B3' in do and 'exc' not in rn:
                            cbm = {}
                            if 'exc' not in rb:
                                for n, o, v in cells_b3_dom(rb):
                                    cbm[n] = o
                            for n, o, v in cells_b3_dom(rn):
                                if not QC.want(n, smoke=n.startswith('B-3 alert 0')):   # smoke — B-3 alert 0 만
                                    continue
                                R(eng, n, o, cbm.get(n), v)
                        if 'B5' in do and 'exc' not in rn:
                            cn, _x = cells_b5(rn)
                            cbm = {}
                            if 'exc' not in rb:
                                for n, o, v in cells_b5(rb)[0]:
                                    cbm[n] = o
                            for n, o, v in cn:
                                R(eng, n, o, cbm.get(n), v)
                if (do_b6 or do_b7) and widths:
                    for subj, ws in SW:
                        for W in ws:
                            if eng != 'chromium' and not do_b6:
                                continue
                            print('── %s · 훑기 %s %dpx' % (eng, subj, W), flush=True)
                            sw = {}
                            # 옛 줄: for who in (('NEW', 'BASE') if eng == 'chromium' else ('NEW',)):
                            for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):   # ★ 10/4 첫 실행 뒤 — 웹킷도 바탕을 훑어 「바탕에 없던 새 넘침」 을 뺀다(원래 있던 카드 760>758 이 새 넘침으로 셈됐다) · regress — 바탕 넘침은 스냅샷
                                try:
                                    sw[who] = sweep(br, eng, who, subj, W)
                                except Exception as e:
                                    sw[who] = {'subj': subj, 'W': W, 'who': who, 'places': {}, 'exc': repr(e)[:300]}
                                    R(eng, 'B-6 %s %dpx %s 훑기 멈춤' % (SUBJ_KO[subj], W, who), False, None, repr(e)[:400])
                            rn, rb = sw['NEW'], sw.get('BASE')
                            sj = SUBJ_KO[subj]
                            if 'exc' in rn:
                                continue
                            if not rn.get('ctx') or rn['ctx'].get('err'):
                                R(eng, 'B-6 %s %dpx 장면 — 근거 없는 문항 넷이 든 절을 못 찾음' % (sj, W), False, None, rn.get('ctx')); continue
                            for kind in PLACES:
                                pr = rn['places'].get(kind) or {}
                                if pr.get('png'):
                                    shots.append(pr['png'])
                            bok = bool(rb and 'exc' not in rb and rb.get('ctx') and not rb['ctx'].get('err'))   # 바탕 훑기가 잘 돌았나(WebKit 은 안 돎)
                            if QC.REGRESS:   # regress — 기준 칸: 「바탕에 없던 새 넘침」 의 바탕 = 앞 인도판 NEW 넘침 이름 스냅샷
                                _rg_ob = _rg_over_base(eng, subj, W, rn)
                            if do_b6:
                                okn, vn = j_over(rn, (rb if bok else None) if QC.GATE else _rg_ob)
                                if QC.REGRESS:
                                    vn['기준'] = QC.base_note('B6.over@%s/%s/%d/%s' % (eng, subj, W, PLACES[0]))
                                R(eng, 'B-6 %s %dpx 가로 넘침 0 — 식 칸 · 패널·창 · 식이 창 밖(절대) · 카드 · 쪽(바탕에 없던 새 넘침)' % (sj, W), okn, j_over(rb)[0] if bok else None, vn)
                                okn, vn = j_kink(rn)
                                R(eng, 'B-6 %s %dpx √ 위 줄과 꺾임 맞닿음(자리 다섯의 √ 마다 · 식 표본 ≥ 1)' % (sj, W), okn, j_kink(rb)[0] if bok else None, vn)
                                okn, vn = j_wrap(rn)
                                if W == 390:
                                    R(eng, 'B-6 %s %dpx 폰 줄바꿈 됨 — 펼친 근거 · 연결 상자가 두 줄 이상 · 가로로 안 넘침' % (sj, W), bool(okn) and j_over(rn, (rb if bok else None) if QC.GATE else _rg_ob)[0],
                                      (bool(j_wrap(rb)[0]) and j_over(rb)[0]) if bok else None, vn)
                                else:
                                    R(eng, 'B-6 %s %dpx 줄 수(참고)' % (sj, W), None, None, vn)
                            if do_b7 and eng == 'chromium' and W in (1440, 390):
                                for nm, fn in (('겹침 0 — 식과 이웃 글 · 맨 위 요소(elementsFromPoint) · 식 표본 ≥ 1', j_overlap), ('잘림 0 — 식이 패널·창 안 · √ 선이 식 높이만큼', j_clip), ('글자 크기 어긋남 0 — 분수 .86 · √ · 첨자 배율', j_font)):
                                    okn, vn = fn(rn)
                                    R(eng, 'B-7 %s %dpx %s' % (sj, W, nm), okn, fn(rb)[0] if bok else None, vn)
            finally:
                br.close()
    if shots:
        R('-', 'B-7 그림 %d장 — 자리 다섯 × 폭 × 과목(사람이 눈으로 보는 것 · 게이트 아님 · 사용자 확인 거리)' % len(shots), None, None, {'폴더': CAP, '예': [os.path.basename(x) for x in shots[:4]]})


def _fin(t0):
    """끝 — 합계 · 결과 파일에 덧붙임(앞 실행 것은 안 지움) · 종료 코드"""
    npass = sum(1 for r in ROWS if r[2] is True); nfail = sum(1 for r in ROWS if r[2] is False)
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    try:
        newrev = git('rev-parse', '--short', 'HEAD').decode('utf-8', 'replace').strip()
        spdrev = JG.git_HU(SPD, 'rev-parse', '--short', 'HEAD').decode('utf-8', 'replace').strip()
    except Exception:
        newrev = spdrev = '?'
    with io.open(OUTF, 'a', encoding='utf-8') as fo:
        fo.write('\n==== %s · jagwa_ggmath GM · 새 판 %s(HEAD %s · md5 %s) · 바탕 %s(md5 %s) · studyplandata HEAD %s · 엔진 %s%s · 묶음 %s ====\n' % (
            time.strftime('%Y-%m-%d %H:%M'), os.path.basename(ROOT), newrev, hashlib.md5(APPS['NEW']).hexdigest()[:8] if APPS.get('NEW') else '-', BASE,
            hashlib.md5(APPS['BASE']).hexdigest()[:8] if APPS.get('BASE') else '-', spdrev, ','.join(ENGS), ' · text-only' if TEXT_ONLY else '', ','.join(ONLY) or '전부'))
        for eng, nm, okn, okb, v in ROWS:
            fo.write('%s | 바탕 %s | %s · %s | %s\n' % ({True: 'PASS', False: 'FAIL', None: 'INFO'}[okn], {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, nm, vs(v, 1200)))
        fo.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    shutil.rmtree(WORKD, ignore_errors=True)
    sys.exit(1 if nfail else 0)


def main():
    t0 = time.time()
    if NODE is None:
        R('node', 'node 실행 파일 없음 — node 칸 못 돎', False, None, 'PATH 의 node 도 파이썬 playwright 가 싣고 온 node 도 못 찾음')
    else:
        load_apps()
        if not APPS['NEW'] or (QC.GATE and not APPS['BASE']):   # regress — 바탕 앱 안 읽음(빈 글)
            R('node', 'B0 앱 읽기 실패 — 새 판 %d B · 바탕 %s %d B' % (len(APPS['NEW']), BASE, len(APPS['BASE'])), False, None, ROOT)
            _fin(t0)
        print('새 판 = %s (LF %d B) · 바탕 = %s (%d B) · studyplandata = %s' % (ROOT, len(APPS['NEW']), BASE, len(APPS['BASE']), SPD), flush=True)
        if not QC.SMOKE:   # smoke — node 칸(B0 ~ B3 글자)은 smoke 칸이 아님 · 브라우저 장면 하나만
            b0()
            if want('B1'):
                b1()
            if want('B2'):
                b2()
            if want('B3'):
                b3_text()
        if TEXT_ONLY:
            pass
        elif any(want(g) for g in ('B3', 'B4', 'B5', 'B6', 'B7')):
            run_browser()
    _fin(t0)


if __name__ == '__main__':
    main()
