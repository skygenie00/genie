# -*- coding: utf-8 -*-
"""건드린 하네스만 — _task_qa_bigguard_1010 §B (2026-10-10) · _qa_chain.py compare/plan 이 부른다

  판 둘(바탕 → 새 판)의 diff 에서
    · 앱 파일(<앱>/index.html): 바뀐 줄(주석만 바뀐 덩이는 뺌)이 든 이름 있는 함수(가장 안쪽) · 그 줄이 부르는 앱 함수 ·
      CSS 규칙 선택자(그 규칙 통째 글자) · id(id="…" · '#…' · getElementById) · 글자 상수(기록 열쇠 꼴 — 빈칸 없는 4자 넘는 글자)
    · 앱 밖 파일: 그 길(genie:<길> · _qa/<길> → n:<길>)
  공용 층(shared_names — 부르는 자리 ≥ 3 · localStorage/indexedDB/fetch/PUT 든 함수)에 바뀐 함수·부르는 함수가 들면 → 그 앱 전체(까닭 = 그 이름)
  아니면 → 하네스 소스(+ 입력에 든 로컬 모듈 .py)에 그 글자가 든 하네스 · 입력(전수표 inputs)에 그 길·글자가 든 하네스 ·
          그 판이 바꾼 하네스(판 관문) · 태그 smoke 하나(가장 짧은 것 · 여기서 돌 수 있는 것 먼저)
"""
import json
import os
import re
import subprocess

import shared_names as SN

HERE = os.path.dirname(os.path.abspath(__file__))
# 흔한 글자(고르기에 안 씀) — 하네스 대부분에 드는 낱말 · DOM · 이벤트 이름
STOP = set('''
true false null undefined function return const this that self window document style class click change input value
checked hidden block none flex inline absolute relative fixed auto left right top bottom width height color background
border margin padding display position content length string number object boolean index items item text html body head
span div button label select option textarea canvas image img path data json name type title open close show hide active
active disabled selected focus blur keydown keyup pointerdown pointerup pointermove touchstart touchend touchmove mousedown
mouseup mousemove scroll resize load error then catch finally async await push slice splice filter map forEach reduce
join split replace trim toString parseInt parseFloat Math Date JSON Object Array String Number Promise Set Map
querySelector querySelectorAll getElementById addEventListener removeEventListener classList toggle contains add remove
innerHTML textContent setAttribute getAttribute dataset appendChild insertBefore createElement preventDefault stopPropagation
utf-8 GET POST PUT DELETE http https localhost
'''.split())
RX_STR = re.compile(r'''(['"])((?:\\.|(?!\1).)*)\1''')
RX_IDENT = re.compile(r'[A-Za-z_$][\w$]*')
RX_HTML_ID = re.compile(r'''\bid\s*=\s*\\?["']([^"'\\\s<>]+)''')
RX_HTML_CLASS = re.compile(r'''\bclass\s*=\s*\\?["']([^"'\\<>]+)''')
RX_ON_ATTR = re.compile(r'''\bon[a-z]+\s*=\s*\\?["']\s*([A-Za-z_$][\w$]*)\s*\(''')


def git(repo, *a, check=True):
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    if check and r.returncode:
        raise SystemExit('NG git %s: %s' % (' '.join(a), r.stderr.decode('utf-8', 'replace')[:300]))
    return r.stdout.decode('utf-8', 'replace')


# ── 판 둘의 diff ─────────────────────────────────────────────────────────────────────────────
def changed(bctx, nctx):
    """[(상태, 길)] — 새 판이 root(작업 자리)면 안 커밋한 고침 · 안 올린 새 파일까지"""
    if nctx.rev:
        out = git(bctx.repo, 'diff', '--no-renames', '--name-status', '-z', bctx.head, nctx.head)
    else:
        out = git(nctx.root, 'diff', '--no-renames', '--name-status', '-z', bctx.head)
    xs = [x for x in out.split('\0') if x != '']
    res = [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
    if not nctx.rev:
        for ent in git(nctx.root, 'status', '--porcelain', '-z', '--untracked-files=all').split('\0'):
            if ent.startswith('?? '):
                res.append(('A', ent[3:]))
    return res


def hunks(bctx, nctx, path):
    """[(옛 줄 a, 옛 줄 수, 새 줄 a, 새 줄 수)] — git diff -U0"""
    if nctx.rev:
        out = git(bctx.repo, 'diff', '-U0', '--no-color', bctx.head, nctx.head, '--', path)
    else:
        out = git(nctx.root, 'diff', '-U0', '--no-color', bctx.head, '--', path)
    res = []
    for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', out, re.M):
        res.append((int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)))
    return res


