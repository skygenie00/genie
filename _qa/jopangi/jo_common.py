# -*- coding: utf-8 -*-
"""조판기 앱 v0 공용 모듈 — 볼트 조문노트 파싱 + 평문 좌표계.

핵심 = **하나의 평문 좌표계**(plainize)를 컴파일러와 뷰어가 똑같이 계산한다.
마크업·링크·각주가 전부 이 좌표계 위의 구간으로 표현되므로,
평문 앵커(직전 25자)가 필요 없다 — 지시서 §1-2 (a) 결정.
"""
import re, os, sys, io, collections

# ⚠ insert(0) 로 넣으면 **이 모듈을 import 한 뒤의 모든 import 를 N: 가 가로챈다.**
#   실제로 jo_build 가 jimun_part 를 N: 의 낡은 사본에서 읽어 검산 한 줄이 통째로 사라졌다.
#   P4 스크립트만 필요하므로 맨 뒤에 붙인다.
#   스크립트 실물이 한 폴더로 모였으므로 드라이브 문자를 박지 않고 이 파일 옆을 쓴다.
_P4 = os.path.dirname(os.path.abspath(__file__))
if _P4 not in sys.path:
    sys.path.append(_P4)
import structure  # P4 산출물 재사용 (새 추출기 금지)


# ────────────────────────────── 검산 판정 규약 (지시서 v3-A §5-1)
#   검산[이름] = '문자열' 을 버리고 판정값을 갖는 레코드로 바꾼다.
#   판정 = 'OK' | 'NG' | 'WARN' | 'INFO'      게이트는 NG 가 하나라도 있으면 멈춘다.
JEONG = ('OK', 'NG', 'WARN', 'INFO')

# 코드 → 어긋났을 때의 판정 (갈래표 · 2026-08-24 사용자 확정).
#   'INFO' 는 목록만 내는 항목. 표에 없는 코드는 WARN 으로 떨어진다 — NG 를 몰래 만들지 않는다.
GATE = {
    'A': 'NG', 'B': 'NG', 'C': 'NG', 'D': 'NG', 'E': 'NG', 'F': 'NG',
    '임베드': 'NG', '평문블록참조': 'INFO', 'H': 'NG', 'H2': 'WARN', 'I': 'NG',
    # ⚠ K 는 INFO 다(8/26) — 표본 행을 화면에서 없애 **진입로가 사라졌다**.
    #   §0-2 규약대로 **지우지 않고** 갈래만 내린다. 렌더 코드(`sampleCards`)는 살아 있고
    #   `S.mok='__표본'` 으로 여전히 도달한다.
    'K': 'INFO', 'L': 'WARN', 'M': 'NG', 'M-2': 'WARN',
    'M3': 'NG', 'M4': 'NG', 'M5': 'NG',      # 8/26 신설 — 문번·흡수·8자ID

    'N': 'WARN', 'Q': 'WARN', 'R': 'NG', 'R2': 'WARN', 'S': 'WARN',
    'O': 'NG', 'O2': 'WARN',
    # v3-K (8/27) — 빈칸 재료(blank_build). K1~K3 = 수·키·정답 무결이라 NG · K4~K6 = 보고성
    'K1': 'NG', 'K2': 'NG', 'K3': 'NG', 'K4': 'WARN', 'K5': 'WARN', 'K6': 'WARN',
    # v3-K2 (8/27) — 디보 빈칸(유시훈 짝) — 같은 결
    'K1d': 'NG', 'K2d': 'NG', 'K3d': 'NG', 'K4d': 'WARN', 'K5d': 'WARN', 'K6d': 'WARN',
    'ID': 'NG', '되돌아감': 'NG', '입력시각': 'WARN', '옮기기': 'NG', 'git': 'NG',
}


