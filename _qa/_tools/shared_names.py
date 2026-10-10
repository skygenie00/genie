# -*- coding: utf-8 -*-
"""앱 공용 층 이름표 — _task_qa_bigguard_1010 §B (2026-10-10)

  python shared_names.py [--rev <genie 커밋>] [--apps jo,jagwa,…] [--write]
        GENIE_ROOT(없으면 본 폴더)의 앱 파일(--rev 면 그 커밋 blob)에서 공용 층 함수를 뽑아 찍는다 · --write = 옆 shared_names.json 에 씀

  공용 층 = 앱 인라인 <script> 의 이름 있는 함수 가운데
    ① 부르는 자리 ≥ 3 (주석 밖 「이름(」 — 인라인 on…="이름(" · 글자로 지은 HTML 안 부름 포함 · 「.이름(」 메서드 · 정의 자리 뺌)
    ② 몸에 localStorage · indexedDB · fetch( · 'PUT' 이 든 함수(주석 밖 · 안에 든 함수 몸 포함)
  _qa_chain.py compare --affected 가 이 표로 「공용 층을 건드린 판」을 가른다(그 판이면 앱 전체 · 아니면 건드린 하네스만).
  JSON 칸: apps.<앱> = {file, md5(LF 바이트), rev, funcs, shared: {이름: 까닭}} — 실행기는 바탕 앱 md5 가 같으면 이 표를 · 다르면 같은 규칙으로 바탕에서 다시 뽑는다.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(HERE, 'shared_names.json')
APP_FILE = {'jo': 'jo/index.html', 'jagwa': 'jagwa/index.html', 'minbeop': 'minbeop/index.html', 'timetable': 'timetable/index.html',
            'gichul': 'gichul/index.html', 'chem': 'chem/index.html'}
CALLS_MIN = 3
TOOL_MAX = 240   # 도구 함수 몸 글자 수 위 끝
STORE_RX = re.compile(r'\b(?:localStorage|sessionStorage|indexedDB)\b|\.transaction\s*\(|\bobjectStore\b|\bfetch\s*\(|[\'"]PUT[\'"]')   # indexedDB = .transaction( · objectStore 도(IDB 래퍼)
KW = {'if', 'for', 'while', 'switch', 'catch', 'return', 'function', 'typeof', 'new', 'delete', 'void', 'in', 'of', 'do', 'else', 'case',
      'try', 'finally', 'throw', 'await', 'yield', 'async', 'const', 'let', 'var', 'class', 'super', 'this', 'import', 'export', 'with'}
RE_KW = {'return', 'typeof', 'case', 'do', 'else', 'in', 'of', 'new', 'delete', 'void', 'throw', 'instanceof', 'yield', 'await'}
RX_SCRIPT = re.compile(r'<script\b([^>]*)>', re.I)
RX_STYLE = re.compile(r'<style\b[^>]*>', re.I)
RX_JUMP = re.compile(r'[\'"`/{}]')
RX_ID = r'[A-Za-z_$][\w$]*'
RX_FN_DECL = re.compile(r'\bfunction\b\s*\*?\s*(' + RX_ID + r')\s*\(')
RX_FN_ASSIGN = re.compile(r'(?<![\w$.])(?:(?:window|self|globalThis)\.)?(' + RX_ID + r')\s*=\s*(?:async\s+)?function\b\s*\*?\s*[\w$]*\s*\(')
RX_FN_ARROW = re.compile(r'(?<![\w$.])(?:(?:window|self|globalThis)\.)?(' + RX_ID + r')\s*=\s*(?:async\s*)?(\([^()]*(?:\([^()]*\)[^()]*)*\)|' + RX_ID + r')\s*=>')
RX_IDENT_ALL = re.compile(RX_ID)
RX_ASG = re.compile(r'(?<![\w$.])([A-Za-z_$][\w$]*)(?:\s*(?:\.[\w$]+|\[[^\]\n]*\]))*\s*(?:=(?![=>])|\+=|-=|\*=|/=|\|\|=|&&=|\?\?=|\+\+|--)')
RX_PREINC = re.compile(r'(?:\+\+|--)\s*([A-Za-z_$][\w$]*)')
RX_MUT = re.compile(r'(?<![\w$.])([A-Za-z_$][\w$]*)(?:\.[\w$]+|\[[^\]\n]*\])*\.(?:push|pop|shift|unshift|splice|set|add|delete|clear|sort|reverse|fill|copyWithin)\s*\(|\bdelete\s+([A-Za-z_$][\w$]*)')
RX_ALIAS = re.compile(r'(?<![\w$.])(?:(?:const|let|var)\s+)?([A-Za-z_$][\w$]*)\s*=\s*([A-Za-z_$][\w$]*)\s*(?=[;,\n)])')
RX_CALL = re.compile(r'(?<![\w$.])(' + RX_ID + r')\s*\(')
RX_DECL_ONLY = re.compile(r'\bfunction\b\s*\*?\s*(' + RX_ID + r')\s*\(')


def lf(t):
    return t.replace('\r\n', '\n')


def regions(html):
    """인라인 <script>(src 없음 · JSON · 템플릿 꼴 빼고) 와 <style> 몸 자리 [(a, b)]"""
    js, css = [], []
    pos = 0
    while True:   # 스크립트 안 글자 「<script」(HTML 을 짓는 글)는 건넘 — 다음 찾기는 그 스크립트 끝 뒤부터
        m = RX_SCRIPT.search(html, pos)
        if not m:
            break
        attrs = m.group(1).lower()
        e = html.find('</script', m.end())
        e = len(html) if e < 0 else e
        pos = e + 1
        if 'src=' in attrs or re.search(r'type\s*=\s*["\']?(?:application/(?:ld\+)?json|text/(?:template|html|plain))', attrs):
            continue
        js.append((m.end(), e))
    for m in RX_STYLE.finditer(html):
        if any(a <= m.start() < b for a, b in js):
            continue
        e = html.find('</style', m.end())
        css.append((m.end(), len(html) if e < 0 else e))
    return js, css


def _prev_sig(s, j, a):
    p = j - 1
    while p >= a and s[p] in ' \t\r\n':
        p -= 1
    if p < a:
        return '', ''
    ch = s[p]
    if ch.isalnum() or ch in '_$':
        q = p
        while q >= a and (s[q].isalnum() or s[q] in '_$'):
            q -= 1
        return ch, s[q + 1:p + 1]
    return ch, ''


def scan_js(s, a, b):
    """JS 한 덩이 — 코드 밖 자리(글자 's' · 주석 'c' · 정규식 'r' · 템플릿 글 't') 와 코드 { } 짝"""
    spans, pairs, stack = [], {}, []
    i = a

    def tmpl(st):
        """템플릿 글(st = 여는 ` 또는 식을 닫는 } 자리) — 끝 ` 뒤 자리 또는 ${ 뒤 자리(스택에 ${ 넣음)"""
        k = st + 1
        while k < b:
            c = s[k]
            if c == '\\':
                k += 2
                continue
            if c == '`':
                spans.append((st, k + 1, 't'))
                return k + 1
            if c == '$' and k + 1 < b and s[k + 1] == '{':
                spans.append((st, k + 2, 't'))
                stack.append(('${', k + 1))
                return k + 2
            k += 1
        spans.append((st, b, 't'))
        return b

    while i < b:
        m = RX_JUMP.search(s, i, b)
        if not m:
            break
        j = m.start()
        ch = s[j]
        if ch in '\'"':
            k = j + 1
            while k < b:
                c = s[k]
                if c == '\\':
                    k += 2
                    continue
                if c == ch or c == '\n':
                    break
                k += 1
            spans.append((j, min(k + 1, b), 's'))
            i = k + 1
        elif ch == '`':
            i = tmpl(j)
        elif ch == '{':
            stack.append(('{', j))
            i = j + 1
        elif ch == '}':
            if stack:
                kind, op = stack.pop()
                if kind == '${':
                    i = tmpl(j)   # } 가 템플릿 식을 닫음 — 다시 템플릿 글
                    continue
                pairs[op] = j
            i = j + 1
        else:   # '/'
            nx = s[j + 1] if j + 1 < b else ''
            if nx == '/':
                e = s.find('\n', j)
                e = b if e < 0 or e > b else e
                spans.append((j, e, 'c'))
                i = e
            elif nx == '*':
                e = s.find('*/', j + 2)
                e = b if e < 0 or e + 2 > b else e + 2
                spans.append((j, e, 'c'))
                i = e
            else:
                pc, pw = _prev_sig(s, j, a)
                is_re = pc == '' or pc in '(,=:[!&|?{};+-*%<>~^}' or (pw and pw in RE_KW)
                if not is_re:
                    i = j + 1
                    continue
                k, cls = j + 1, False
                while k < b:
                    c = s[k]
                    if c == '\\':
                        k += 2
                        continue
                    if c == '\n':
                        break
                    if cls:
                        cls = c != ']'
                    elif c == '[':
                        cls = True
                    elif c == '/':
                        break
                    k += 1
                k += 1
                while k < b and (s[k].isalpha()):
                    k += 1
                spans.append((j, min(k, b), 'r'))
                i = k
    return spans, pairs


def blank(s, spans, kinds):
    """spans 가운데 kinds 자리를 빈칸으로(줄바꿈은 둠 · 자리 그대로)"""
    out, last = [], 0
    for x, y, k in sorted(spans):
        if k not in kinds or y <= last or y <= x:
            continue
        x = max(x, last)
        out.append(s[last:x])
        out.append(re.sub(r'[^\n]', ' ', s[x:y]))
        last = y
    out.append(s[last:])
    return ''.join(out)


def _match_paren(code, p):
    d = 0
    for k in range(p, min(len(code), p + 4000)):
        c = code[k]
        if c == '(':
            d += 1
        elif c == ')':
            d -= 1
            if d == 0:
                return k
    return -1


def _expr_end(code, p, lim):
    d = 0
    for k in range(p, min(lim, p + 20000)):
        c = code[k]
        if c in '([{':
            d += 1
        elif c in ')]}':
            if d == 0:
                return k
            d -= 1
        elif d == 0 and c in ';,\n':
            return k
    return min(lim, p + 20000)


class Model:
    """앱 HTML 한 판 — 코드 보기(글자 · 주석 가림) · 함수(이름 · 몸 자리) · 부르는 자리 · 저장 API"""

    def __init__(self, html):
        self.html = html = lf(html)
        self.js, self.css = regions(html)
        spans, pairs = [], {}
        for a, b in self.js:
            sp, pr = scan_js(html, a, b)
            spans += sp
            pairs.update(pr)
        self.spans = spans
        self.pairs = pairs
        code = blank(html, spans, 'scrt')          # 코드만(글자 · 주석 · 정규식 · 템플릿 글 가림)
        nocom = blank(html, spans, 'c')           # 주석만 가림(인라인 부름 글자는 남김)
        # 스크립트 밖(마크업 · 스타일)은 코드 보기에서 가림 · 주석 보기에서는 HTML 주석만 가림
        outside = []
        last = 0
        for a, b in self.js:
            outside.append((last, a))
            last = b
        outside.append((last, len(html)))
        self.code = blank(code, [(x, y, 'o') for x, y in outside], 'o')
        hc = [(m.start(), m.end(), 'h') for m in re.finditer(r'<!--.*?-->', html, re.S) if not any(a <= m.start() < b for a, b in self.js)]
        self.nocom = blank(nocom, hc, 'h')
        self.funcs = self._funcs()
        self._scope()
        self.alias = {}                                               # 다른 이름(var putRaw=put) → 원래 이름
        tops = {f['name'] for f in self.funcs if f['parent'] is None}
        for m in RX_ALIAS.finditer(self.code):
            a, b0 = m.group(1), m.group(2)
            if a != b0 and b0 in tops and a not in KW and not any(a <= m.start() and False for a in ()):
                if not any(f['a'] <= m.start() <= f['b'] for f in self.funcs if f['b'] - f['a'] < 200000 and f['parent'] is None and False):
                    self.alias.setdefault(a, b0)
        self.names = {f['name'] for f in self.funcs}                 # 맨 이름(하네스 글자 고르기)
        self.ids = {f['id'] for f in self.funcs}                     # 자리 이름(안쪽 함수 = 바깥>안)
        cnt = Counter(m.group(1) for m in RX_CALL.finditer(self.nocom))
        dec = Counter(m.group(1) for m in RX_DECL_ONLY.finditer(self.code))
        self.calls, self.store = {}, {}
        nested = {f['name'] for f in self.funcs if f['parent'] is not None}
        for f in self.funcs:
            if f['parent'] is None:
                c = cnt.get(f['name'], 0) - dec.get(f['name'], 0)
                if f['name'] in nested:   # 같은 이름 안쪽 함수가 가린 부름은 뺀다(그 자리에서 이 이름 = 안쪽 함수)
                    rx = re.compile(r'(?<![\w$.])' + re.escape(f['name']) + r'\s*\(')
                    c = sum(1 for m in rx.finditer(self.nocom) if self.resolve(f['name'], m.start()) == f['name']) - dec.get(f['name'], 0)
            else:   # 안쪽 함수 — 바깥 함수 몸 안에서만 셈(같은 이름 지역 함수 draw · row … 가 한 이름으로 뭉치지 않게)
                p = f['parent']
                rx = re.compile(r'(?<![\w$.])' + re.escape(f['name']) + r'\s*\(')
                c = len(rx.findall(self.nocom, p['a'], p['b'] + 1)) - len(re.findall(r'\bfunction\b\s*\*?\s*' + re.escape(f['name']) + r'\s*\(', self.code[p['a']:p['b'] + 1]))
            self.calls[f['id']] = max(self.calls.get(f['id'], 0), c)
            body = self.nocom[f['a']:f['b'] + 1]
            ks = sorted({re.sub(r'^\.|\s*\($', '', k.group(0).strip("'\"")) for k in STORE_RX.finditer(body)})
            if ks:
                self.store.setdefault(f['id'], set()).update(ks)
        for a, b0 in self.alias.items():
            if a in self.ids:
                continue
            self.calls[a] = cnt.get(a, 0)
            if b0 in self.store:
                self.store[a] = set(self.store[b0])
        self.shared = {}
        for n in sorted(self.ids | set(self.alias)):
            why = []
            if self.calls.get(n, 0) >= CALLS_MIN:
                why.append('부름 %d' % self.calls[n])
            if n in self.store:
                why.append('저장 ' + '·'.join(sorted(self.store[n])))
            if why:
                self.shared[n] = ' · '.join(why)
        self.tools = self._tools()
        self._lines = None

    def _tools(self):
        """도구 함수 — 공용(부름 ≥ 3) 가운데 앱 상태를 안 만지는 작은 함수: 맨 위 · 저장 API 없음 · 몸 ≤ TOOL_MAX 자 ·
           부르는 앱 함수가 도구뿐 · 바깥 이름에 = 안 함($ · esc · toast 꼴) — 바뀐 줄이 「부르기만」 하면 공용 층을 건드린 것으로 안 셈(몸을 고치면 셈)"""
        cand, bad = {}, set()
        for f in self.funcs:
            if f['parent'] is not None or f['id'] not in self.shared or f['id'] in self.store or f['b'] - f['a'] > TOOL_MAX:
                bad.add(f['id'])
                continue
            body = self.code[f['a']:f['b'] + 1]
            head = self.code[f['at']:f['a']]
            local = set(RX_IDENT_ALL.findall(head)) | set(re.findall(r'\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)', body))
            local |= set(re.findall(r'(?<![\w$.])([A-Za-z_$][\w$]*)\s*=>', body)) | {x for g in re.findall(r'\(([^()]*)\)\s*=>', body) for x in RX_IDENT_ALL.findall(g)}
            asg = {m.group(1) for m in RX_ASG.finditer(body)} | {m.group(1) for m in RX_PREINC.finditer(body)} | {m.group(1) for m in RX_MUT.finditer(body)}
            if asg - local:   # 바깥 이름(전역 값 · 전역 객체 칸 · 전역 배열 push …)을 바꿈 = 앱 상태를 만짐
                bad.add(f['id'])
                continue
            calls = {m.group(1) for m in RX_CALL.finditer(body)} & (self.top | set(self.alias))
            cand[f['id']] = cand.get(f['id'], set()) | (calls - {f['name']})
        for n in bad | set(self.alias):   # 정의가 여럿이면(감싼 판 · 빈 판) 모두 걸러져야 도구 · 다른 이름(alias)은 도구 아님
            cand.pop(n, None)
        tools = set()
        ch = True
        while ch:
            ch = False
            for n, cs in cand.items():
                if n not in tools and cs <= tools:
                    tools.add(n)
                    ch = True
        return tools

    def _scope(self):
        """함수마다 바깥 함수(정의 자리를 몸에 품은 가장 안쪽 함수) · 자리 이름 id"""
        fs = sorted(self.funcs, key=lambda f: (f['a'], -f['b']))
        stack = []
        for f in fs:
            while stack and stack[-1]['b'] < f['at']:
                stack.pop()
            par = None
            for g in reversed(stack):
                if g['a'] <= f['at'] <= g['b'] and g is not f:
                    par = g
                    break
            f['parent'] = par
            f['id'] = (par['id'] + '>' + f['name']) if par else f['name']
            stack.append(f)
        self.top = {f['name'] for f in self.funcs if f['parent'] is None}

    def _funcs(self):
        code, out = self.code, []
        for m in RX_FN_DECL.finditer(code):
            p = _match_paren(code, m.end() - 1)
            if p < 0:
                continue
            q = code.find('{', p)
            if q >= 0 and q in self.pairs and not code[p + 1:q].strip():
                out.append({'name': m.group(1), 'at': m.start(), 'a': q, 'b': self.pairs[q]})
        for m in RX_FN_ASSIGN.finditer(code):
            if m.group(1) in KW:
                continue
            p = _match_paren(code, m.end() - 1)
            q = code.find('{', p) if p >= 0 else -1
            if q >= 0 and q in self.pairs and not code[p + 1:q].strip():
                out.append({'name': m.group(1), 'at': m.start(), 'a': q, 'b': self.pairs[q]})
        for m in RX_FN_ARROW.finditer(code):
            if m.group(1) in KW:
                continue
            k = m.end()
            while k < len(code) and code[k] in ' \t\r\n':
                k += 1
            if k < len(code) and code[k] == '{' and k in self.pairs:
                out.append({'name': m.group(1), 'at': m.start(), 'a': k, 'b': self.pairs[k]})
            else:
                lim = next((b for a, b in self.js if a <= k < b), len(code))
                out.append({'name': m.group(1), 'at': m.start(), 'a': k, 'b': max(k, _expr_end(code, k, lim) - 1)})
        out.sort(key=lambda f: (f['a'], -f['b']))
        return out

    # ── 줄 · 자리 ──
    def line_starts(self):
        if self._lines is None:
            self._lines = [0] + [m.end() for m in re.finditer(r'\n', self.html)]
        return self._lines

    def line_span(self, ln):
        """1 부터 센 줄 → (a, b) 글자 자리"""
        ls = self.line_starts()
        if ln < 1 or ln > len(ls):
            return None
        a = ls[ln - 1]
        b = ls[ln] - 1 if ln < len(ls) else len(self.html)
        return a, b

    def where(self, pos):
        if any(a <= pos < b for a, b in self.js):
            return 'js'
        if any(a <= pos < b for a, b in self.css):
            return 'css'
        return 'html'

    def chain(self, pos):
        """pos 를 몸에 품은 이름 있는 함수들(안쪽 → 바깥) — [함수 dict]"""
        fs = [f for f in self.funcs if f['a'] <= pos <= f['b']]
        fs.sort(key=lambda f: f['b'] - f['a'])
        return fs

    def overlapping(self, a, b):
        """글자 자리 a..b(한 줄)와 겹치는 이름 있는 함수(정의 머리 ~ 몸 끝) — 그 줄에서 정의된 한 줄 함수(var f=x=>…)도 듦 · 안쪽 → 바깥"""
        fs = [f for f in self.funcs if f['at'] <= b and f['b'] >= a]
        fs.sort(key=lambda f: f['b'] - f['at'])
        return fs

    def enclosing(self, pos):
        """pos 를 몸에 품은 이름 있는 함수 가운데 가장 안쪽의 자리 이름(없으면 None)"""
        fs = self.chain(pos)
        return fs[0]['id'] if fs else None

    def resolve(self, name, pos):
        """pos 에서 부른 이름 → 자리 이름(둘레 함수의 안쪽 함수 먼저 · 다음 맨 위 함수 · 없으면 None)"""
        for g in self.chain(pos):
            cid = g['id'] + '>' + name
            if cid in self.ids:
                return cid
        return name if name in self.top else None


def md5_lf(text):
    return hashlib.md5(lf(text).encode('utf-8')).hexdigest()


def extract(html):
    m = Model(html)
    return {'md5': md5_lf(html), 'funcs': len(m.ids), 'rule': '부르는 자리 ≥ %d · 몸에 localStorage/indexedDB/fetch/PUT(안쪽 함수 = 바깥>안 · 바깥 몸 안에서 셈)' % CALLS_MIN,
            'shared': m.shared, 'tools': sorted(m.tools)}


def _git(repo, *a):
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    if r.returncode:
        raise SystemExit('NG git %s: %s' % (' '.join(a), r.stderr.decode('utf-8', 'replace')[:300]))
    return r.stdout


def main(av):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    root = os.environ.get('GENIE_ROOT') or os.path.join(os.path.expanduser('~'), 'Documents', 'genie')
    rev = av[av.index('--rev') + 1] if '--rev' in av else None
    apps = av[av.index('--apps') + 1].split(',') if '--apps' in av else list(APP_FILE)
    old = {}
    try:
        with open(JSON_PATH, encoding='utf-8') as f:
            old = json.load(f)
    except FileNotFoundError:
        pass
    out = {'v': 1, 'about': '앱 공용 층 이름표(_tools/shared_names.py 가 뽑음 · 손으로 고치지 말 것) — _qa_chain.py compare --affected 가 씀',
           'made': '', 'rev': '', 'apps': dict(old.get('apps') or {})}
    head = (rev or _git(root, 'rev-parse', 'HEAD').decode().strip())
    for app in apps:
        p = APP_FILE[app]
        if rev:
            try:
                html = _git(root, 'show', '%s:%s' % (rev, p)).decode('utf-8', 'replace')
            except SystemExit:
                continue
        else:
            fp = os.path.join(root, *p.split('/'))
            if not os.path.isfile(fp):
                continue
            html = open(fp, 'rb').read().decode('utf-8', 'replace')
        e = extract(html)
        e['file'] = p
        out['apps'][app] = e
        print('%-9s 함수 %4d · 공용 %4d(부름 ≥ %d · 저장 API) · md5 %s' % (app, e['funcs'], len(e['shared']), CALLS_MIN, e['md5'][:8]))
    out['rev'] = _git(root, 'rev-parse', head).decode().strip() if head else ''
    out['made'] = '%s · genie %s' % (__import__('time').strftime('%Y-%m-%d %H:%M'), out['rev'][:7])
    if '--write' in av:
        with open(JSON_PATH, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=False) + '\n')
        print('씀', JSON_PATH)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