def text_at(ctx, path):
    if ctx.rev:
        r = subprocess.run(['git', '-C', ctx.repo, 'show', '%s:%s' % (ctx.head, path)], capture_output=True)
        return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else ''
    fp = os.path.join(ctx.root, *path.split('/'))
    return open(fp, 'rb').read().decode('utf-8', 'replace') if os.path.isfile(fp) else ''


# ── 공용 층 이름표 ───────────────────────────────────────────────────────────────────────────
def shared_for(app, html, model=None):
    """(공용 {자리 이름: 까닭}, 도구 {이름}, 출처 글) — shared_names.json 의 그 앱 md5 가 같으면 그 표 · 아니면 같은 규칙으로 이 판에서 다시 뽑음"""
    md5 = SN.md5_lf(html)
    try:
        with open(SN.JSON_PATH, encoding='utf-8') as f:
            tab = (json.load(f).get('apps') or {}).get(app) or {}
    except (OSError, ValueError):
        tab = {}
    if tab.get('md5') == md5:
        return tab.get('shared') or {}, set(tab.get('tools') or []), 'shared_names.json(%s)' % md5[:8]
    m = model or SN.Model(html)
    return m.shared, set(m.tools), '바탕 판에서 다시 뽑음(%s · json 은 %s)' % (md5[:8], (tab.get('md5') or '없음')[:8])


# ── 앱 파일 diff 읽기 ─────────────────────────────────────────────────────────────────────────
def _lines(model, a, n):
    """줄 a 부터 n 줄 — [(줄 번호, 자리 a, 자리 b)]"""
    out = []
    for ln in range(a, a + n):
        sp = model.line_span(ln)
        if sp:
            out.append((ln,) + sp)
    return out


def _css_selectors(html, a, b, lo):
    """CSS 한 줄(a..b)의 규칙 선택자들 — 그 줄에 규칙 머리({)가 있으면 그 앞 글자 · 없으면(여러 줄 규칙의 선언 줄) 품은 규칙 머리 · @ 머리(@media …)는 뺌"""
    line = re.sub(r'/\*.*?\*/', lambda m: ' ' * len(m.group(0)), html[a:b])
    out = []
    if '{' in line:
        last = 0
        for m in re.finditer(r'[{}]', line):
            if m.group(0) == '{':
                sel = line[last:m.start()].strip()
                if sel and not sel.startswith('@'):
                    out.append(sel)
            last = m.end()
        return out
    depth, k = 0, a
    while k > lo:   # 품은 규칙의 { 까지 뒤로(닫힌 { } 짝은 건넘)
        c = html[k - 1]
        if c == '}':
            depth += 1
        elif c == '{':
            if depth == 0:
                break
            depth -= 1
        k -= 1
    if k <= lo:
        return out
    s0 = max(html.rfind('}', lo, k - 1), html.rfind('{', lo, k - 1), html.rfind('*/', lo, k - 1) + 1, lo - 1) + 1
    sel = re.sub(r'/\*.*?\*/', ' ', html[s0:k - 1], flags=re.S).strip()
    if sel and not sel.startswith('@'):
        out.append(sel)
    return out


def _norm_sel(s):
    s = re.sub(r'/\*.*?\*/', ' ', s, flags=re.S)
    return [re.sub(r'\s+', ' ', re.sub(r'\s*([>+~])\s*', r' \1 ', x)).strip() for x in s.split(',') if x.strip()]


def _distinct(tok):
    """고르기에 쓸 만한 글자 — 4자 넘고 흔한 낱말 아님 · 숫자 · 대문자(낙타) · _ · : · - · / · . · 한글이 들거나 7자 넘음"""
    if len(tok) < 4 or tok in STOP or tok.lower() in STOP:
        return False
    if re.fullmatch(r'\d+(\.\d+)?', tok):
        return False
    if re.search(r'[0-9_:/.\-가-힣]', tok) or re.search(r'[a-z][A-Z]', tok) or len(tok) >= 7:
        return True
    return False