class Checks:
    """검산 레코드 모음. 낡은 `검산[이름] = 문자열` 호출도 받아서 **눈에 보이게** 남긴다
       — 조용히 사라지면 8/23 처럼 검산 한 줄이 없어진 것을 아무도 모른다."""

    def __init__(self):
        self.rows = []

    def chk(self, 코드, 이름, 판정, 실측, 기준, 비고=''):
        if 판정 not in JEONG:
            raise ValueError('판정은 %s 중 하나여야 한다: %r' % (JEONG, 판정))
        self.rows.append({'코드': str(코드), '이름': 이름, '판정': 판정,
                          '실측': str(실측), '기준': str(기준), '비고': 비고})
        return 판정

    # 갈래는 GATE 표에서 찾는다 — 호출하는 쪽이 NG 를 임의로 만들 수 없게 한다.
    def gate(self, 코드, 이름, ok, 실측, 기준, 갈래=None, 비고=''):
        갈래 = 갈래 or GATE.get(str(코드), 'WARN')
        return self.chk(코드, 이름, 'OK' if ok else 갈래, 실측, 기준, 비고)

    def __setitem__(self, k, v):        # 미변환 호출 감지용
        self.rows.append({'코드': '?', '이름': str(k), '판정': 'WARN',
                          '실측': str(v), '기준': '—',
                          '비고': '⚠ 판정 규약으로 안 바뀐 낡은 호출이다'})

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)

    @property
    def 판정(self):
        return 'NG' if any(r['판정'] == 'NG' for r in self.rows) else 'OK'

    def by(self, 판정):
        return ['%s %s — %s (기준 %s)' % (r['코드'], r['이름'], r['실측'], r['기준'])
                for r in self.rows if r['판정'] == 판정]

# ────────────────────────────── 볼트 루트 탐색 (지시서 v3-A §4-1)
#   사용자명을 코드에 박지 않는다. 두 PC 실측값이 둘 다 %USERPROFILE%\Documents\PA's archive 다.
VAULT_NEED = [r'산업재산권법\1.특허법\조문', r'산업재산권법\2.상표법\조문',
              r'산업재산권법\3.디보법\조문', r'민사소송법\민소법조문']


def find_vault():
    r"""(볼트_「변리사 시험」_폴더, 없는폴더목록, 뒤진자리목록).
       ① 환경변수 JOPANGI_VAULT  ② %USERPROFILE%\Documents\PA's archive
       둘이 없으면 (None, …) — **다른 자리를 뒤지지 않는다.**"""
    roots = []
    if os.environ.get('JOPANGI_VAULT'):
        roots.append(os.environ['JOPANGI_VAULT'])
    up = os.environ.get('USERPROFILE')
    if up:
        roots.append(os.path.join(up, 'Documents', "PA's archive"))
    tried, miss_at = [], None
    for root in roots:
        for base in (os.path.join(root, '변리사 시험'), root):
            tried.append(base)
            if not os.path.isdir(base):
                continue
            miss = [n for n in VAULT_NEED if not os.path.isdir(os.path.join(base, n))]
            if not miss:
                return base, [], tried
            if miss_at is None:
                miss_at = miss
    return None, (miss_at or []), tried


CALLOUT_HEAD = re.compile(r'^\s*>\s*\[!note\]-\s*원본\s*$')
LINK_D = re.compile(r'\[\[([^\[\]|]+)\|([^\[\]|]+)\]\]')
LINK_P = re.compile(r'\[\[([^\[\]|]+)\]\]')
EMBED = re.compile(r'!\[\[([^\[\]]+)\]\]')
FNREF = re.compile(r'\[\^([^\]]+)\]')
FNDEF = re.compile(r'^\s*\[\^([^\]]+)\]:\s?(.*)$')
BLOCKID = re.compile(r'(?<![\[\w])\^([A-Za-z0-9][A-Za-z0-9-]{2,})\s*$')
TAGLINE = re.compile(r'^\s*#[^\s#]\S*')

# 마크업 인라인 토큰 — 여는/닫는 쌍
MARKUP_TOKENS = [
    ('font', re.compile(r'<font\s+color\s*=\s*"?([^">]+)"?\s*>', re.I), re.compile(r'</font>', re.I)),
    ('span', re.compile(r'<span\s+([^>]*)>', re.I), re.compile(r'</span>', re.I)),
    ('u',    re.compile(r'<u>', re.I),  re.compile(r'</u>', re.I)),
    ('mark', re.compile(r'=='), re.compile(r'==')),
    ('bold', re.compile(r'\*\*'), re.compile(r'\*\*')),
    ('strike', re.compile(r'~~'), re.compile(r'~~')),
]