def analyze_app(app, path, old, new, hk):
    """앱 파일 하나의 diff → {touched: {자리 이름: 까닭}, refs: [자리 이름], tokens: {글자: 갈래}, shared_hit: {이름: 까닭}, src, notes}
       touched = 바뀐 줄을 몸에 품은 이름 있는 함수 전부(안쪽 → 바깥 · 안쪽 함수가 바뀌면 그 바깥 함수도 바뀐 것)
       refs    = 바뀐 줄이 부르거나 가리키는 앱 함수(도구 함수 $ · esc · toast … 는 공용 판정에서 뺌 — 몸을 고친 판만 셈)"""
    mo, mn = SN.Model(old), SN.Model(new)
    sh_o, tl_o, src = shared_for(app, old, mo)
    shared = dict(mn.shared)
    shared.update(sh_o)
    tools = (tl_o | set(mn.tools)) - {k for k in shared if k not in tl_o and k not in mn.tools}
    touched, refs, tokens, notes = {}, set(), {}, []
    css_n = 0
    for (oa, on, na, nn) in hk:
        olines = _lines(mo, oa, on) if on else []
        nlines = _lines(mn, na, nn) if nn else []
        # 주석만 바뀐 덩이 — 주석 가린 보기가 같으면 건넘
        o_code = ''.join(mo.nocom[a:b] for _, a, b in olines)
        n_code = ''.join(mn.nocom[a:b] for _, a, b in nlines)
        if re.sub(r'\s+', '', o_code) == re.sub(r'\s+', '', n_code):
            notes.append('주석만 %d~%d' % (na, na + max(nn, 1) - 1))
            continue
        for model, lines in ((mo, olines), (mn, nlines)):
            for ln, a, b in lines:
                w = model.where(a)
                if w == 'js':
                    for f in model.overlapping(a, b):
                        touched.setdefault(f['id'], '몸 %d줄' % ln)
                    keep = model.nocom[a:b]
                    code = model.code[a:b]
                    seen = set()
                    for m in list(SN.RX_CALL.finditer(keep)) + list(RX_IDENT.finditer(code)):
                        nm = m.group(1) if m.re is SN.RX_CALL else m.group(0)
                        if nm in seen:
                            continue
                        seen.add(nm)
                        rid = model.resolve(nm, a + m.start())
                        if rid is None and nm in model.alias:
                            rid = nm
                        if rid:
                            refs.add(rid)
                    for m in RX_STR.finditer(model.html[a:b]):
                        _str_tokens(m.group(2), tokens)
                    _html_tokens(model.html[a:b], tokens)
                elif w == 'css':
                    lo, hi = next((x, y) for x, y in model.css if x <= a < y)
                    if not re.sub(r'/\*.*?\*/', '', model.html[a:b]).strip():
                        continue
                    for sel in _css_selectors(model.html, a, b, lo):
                        for x in _norm_sel(sel):
                            tokens.setdefault(x, 'css')
                            css_n += 1
                else:
                    _html_tokens(model.html[a:b], tokens)
    hit = {}
    for f, why in touched.items():
        if f in shared:
            hit[f] = '바뀐 함수(%s) · %s' % (why, shared[f])
    for f in sorted(refs):
        if f in shared and f not in hit and f not in tools:
            hit[f] = '바뀐 줄이 부름 · %s' % shared[f]
    leaf = lambda i: i.split('>')[-1]
    for f in touched:
        if _distinct(leaf(f)) or len(leaf(f)) >= 4:
            tokens.setdefault(leaf(f), 'fn')
    for f in refs:
        if f not in shared and _distinct(leaf(f)):
            tokens.setdefault(leaf(f), 'fn')
    # 공용 아닌 바뀐 함수 — 부르는 자리(≤ 2)의 함수 이름 · 맨 위 자리면 그 줄의 id 도 글자로(한 층 위)
    for f in [x for x in touched if x not in shared]:
        nm = leaf(f)
        for model in (mo, mn):
            for m in re.finditer(r'(?<![\w$.])' + re.escape(nm) + r'\s*\(', model.nocom):
                if model.resolve(nm, m.start()) != f:
                    continue
                ch = [g for g in model.chain(m.start()) if g['id'] != f]
                if ch:
                    tokens.setdefault(ch[0]['name'], 'caller')
                else:
                    ls = model.html.rfind('\n', 0, m.start()) + 1
                    le = model.html.find('\n', m.start())
                    _html_tokens(model.html[ls:le], tokens, only_ids=True)
                    for s2 in RX_STR.finditer(model.html[ls:le]):
                        if s2.group(2).startswith('#'):
                            _str_tokens(s2.group(2), tokens)
    return {'touched': touched, 'refs': sorted(refs), 'tokens': tokens, 'shared_hit': hit, 'src': src, 'notes': notes, 'css': css_n,
            'shared_n': len(shared), 'tool_refs': sorted(r for r in refs if r in tools)}


def _str_tokens(s, tokens):
    s = s.strip()
    if not s or len(s) > 120 or '${' in s or re.fullmatch(r'-?[a-z\-]+\s*:\s*[^:;{}]+;?', s):   # 템플릿 조각 · CSS 선언 글자(text-align:left)는 안 씀
        return
    if s.startswith('#') and re.fullmatch(r'#[\w\-]+', s):
        if _distinct(s[1:]) or len(s) > 4:
            tokens.setdefault(s[1:], 'id')
        return
    if re.match(r'^[#.\[][^\s]', s) and re.search(r'[#.\[]', s) and not re.search(r'[<>=;{}]', s.replace('>', '')):
        for x in _norm_sel(s):
            if len(x) >= 4:
                tokens.setdefault(x, 'sel')
        for idm in re.finditer(r'#([\w\-]+)', s):
            tokens.setdefault(idm.group(1), 'id')
        return
    if re.fullmatch(r'[^\s<>"\'`]{4,}', s) and _distinct(s):
        tokens.setdefault(s, 'str')


def _html_tokens(t, tokens, only_ids=False):
    for m in RX_HTML_ID.finditer(t):
        if len(m.group(1)) >= 3:
            tokens.setdefault(m.group(1), 'id')
    for m in re.finditer(r'''(?:getElementById|\$)\(\s*['"]#?([\w\-]+)['"]''', t):
        tokens.setdefault(m.group(1), 'id')
    if only_ids:
        return
    for m in RX_HTML_CLASS.finditer(t):
        for c in m.group(1).split():
            if _distinct(c) and '${' not in c and not re.search(r'[{}?:]', c):
                tokens.setdefault('.' + c, 'class')
    for m in RX_ON_ATTR.finditer(t):
        tokens.setdefault(m.group(1), 'fn')


# ── 하네스 고르기 ────────────────────────────────────────────────────────────────────────────
def _hsrc(hhome, r, cache):
    """하네스 소스 + 입력에 든 로컬 모듈(.py · n: · 하네스 자신 빼고) 글"""
    k = r['file']
    if k in cache:
        return cache[k]
    parts = []
    fp = os.path.join(hhome, *r['file'].split('/'))
    try:
        parts.append(open(fp, 'rb').read().decode('utf-8', 'replace'))
    except OSError:
        pass
    for x in r.get('inputs') or []:
        if x.startswith('n:') and x.endswith('.py') and x[2:] != r['file']:
            mp = os.path.join(hhome, *x[2:].split('/'))
            if mp not in cache:
                try:
                    cache[mp] = open(mp, 'rb').read().decode('utf-8', 'replace')
                except OSError:
                    cache[mp] = ''
            parts.append(cache[mp])
    cache[k] = '\n'.join(parts)
    return cache[k]


def sel_parts(sel):
    """선택자의 낱 이름(클래스 · id · [속성]) 가운데 고르기에 쓸 만한 것"""
    xs = [a or b for a, b in re.findall(r'[#.]([\w\-]+)|\[([\w\-]+)', sel)]
    return [x for x in dict.fromkeys(xs) if _distinct(x)]


def _hit(tok, kind, text):
    if kind in ('css', 'sel'):
        t = re.sub(r'\s+', ' ', text)
        if tok in t or tok.replace(' > ', '>') in t:
            return True
        ps = sel_parts(tok)   # 선택자 글자 통째가 없으면 — 그 선택자의 낱 이름이 하네스에 다 들어야 고름(하나만 들면 안 고름 · .g3tx 만 쓰는 하네스는 .g3it .g3tx 를 안 탐)
        return bool(ps) and all(re.search(r'(?<![\w\-])' + re.escape(x) + r'(?![\w\-])', text) for x in ps)
    if re.fullmatch(r'[\w$]+', tok):
        return re.search(r'(?<![\w$])' + re.escape(tok) + r'(?![\w$])', text) is not None
    return tok in text


def path_inputs(path):
    """바뀐 genie 길 → 전수표 입력 꼴 후보"""
    c = ['genie:' + path]
    if path.startswith('_qa/'):
        c.append('n:' + path[4:])
    return c


def _in_match(inputs, cands):
    for x in inputs or []:
        for c in cands:
            if x == c or (x.endswith('/**') and c.startswith(x[:-2])):
                return x
    return None