def split_note(text):
    """노트 → (정리부 줄들, 원본콜아웃 줄들). 콜아웃이 없으면 원본은 빈 배열."""
    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    for i, ln in enumerate(lines):
        if CALLOUT_HEAD.match(ln):
            body = []
            for x in lines[i + 1:]:
                if x.startswith('>'):
                    body.append(re.sub(r'^>\s?', '', x))
                elif not x.strip():
                    continue
                else:
                    break
            return lines[:i], body
    return lines, []


# ── revfix0930 A-1 (9/30) — 다른 법 인용 판정 · 앱 wmAutoOther(jo/index.html)와 **한 벌**이다(고치면 둘 다 고친다) ──
#   조 인용 앞 글을 인용 사슬째 걷는다(띄어쓰기 · ㆍ · , · 및 · 또는 · 와/과 · 이나 · 부터 · 까지 · 내지 · ~ · 앞 인용 · 편·장·절 · 괄호 묶음).
#   남은 글이 ① 「법 이름」 ② 같은/동 법·법률·영·규칙·조약·협정·의정서·협약 ③ 시행령·시행규칙
#   ④ 조약 이름(…협정 · …조약 · …의정서 · …협약 — 「」 없이 쓴 「헤이그협정 제1조」 · 「마드리드 의정서 제2조」)
#   ⑤ 맨 법 이름(…법 · …법률 — 「비송사건절차법 제248조」 · 이 법 · 본법 · 동법 · 방법 같은 낱말은 뺌) 으로 끝나면 다른 법 인용이다.
_OL_TAIL = re.compile(r'(?:\s|ㆍ|·|,|및|또는|와|과|이나|부터|까지|내지|~|\()+$')
_OL_PAR = re.compile(r'\([^()]*\)$')
_OL_JO = re.compile(r'제\d+조(?:의\d+)?(?:제\d+항)?(?:제\d+호(?:의\d+)?)?(?:제\d+목)?(?:\(\d+\))?$')
_OL_UNIT = re.compile(r'(?:제\d+(?:편|장|절|관|항|목)|제\d+호(?:의\d+)?)$')
_OL_SAME = re.compile(r'(?:같은|동)\s*(?:법률|법|영|규칙|조약|협정|의정서|협약)$')
_OL_SUB = re.compile(r'(?:시행령|시행규칙)$')
_OL_TREATY = re.compile(r'(?:협정|조약|의정서|협약)$')
_OL_HRUN = re.compile(r'[가-힣]+$')
_OL_LAWW = re.compile(r'법(?:률)?$')
OL_NOTLAW = frozenset(('법', '법률', '이법', '본법', '동법', '방법', '위법', '적법', '불법', '입법', '편법', '합법', '용법',
                       '문법', '해법', '기법', '수법', '요법', '공법', '사법', '준법', '탈법', '무법'))


def other_law_cite(pre):
    """조 인용 바로 앞 글(pre · 160자 안팎) → 다른 법 인용이면 True"""
    t = pre
    for _ in range(80):
        t2 = _OL_UNIT.sub('', _OL_JO.sub('', _OL_PAR.sub('', _OL_TAIL.sub('', t))))
        if t2 == t:
            break
        t = t2
    if t.endswith('」') or _OL_SAME.search(t) or _OL_SUB.search(t) or _OL_TREATY.search(t):
        return True
    m = _OL_HRUN.search(t)
    return bool(m and _OL_LAWW.search(m.group(0)) and m.group(0) not in OL_NOTLAW)