def select(app, rows, ch, app_res, hhome, sec_of, runnable=None):
    """→ {'full': bool, 'why': 첫 줄 까닭, 'rows': [줄], 'pick': {이름: 까닭}}"""
    from collections import OrderedDict
    APPF = SN.APP_FILE.get(app)
    pick = OrderedDict()
    rname = lambda r: os.path.basename(r['file'])[:-3].replace('_harness_', '')
    # 공용 층 — 그 앱 파일에서
    hit = {}
    for p, res in app_res.items():
        if p == APPF and res['shared_hit']:
            hit.update(res['shared_hit'])
    if hit:
        names = list(hit)
        why = '공용 층 건드림 → %s 전체 %d — %s%s' % (app, len([r for r in rows]), ' · '.join(names[:6]), (' 외 %d' % (len(names) - 6)) if len(names) > 6 else '')
        return {'full': True, 'why': why, 'rows': list(rows), 'pick': {rname(r): '전체(공용 층)' for r in rows}, 'hit': hit}
    # 다른 앱 파일의 공용 층 → 그 파일을 읽는 하네스
    for p, res in app_res.items():
        if p != APPF and res['shared_hit']:
            for r in rows:
                if ('genie:' + p) in (r.get('inputs') or []):
                    pick.setdefault(rname(r), '%s 공용 층(%s)' % (p, ', '.join(list(res['shared_hit'])[:3])))
    appfiles = set(SN.APP_FILE.values())
    for st, p in ch:
        if p in appfiles:
            continue
        cands = path_inputs(p)
        for r in rows:
            if p == '_qa/' + r['file']:
                pick.setdefault(rname(r), '판 관문(하네스 %s)' % ('새로' if st.startswith('A') else '바뀜'))
                continue
            m = _in_match(r.get('inputs'), cands)
            if m:
                pick.setdefault(rname(r), '입력 바뀜 ' + m)
    tokens = {}
    for p, res in app_res.items():
        for t, k in res['tokens'].items():
            tokens.setdefault(t, k)
    cache = {}
    for r in rows:
        src = _hsrc(hhome, r, cache)
        ins = ' '.join(r.get('inputs') or [])
        got = [t for t, k in tokens.items() if _hit(t, k, src) or (k == 'str' and t in ins)]
        if got:
            pick.setdefault(rname(r), '글자 ' + ' · '.join(got[:4]) + (' 외 %d' % (len(got) - 4) if len(got) > 4 else ''))
    # 태그 smoke 하나 — 가장 짧은 것(여기서 돌 수 있는 것 먼저)
    sm = [r for r in rows if 'smoke' in (r.get('tags') or []) and not r.get('skip')]
    if sm:
        appin = 'genie:' + APPF if APPF else None
        sm.sort(key=lambda r: (0 if (runnable is None or runnable(r)) else 1, 0 if (appin and appin in (r.get('inputs') or [])) else 1,
                               float(sec_of(r) or 1e9), r['file']))
        s0 = sm[0]
        if rname(s0) not in pick:
            pick[rname(s0)] = 'smoke 하나(%s)' % (('%.0f초' % float(sec_of(s0))) if sec_of(s0) else '잰 적 없음')
    sel = [r for r in rows if rname(r) in pick]
    nt = sum(len(res['tokens']) for res in app_res.values())
    why = '공용 층 안 건드림 → 하네스 %d/%d — %s' % (len(sel), len(rows), ' · '.join('%s(%s)' % (k, v) for k, v in list(pick.items())[:8]))
    return {'full': False, 'why': why, 'rows': sel, 'pick': dict(pick), 'hit': {}, 'tokens': nt}


def affected(app, rows, bctx, nctx, hhome, sec_of, runnable=None):
    """판 둘 → select 결과 + diff 요약"""
    ch = changed(bctx, nctx)
    res = {}
    for st, p in ch:
        if p in SN.APP_FILE.values():
            old, new = text_at(bctx, p), text_at(nctx, p)
            if not old or not new:   # 앱 파일이 새로 생기거나 없어짐 = 통째
                res[p] = {'touched': {}, 'refs': [], 'tokens': {}, 'shared_hit': {'(파일 %s)' % ('새로' if not old else '지움'): '앱 파일 통째'},
                          'src': '', 'notes': [], 'css': 0, 'shared_n': 0}
                continue
            res[p] = analyze_app([a for a, f in SN.APP_FILE.items() if f == p][0], p, old, new, hunks(bctx, nctx, p))
    out = select(app, rows, ch, res, hhome, sec_of, runnable)
    out['changed'] = ch
    out['app_res'] = res
    return out