def plainize(line):
    """한 줄 → (평문, 요소목록).

    평문 = 마크업·링크문법·각주참조·블록ID를 걷어낸 순수 텍스트(들여쓰기 유지).
    요소 = 평문 좌표 위의 구간. 뷰어가 이 좌표로 되살린다.
      {'kind':'link','a':int,'b':int,'target':str}          [[대상|표시]]
      {'kind':'embed','a':int,'b':int,'target':str}         ![[대상]]  (해소하지 않는다)
      {'kind':'fnref','a':int,'b':int,'id':str}             [^1]  (b==a · 삽입점)
      {'kind':'markup','a':int,'b':int,'유형':str,'값':str}  <font>·==·** 등
    """
    src = line
    out = []          # 평문 조각
    els = []
    open_stack = []   # (유형, 값, 평문시작)
    i = 0
    plen = 0

    def emit(s):
        nonlocal plen
        out.append(s)
        plen += len(s)

    # ⚠ 한 줄에 블록 ID 가 둘 붙은 곳이 있다(상-제34조 ' ^50b022   ^f37c3b').
    #    뒤에서부터 전부 걷어낸다. 대표값 = 맨 뒤 것(blockid_census.py 와 같은 규칙).
    ids = []
    while True:
        m = BLOCKID.search(src)
        if not m:
            break
        ids.append(m.group(1))
        src = src[:m.start()]
    ids.reverse()
    blockid = ids[-1] if ids else None

    while i < len(src):
        # 임베드가 링크보다 먼저 (![[..]] 는 [[..]] 를 포함한다)
        m = EMBED.match(src, i)
        if m:
            els.append({'kind': 'embed', 'a': plen, 'b': plen, 'target': m.group(1)})
            i = m.end()
            continue
        m = LINK_D.match(src, i)
        if m:
            a = plen
            emit(m.group(2))
            els.append({'kind': 'link', 'a': a, 'b': plen,
                        'target': m.group(1), 'disp': m.group(2)})
            i = m.end()
            continue
        m = LINK_P.match(src, i)
        if m:
            a = plen
            emit(m.group(1))
            els.append({'kind': 'link', 'a': a, 'b': plen,
                        'target': m.group(1), 'disp': m.group(1)})
            i = m.end()
            continue
        m = FNREF.match(src, i)
        if m:
            els.append({'kind': 'fnref', 'a': plen, 'b': plen, 'id': m.group(1)})
            i = m.end()
            continue

        hit = None
        for 유형, op, cl in MARKUP_TOKENS:
            # 닫는 쪽 먼저 본다 — == 나 ** 는 여닫이가 같은 토큰이라
            # 열려 있으면 닫는 것으로 읽어야 한다
            if open_stack and open_stack[-1][0] == 유형:
                m = cl.match(src, i)
                if m:
                    유, 값, a = open_stack.pop()
                    els.append({'kind': 'markup', 'a': a, 'b': plen, '유형': 유, '값': 값})
                    hit = m.end()
                    break
            m = op.match(src, i)
            if m:
                값 = m.group(1) if m.groups() else ''
                if 유형 == 'span':
                    값 = 'style="%s"' % re.sub(r'^style\s*=\s*"?|"$', '', 값.strip())
                open_stack.append((유형, 값, plen))
                hit = m.end()
                break
        if hit is not None:
            i = hit
            continue
        emit(src[i])
        i += 1

    # 안 닫힌 마크업은 줄 끝까지로 본다
    while open_stack:
        유, 값, a = open_stack.pop()
        els.append({'kind': 'markup', 'a': a, 'b': plen, '유형': 유, '값': 값,
                    '미닫힘': True})

    plain = ''.join(out)
    els.sort(key=lambda e: (e['a'], e['b']))
    return plain, els, (blockid, ids)


def parse_note(path):
    """조문노트 1개 → dict. 정리부 줄마다 구조키·평문·요소를 붙인다."""
    raw = open(path, encoding='utf-8').read()
    edit_lines, orig_lines = split_note(raw)

    items = structure.classify(edit_lines)
    items = structure.body_slots(items)

    footnotes = {}
    rows = []
    for (k, ln) in items:
        m = FNDEF.match(ln)
        if m:
            # ⚠ 각주 본문도 같은 평문 좌표계에 태운다 — 여기에도 마크업이 붙는다
            #    (특-제10조·제21조·제28조의2·제66조의3 실측).
            plain, els, (bid, bids) = plainize(m.group(2))
            footnotes[m.group(1)] = len(rows)
            rows.append({'키': ['각주', m.group(1)], '평문': plain, '요소': els,
                         '블록ID': bid, '블록ID들': bids, '꼬리': True, '각주정의': m.group(1)})
            continue
        if k[0] in ('빈줄',):
            continue
        plain, els, (bid, bids) = plainize(ln)
        # ⚠ 블록 ID 만 있는 줄을 버리면 앵커 8개가 사라진다(상-제34조).
        if not plain.strip() and not els and not bids:
            continue
        rows.append({'키': list(k), '평문': plain, '요소': els,
                     '블록ID': bid, '블록ID들': bids, '꼬리': k[0] in ('꼬리', '두문자')})
    return {'정리부': rows, '원본': orig_lines, '각주': footnotes}


def flat_of(rows):
    """정리부 평문 줄들 → 한 줄 평문 + (flat위치 → (행idx, 열)) 역맵.
       마크업 레이어의 문맥 앵커가 줄바꿈을 공백으로 바꾼 형태라 이렇게 맞춘다."""
    buf = []
    idx = []          # flat 각 문자 → (row, col)
    for ri, r in enumerate(rows):
        s = r['평문'].strip()
        if not s:
            continue
        off = len(r['평문']) - len(r['평문'].lstrip())
        if buf:
            buf.append(' ')
            idx.append(None)
        for ci, ch in enumerate(s):
            buf.append(ch)
            idx.append((ri, off + ci))
    return ''.join(buf), idx


# ══════════════ 기출 메인 역방향 (2026-09-20 · `_task_prec_vault_link_add1.md` §A) ══════════════
#   기출 노트 `2차<과>기출\` 머리말 `연결판례:` → 요약본 파일이름 → {2차 코드}.
#   ⚠ **두 법 노트를 다 읽고, 요약본이 어느 법 폴더에 있든 찾는다** — 키가 파일이름 글자라서 폴더와 무관하다.
#     상표 판례가 특허 2차 문제의 메인인 일이 있고(2002후567), 요약본이 법 폴더를 옮겨 다니기도 한다.
#   ⚠ ⚙(`jo_build` 검산 F2)와 이관 스크립트(`gichul_vault_fill`)가 **이 한 함수**를 같이 쓴다.
#     9/20 에 둘이 서로 다른 조회를 써서 하나는 통과하고 하나는 M 을 벗기려 들었다.
GI_NOTE_DIRS = (r'산업재산권법\1.특허법\2차특허기출', r'산업재산권법\2.상표법\2차상표기출')
GI_NOTE_RE = re.compile(r'^([특상디])기출 (\d\d)-(\d+)-(\d+)')
_GI_REV = {}


def gichul_rev(vault):
    """요약본 파일이름 → {'2차-<과>-YY-회-N'} (기출 노트 머리말 `연결판례:` 역방향)."""
    if vault in _GI_REV:
        return _GI_REV[vault]
    rev = collections.defaultdict(set)
    for rel in GI_NOTE_DIRS:
        d = os.path.join(vault, rel)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            m = GI_NOTE_RE.match(f)
            if not (f.endswith('.md') and m):
                continue
            code = '2차-%s-%s-%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4))
            t = io.open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
            if not t.startswith('---'):
                continue
            e = t.find('\n---', 3)
            head = t[3:e] if e >= 0 else t[3:]
            on = False
            for ln in head.split('\n'):
                s = ln.rstrip('\r')
                mm = re.match(r'^([A-Za-z0-9가-힣_]+)\s*:\s?(.*)$', s)
                if mm:
                    on = (mm.group(1) == '연결판례')
                    if on and mm.group(2).strip():
                        for Lk in LINK_P.findall(mm.group(2)) + [x[0] for x in LINK_D.findall(mm.group(2))]:
                            rev[Lk.split('#')[0].split('/')[-1].strip()].add(code)
                    continue
                if on and re.match(r'^\s*-\s', s):
                    for Lk in LINK_P.findall(s) + [x[0] for x in LINK_D.findall(s)]:
                        rev[Lk.split('#')[0].split('/')[-1].strip()].add(code)
    _GI_REV[vault] = rev
    return rev
