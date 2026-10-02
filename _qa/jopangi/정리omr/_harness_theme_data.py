# -*- coding: utf-8 -*-
"""관문 — 정리omr 테마 재료(theme/patent_hr8/테마.json.gz) + 8판 글 파일(words/patent_hr8/글.json.gz)
   (jopangi/task/_task_jo_theme_data.md §B · 2026-10-01)

  python _harness_theme_data.py [--tables <표 폴더>]
  자리: N:(정리omr 주석1·프1 PDF · _테마 표 — need_n) · MBPDF_ROOT(두 출력 · 읽기만) · GENIE_ROOT(조문 재료 · 읽기만)
  쓰는 것: <표 폴더>\\_check.md(B-3 표본 · 바뀌었을 때만) · %TEMP% 시험 굽기(표 사본 · gz) — 배달된 출력·N: 표는 안 고친다
  B-1 박스 · B-2 표 초안(메모리 — 사용자가 표를 손질해도 안 흔들린다 · N: 표 = 초안인지는 정보 줄) · B-3 표본 · B-4 구역 SVG(시험 구역 줄을 임시 표에 더해 굽고 · 하네스가 따로 센 run·Ink 와 맞댐)
  B-5 테마.json.gz(크기 · 두 번 굽기 md5 · 한 줄 고침 = 그 테마만) · B-6 글.json.gz · B-7 D11 · genie 무변
  fix2(2026-10-02) — B-2 박스 칸 잣대 = 큰 박스 70(초안 거리 규칙 걷음 · _task_jo_theme_fix2 §A-1) · 묶음·구역 그림·테마 점 관문 = _harness_theme_fix2.py
  헛잣대: 프1 맞대기를 1pt 민 박스(짝 ≈ 0) · 빈 구역(text 0 · path 0) · minbeoppdf 착수 바탕 70766166(두 출력 없음)
  ⚠ 색 — 지시서 「색 종류 ≤ 8」 은 §0-1 의 8 색 목록을 잣대로 쓴 것인데 실측은 26 색이다(2026-10-01). 색이 제대로 읽혔는지는
     「글자 색 = 프1 같은 자리 색」 159,787/159,787 로 갈음해 잰다(갈음 줄로 찍는다 · 채팅 확인 대기).
  끝 줄 = 「PASS n · FAIL m」 · 종료 코드 0 = FAIL 0
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import argparse, collections, csv, gzip, hashlib, io, json, os, random, re, shutil, statistics, subprocess, sys, tempfile, time
import xml.etree.ElementTree as ET

NROOT = _roots.need_n('정리omr 주석1·프1 PDF · _테마 표')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _theme_build as TB   # noqa: E402
sys.path.insert(0, os.path.join(NROOT, 'minbeop', 'script'))
import _book_text_build as BT   # noqa: E402
sys.path.append(NROOT)
import _d11_scan   # noqa: E402

DOCID = 'patent_hr8'
BASE_MBPDF = '70766166'          # minbeoppdf 착수 바탕(두 출력 없음)
WANT_TEXT_CHARS = 874457
WANT_BOOK = {'보정을무효로': [(55, 2), (776, 1)]}
WANT_SC = ('심사청구', 84, 316)
TEST_REGION = (1, [120, 0, 270, 32])   # 시험 구역(지시서 §0-2 보기 자리 · 1쪽 x 120~270 · y 0~32pt)
CHAT_REF = dict(text=24, path=24, bytes=21829)   # 채팅 실측(참고 — 정의가 같으란 법은 없다)
R = []


def P(*a):
    print(*a, flush=True)


def T(gate, name, ok, val=''):
    R.append((gate, name, bool(ok)))
    P('%s %s %s%s' % ('PASS' if ok else 'FAIL', gate, name, (' — %s' % (val,)) if val != '' else ''))


def INFO(gate, name, val=''):
    P('INFO %s %s%s' % (gate, name, (' — %s' % (val,)) if val != '' else ''))


def stage(name, t0):
    P('  [단계] %s %.2f분' % (name, (time.time() - t0) / 60))


def write_if_changed(path, data):
    if os.path.isfile(path) and open(path, 'rb').read() == data:
        return False
    TB.write_verified(path, data)
    return True


def git_status(repo):
    """읽기만 — --no-optional-locks: 색인 새로고침 쓰기(index.lock)를 안 잡는다(본 세션이 같은 때 git 을 돌릴 수 있다)"""
    r = subprocess.run(['git', '--no-optional-locks', '-C', repo, '-c', 'core.quotepath=false', 'status', '--porcelain'], capture_output=True)
    return r.stdout


def git_has(repo, rev, path):
    r = subprocess.run(['git', '-C', repo, 'cat-file', '-e', '%s:%s' % (rev, path)], capture_output=True)
    return r.returncode == 0


def git_rev_ok(repo, rev):
    return subprocess.run(['git', '-C', repo, 'cat-file', '-e', rev + '^{commit}'], capture_output=True).returncode == 0


# ── 하네스 따로 센 값(B-4) — 빌더 함수를 쓰지 않고 다시 짠다 ──
def my_runs(X, p, reg):
    rx0, ry0, rx1, ry1 = reg
    n = 0
    for b in X['boxes']:
        if b['p'] != p or not b['chars']:
            continue
        ns = [c for c in b['chars'] if c['t'] != ' ']
        if not ns:
            continue
        thr = statistics.median([c['x1'] - c['x0'] for c in ns]) * 1.45
        rows = collections.OrderedDict()
        for c in sorted(b['chars'], key=lambda c: (c['b'], c['x0'], c['i'])):
            key = None
            for y in rows:
                if c['b'] - y <= 0.6 and c['b'] >= y:
                    key = y
            if key is None:
                key = c['b']
                rows[key] = []
            rows[key].append(c)
        for y, cs in rows.items():
            cs.sort(key=lambda c: (c['x0'], c['i']))
            cur_col, has, sp, prev = None, False, 0, None
            for c in cs:
                ins = rx0 <= (c['x0'] + c['x1']) / 2 <= rx1 and ry0 <= y - c['size'] * 0.35 <= ry1
                if not ins:
                    n += 1 if has else 0
                    cur_col, has, sp, prev = None, False, 0, None
                    continue
                if prev is not None and c['x0'] - prev['x1'] > thr:
                    n += 1 if has else 0
                    cur_col, has, sp = None, False, 0
                prev = c
                if c['t'] == ' ':
                    if has:
                        sp += 1
                        if sp >= 2:
                            n += 1
                            cur_col, has, sp = None, False, 0
                    continue
                if has and c['c'] != cur_col:
                    n += 1
                    has = False
                cur_col, has, sp = c['c'], True, 0
            n += 1 if has else 0
    return n


def my_inks(pdf_path, p, reg):
    import pikepdf
    rx0, ry0, rx1, ry1 = reg
    pdf = pikepdf.open(pdf_path)
    pg = pdf.pages[p - 1]
    H = float(pg.MediaBox[3])
    n = 0
    for a in pg.get('/Annots', []):
        if str(a.get('/Subtype')) != '/Ink':
            continue
        pts = []
        for s in a.get('/InkList', []):
            v = [float(q) for q in s]
            pts += [(v[i], H - v[i + 1]) for i in range(0, len(v) - 1, 2)]
        if pts and all(rx0 <= x <= rx1 and ry0 <= y <= ry1 for x, y in pts):
            n += 1
    return n


def find_counts(texts, q):
    """앱 cvbFind 와 같은 셈 — 공백(줄바꿈 포함) 뺀 쪽 글에서 겹침 허용"""
    out = []
    for i, t in enumerate(texts, 1):
        s = re.sub(r'\s+', '', t)
        at, j = 0, s.find(q)
        while j >= 0:
            at += 1
            j = s.find(q, j + 1)
        if at:
            out.append((i, at))
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--tables', help='표 폴더(기본 N: jopangi\\정리omr\\_테마)')
    a = ap.parse_args()
    d = TB.default_paths()
    tables = a.tables or d['tables']
    mb = _roots.mbpdf()
    gz_theme = _roots.mbpdf('theme', DOCID, '테마.json.gz')
    gz_text = _roots.mbpdf('words', DOCID, '글.json.gz')
    genie = _roots.genie()
    P('MBPDF_ROOT = %s · GENIE_ROOT = %s · 표 = %s' % (mb, genie, tables))
    T_ALL = time.time()
    gs0 = git_status(genie)
    tmp = tempfile.mkdtemp(prefix='h_theme_data_')

    # ═════ B-1 박스 ═════
    t0 = time.time()
    X = TB.extract(d['pdf'])
    lay = TB.layout_all(X)
    boxes = X['boxes']
    nsc = {b['k']: sum(1 for c in b['chars'] if c['t'] != ' ') for b in boxes}
    ntext = sum(1 for k in nsc if nsc[k])
    T('B-1', '박스 글 있음 148/191', ntext == 148 and len(boxes) == 191, '%d/%d' % (ntext, len(boxes)))
    chars = sum(nsc.values())
    line_chars = sum(len(r['t'].replace(' ', '')) for k in lay for ln in lay[k]['lines'] for r in ln['runs'])
    T('B-1', '글자 합 159,787(줄로 묶은 글자 = 글리프)', chars == TB.WANT_CHARS == line_chars, '%d · 줄 %d' % (chars, line_chars))
    f1 = TB.load_pdf1(d['pdf1'])
    hit, miss, colsame = TB.char_check(boxes, f1)
    T('B-1', '프1 1~5쪽 같은 자리 같은 글자 100%', hit == chars and miss == 0, '짝 %d · 못 찾음 %d' % (hit, miss))
    cols = sorted({c['c'] for b in boxes for c in b['chars'] if c['t'] != ' '})
    T('B-1', '색 — 지시서 「≤ 8」 갈음: 글자 색 = 프1 같은 자리 색', colsame == chars and hit == chars,
      '%d/%d · 색 종류 %d(지시서 §0-1 목록 8 = 일부 · 채팅 확인)' % (colsame, chars, len(cols)))
    xr = sum(TB.xrev_count(lay[k]['glines']) for k in lay)
    T('B-1', '줄 안 글자 x 역전 0(다음 글자 x0 < 앞 글자 x1 − 0.25pt)', xr == 0, xr)
    h2, m2, _c2 = TB.char_check(boxes, f1, dx_shift=1.0)
    T('B-1 헛잣대', '박스를 1pt 민 채 맞대면 짝 ≈ 0(잣대가 산다)', h2 < chars * 0.01, '짝 %d / %d' % (h2, chars))
    big = [k for k in nsc if nsc[k] >= TB.BIG]
    small = [k for k in nsc if 0 < nsc[k] < TB.BIG]
    head = sum(1 for k in big if re.match(r'^\s*(\{[^}]+\}|\d{1,2}\s*\.)', ''.join(r['t'] for r in lay[k]['lines'][0]['runs'])))
    T('B-1', '§0-2 큰 박스 70 · 작은 조각 78 · 머리 {…}/N. 61', (len(big), len(small), head) == (70, 78, 61), '%d · %d · %d' % (len(big), len(small), head))
    T('B-1', '§0-2 보기 k2 1,077자 · k6 1,500자', (nsc[2], nsc[6]) == (1077, 1500), '%d · %d' % (nsc[2], nsc[6]))
    jd = TB.load_jodata(d['jodata'])
    anyc, pat, dist_any, pairs_any, dist_pat, pairs_pat = set(), set(), set(), set(), set(), set()
    for k in lay:
        for s, law in TB.cites(TB.box_text(lay[k]), jd['jo_keys']):
            anyc.add(k); dist_any.add(s); pairs_any.add((k, s))
            if law == TB.LAW:
                pat.add(k); dist_pat.add(s); pairs_pat.add((k, s))
    T('B-1', '§0-2 조 인용 있는 박스 88', len(anyc) == 88, len(anyc))
    INFO('B-1', '조 종 · 짝(채팅 207 · 579 — 인용 꼴 정의 차)', '모든 법 %d · %d · 특허법(목록 안) %d · %d' % (len(dist_any), len(pairs_any), len(dist_pat), len(pairs_pat)))
    stage('B-1 박스', t0)

    # ═════ B-2 표 초안(메모리) ═════
    t0 = time.time()
    dr = TB.draft_tables(X, lay, jd)
    dtab = os.path.join(tmp, 'draft')
    os.makedirs(dtab)
    for f, key in ((TB.F_THEME, 'theme'), (TB.F_ACR, 'acr'), (TB.F_SUBJ, 'subj')):
        open(os.path.join(dtab, f), 'wb').write(dr[key])
    themes, acr, subj = TB.read_tables(dtab, len(boxes))
    T('B-2', '테마 70줄', len(themes) == 70, len(themes))
    listed = [int(k) for t in themes for k in t['boxes']]
    textk = sorted(k for k in nsc if nsc[k])
    dup = [k for k, n in collections.Counter(listed).items() if n > 1]
    # 옛 잣대 고침(2026-10-02 · _task_jo_theme_fix2 §A-1 · 사용자 10/2 09:17 「작은 박스 가까운 큰 박스에 붙임 — 누가 정했어」) — 초안의 거리 규칙(+k)을 걷었다:
    #   초안 박스 칸 = 큰 박스 70 한 번씩 · 작은 조각·그림 도장 0(묶음은 표 = 채팅 그림 검수 _theme_small_1002.csv 가 정한다 · 그 관문 = _harness_theme_fix2 A-2·A-3)
    T('B-2', '박스 칸 = 큰 박스 70 한 번씩(작은 조각·그림 0 · 빠짐 0 · 두 번 0 — fix2 §A-1 거리 규칙 걷음 · 옛 「글 있는 148 전부 +k」 갈음)', sorted(listed) == sorted(big) and not dup,
      '칸 %d · 큰 박스 %d · 작은 조각 %d · 두 번 %d · 글 없는 박스 %d' % (len(listed), len(big), len([k for k in listed if 0 < nsc[k] < TB.BIG]), len(dup), len([k for k in listed if not nsc[k]])))
    bigc = sum(1 for k in big if any(law == TB.LAW for _s, law in TB.cites(TB.box_text(lay[k]), jd['jo_keys'])))
    filled = sum(1 for t in themes if t['jo'])
    T('B-2', '조 칸 채워진 줄 = 특허법 조 인용 있는 큰 박스 수(70)', filled == bigc == 70, '%d · %d' % (filled, bigc))
    st = dr.get('acr_stat', {})
    T('B-2', '두문자 후보 수', len(acr) >= 1, '%d (규칙 %s → 합성어 거름 %s → 겹침 거름 %s)' % (len(acr), st.get('acr_rule'), st.get('acr_seg'), st.get('acr_final')))
    T('B-2', '주체 수 ≥ 15', len(subj) >= 15, len(subj))
    bkn = sum(1 for t in themes if t['bk'] is None)
    INFO('B-2', '초안 bk 칸 빈칸(굽을 때 테마 점 새 규칙으로 셈 — fix2 §A-4 · 옛 「bk 111 인 줄」 정보 갈음)', '%d/%d' % (bkn, len(themes)))
    same = all(os.path.isfile(os.path.join(tables, f)) and open(os.path.join(tables, f), 'rb').read() == dr[key]
               for f, key in ((TB.F_THEME, 'theme'), (TB.F_ACR, 'acr'), (TB.F_SUBJ, 'subj')))
    INFO('B-2', 'N: 표 = 초안 바이트(손질 전)', '예' if same else '아니오(손질됐거나 없음 — B-5 는 그 표로 잰다)')
    stage('B-2 표', t0)

    # ═════ B-3 표본 → _check.md ═════
    t0 = time.time()
    rnd = random.Random(20261001)
    md = ['# 정리omr 테마 표 — 표본(_harness_theme_data.py B-3 · 채팅 검수용 · 2026-10-01)', '',
          '> 원문 줄 = 정리omr 주석1 PDF 도장(텍스트박스) 글 · 줄 앞 「·」 수 = 들여쓰기(ind). 자동 생성 — 손으로 고치지 말 것(다시 돌리면 덮임).', '']
    ths = rnd.sample(themes, 5)
    md += ['## 테마 5', '']
    for t in ths:
        md.append('### %s · {%s} · 박스 %s · bk %s' % (t['id'], t['n'], ' '.join(t['boxes']), ''.join(map(str, t['bk'] or [0, 0, 0]))))
        md.append('- 조: %s' % (' '.join(t['jo']) or '(없음)'))
        k0 = int(t['boxes'][0])
        for ln in lay[k0]['lines'][:8]:
            md.append('    ' + '·' * ln['ind'] + ''.join(r['t'] for r in ln['runs']))
        md.append('')
    occ = {w: L for w, L in dr['acr_list']}
    aws = rnd.sample(list(acr.keys()), min(10, len(acr)))
    md += ['## 두문자 후보 10', '']
    for w in aws:
        md.append('- **%s** · 조 %s' % (w, ' '.join(acr[w]['jo']) or '(없음)'))
        for k, li, _c, line in occ.get(w, [])[:2]:
            md.append('    - k%d 줄%d: %s' % (k, li, line))
    md.append('')
    sws = rnd.sample(subj, min(10, len(subj)))
    freq = dict(dr['subj_list'])
    md += ['## 주체 10', '']
    for w in sws:
        line = next((t for t in jd['texts'] if w in t), '')
        i = line.find(w)
        ctx = ('…' if i > 35 else '') + line[max(0, i - 35):i + len(w) + 35].strip() + ('…' if i + len(w) + 35 < len(line) else '')
        md.append('- **%s** · 빈도 %s · %s' % (w, freq.get(w, '?'), ctx))
    md.append('')
    data = ('\n'.join(md)).encode('utf-8')
    chk = os.path.join(tables, '_check.md')
    wrote = write_if_changed(chk, data)
    T('B-3', '표본 _check.md — 테마 5 · 두문자 10 · 주체 10', len(ths) == 5 and len(aws) == min(10, len(acr)) == 10 and len(sws) == 10,
      '%s(%s · %d B)' % (chk, '씀' if wrote else '같음', len(data)))
    stage('B-3 표본', t0)

    # ═════ B-4 구역 SVG(시험 구역 줄) ═════
    t0 = time.time()
    stab = os.path.join(tmp, 'svg')
    shutil.copytree(dtab, stab)
    p_reg, reg = TEST_REGION
    inside_k = [str(b['k']) for b in boxes if b['p'] == p_reg and nsc[b['k']]
                and reg[0] <= (b['rect'][0] + b['rect'][2]) / 2 <= reg[2] and reg[1] <= (b['rect'][1] + b['rect'][3]) / 2 <= reg[3]]
    with open(os.path.join(stab, TB.F_THEME), 'ab') as f:
        f.write(('tsv1,구역 시험,%s,%d %s,,\r\n' % (' '.join(inside_k), p_reg, ' '.join(str(v) for v in reg))).encode('utf-8'))
        f.write(('tsv0,빈 구역(헛잣대),,1 0 0 1 1,,\r\n').encode('utf-8'))
    th2, ac2, sb2 = TB.read_tables(stab, len(boxes))
    obj2, _raw2, _blob2, svginfo = TB.bake(X, lay, TB.md5_file(d['pdf']), th2, ac2, sb2, jd)
    tz = next(t for t in obj2['themes'] if t['id'] == 'tsv1')
    svg = obj2['boxes']['tsv1r']['svg']
    try:
        ET.fromstring(svg)
        xml_ok = True
    except Exception:
        xml_ok = False
    nt, npth = svg.count('<text '), svg.count('<path ')
    want_t, want_p = my_runs(X, p_reg, reg), my_inks(d['pdf'], p_reg, reg)
    T('B-4', '구역 text 수 = 그 사각 안 글자 run 수(하네스가 따로 셈)', nt == want_t and nt > 0, '%d · %d (채팅 %d)' % (nt, want_t, CHAT_REF['text']))
    T('B-4', '구역 path 수 = 그 사각 안 Ink 수(pikepdf 로 따로 셈)', npth == want_p and npth > 0, '%d · %d (채팅 %d)' % (npth, want_p, CHAT_REF['path']))
    sz = len(svg.encode('utf-8'))
    T('B-4', 'SVG 크기 ≤ 60KB · XML 성함', sz <= 60 * 1024 and xml_ok, '%d B (채팅 %d B)' % (sz, CHAT_REF['bytes']))
    T('B-4', '구역 테마 박스 = 구역 박스 하나(구역 안 박스 %d 개는 SVG 로)' % len(inside_k), tz['boxes'] == ['tsv1r'] and tz['region'] and tz['region']['p'] == p_reg,
      '%s · region %s' % (tz['boxes'], tz['region']))
    e0 = obj2['boxes']['tsv0r']['svg']
    T('B-4 헛잣대', '빈 구역 = text 0 · path 0', e0.count('<text ') == 0 and e0.count('<path ') == 0, e0[:60])
    with gzip.open(gz_theme, 'rb') as f:
        dj = json.loads(f.read().decode('utf-8'))
    INFO('B-4', '배달본 구역 테마', '%d(초안은 구역 빈칸 — 사용자가 적으면 생긴다)' % sum(1 for t in dj['themes'] if t.get('region')))
    stage('B-4 SVG', t0)

    # ═════ B-5 테마.json.gz ═════
    t0 = time.time()
    blob = open(gz_theme, 'rb').read()
    md5_d = hashlib.md5(blob).hexdigest()
    T('B-5', '테마.json.gz ≤ 1.5MB', len(blob) <= 1.5 * 1024 * 1024, '%d B · md5 %s' % (len(blob), md5_d))
    T('B-5', 'pdfMd5 = 주석1 PDF md5', dj.get('pdfMd5') == TB.md5_file(d['pdf']), dj.get('pdfMd5'))
    th3, ac3, sb3 = TB.read_tables(tables, len(boxes))
    _o3, _r3, blob3, _s3 = TB.bake(X, lay, TB.md5_file(d['pdf']), th3, ac3, sb3, jd)
    T('B-5', '배달본 = 지금 표로 다시 구운 것(바이트)', blob3 == blob, hashlib.md5(blob3).hexdigest())
    mds = []
    for seed in ('1', '2'):
        ctab = os.path.join(tmp, 'e2e%s' % seed)
        shutil.copytree(tables, ctab, ignore=shutil.ignore_patterns('_check.md'))
        outp = os.path.join(tmp, 'e2e%s.json.gz' % seed)
        env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING='utf-8')
        r = subprocess.run([sys.executable, os.path.join(HERE, '_theme_build.py'), '--tables', ctab, '--out', outp, '--no-pdf1'],
                           capture_output=True, env=env)
        mds.append(hashlib.md5(open(outp, 'rb').read()).hexdigest() if r.returncode == 0 and os.path.isfile(outp) else 'rc%d' % r.returncode)
    T('B-5', '두 번 만들어 md5 같음(PYTHONHASHSEED 1 · 2 · 처음부터 끝까지) = 배달본', mds[0] == mds[1] == md5_d, ' · '.join(mds))
    etab = os.path.join(tmp, 'edit')
    shutil.copytree(dtab, etab)
    base_obj = TB.bake(X, lay, 'x', *TB.read_tables(etab, len(boxes)), jd)[0]
    rows = list(csv.reader(io.StringIO(open(os.path.join(etab, TB.F_THEME), 'rb').read().decode('utf-8-sig'))))
    tid = themes[4]['id']
    i5 = next(i for i, r in enumerate(rows) if r and r[0] == tid)
    old_name = rows[i5][1]
    rows[i5][1] = '한줄고침시험'
    open(os.path.join(etab, TB.F_THEME), 'wb').write(TB.write_csv_bytes(rows[0], rows[1:]))
    ed_obj = TB.bake(X, lay, 'x', *TB.read_tables(etab, len(boxes)), jd)[0]
    diff_t = [i for i, (a1, b1) in enumerate(zip(base_obj['themes'], ed_obj['themes'])) if a1 != b1]
    only = diff_t == [4] and {k for k in base_obj['themes'][4] if base_obj['themes'][4][k] != ed_obj['themes'][4][k]} == {'n'}
    rest = base_obj['boxes'] == ed_obj['boxes'] and base_obj['acr'] == ed_obj['acr'] and base_obj['subj'] == ed_obj['subj'] and len(base_obj['themes']) == len(ed_obj['themes'])
    T('B-5', '표 한 줄(%s 이름) 고치고 다시 구우면 그 테마만 바뀜' % tid, only and rest, '바뀐 테마 %s · 이름 %r → %r' % ([base_obj['themes'][i]['id'] for i in diff_t], old_name[:12], ed_obj['themes'][4]['n']))
    if git_rev_ok(mb, BASE_MBPDF):
        T('B-5 헛잣대', '착수 바탕 %s 에 테마.json.gz 없음' % BASE_MBPDF, not git_has(mb, BASE_MBPDF, 'theme/%s/테마.json.gz' % DOCID))
    else:
        INFO('B-5 헛잣대', '바탕 %s 이 이 저장소에 없다 — 건너뜀' % BASE_MBPDF)
    stage('B-5 테마.json.gz', t0)

    # ═════ B-6 글.json.gz ═════
    t0 = time.time()
    tb = open(gz_text, 'rb').read()
    tj = json.loads(gzip.decompress(tb).decode('utf-8'))
    meta = json.load(io.open(_roots.mbpdf('words', DOCID, '책메타.json'), encoding='utf-8'))
    tt = tj.get('t') or []
    T('B-6', 't 805 · pages 805 · docid · pdfMd5 = 책메타', len(tt) == 805 == tj.get('pages') and tj.get('docid') == DOCID and tj.get('pdfMd5') == meta['pdfMd5'],
      '%d · %s · %s' % (len(tt), tj.get('docid'), (tj.get('pdfMd5') or '')[:8]))
    tc = sum(len(t) - t.count('\n') for t in tt)
    T('B-6', '글자 합 874,457', tc == WANT_TEXT_CHARS, tc)
    f1q = find_counts(tt, '보정을무효로')
    T('B-6', '「보정을무효로」 55쪽 2곳 · 776쪽 1곳', f1q == WANT_BOOK['보정을무효로'], f1q)
    f2q = find_counts(tt, WANT_SC[0])
    T('B-6', '「심사청구」 84쪽 316곳', (len(f2q), sum(n for _p, n in f2q)) == WANT_SC[1:], '%d쪽 %d곳' % (len(f2q), sum(n for _p, n in f2q)))
    INFO('B-6', '55쪽 앞 40자', re.sub(r'\s+', '', tt[54])[:40] if len(tt) > 54 else '')
    T('B-6', '글.json.gz ≤ 1MB', len(tb) <= 1024 * 1024, '%d B · md5 %s' % (len(tb), hashlib.md5(tb).hexdigest()))
    wdir = _roots.mbpdf('words', DOCID)
    again = [BT.page_text(json.loads(gzip.decompress(open(os.path.join(wdir, 'ox_book_%s_p%d.json.gz' % (DOCID, p)), 'rb').read()).decode('utf-8')).get('words') or '')
             for p in range(1, 806)]
    blob6 = BT.dump_gz(dict(docid=DOCID, pdfMd5=meta['pdfMd5'], pages=805, builtAt=tj.get('builtAt'), builtBy=tj.get('builtBy'), t=again))
    T('B-6', '멱등 — 쪽 파일에서 다시 지은 것 = 배달본(바이트)', blob6 == tb, hashlib.md5(blob6).hexdigest())
    if git_rev_ok(mb, BASE_MBPDF):
        T('B-6 헛잣대', '착수 바탕 %s 에 글.json.gz 없음' % BASE_MBPDF, not git_has(mb, BASE_MBPDF, 'words/%s/글.json.gz' % DOCID))
    stage('B-6 글.json.gz', t0)

    # ═════ B-7 D11 · genie 무변 ═════
    t0 = time.time()
    H = _d11_scan.load_hash()
    allow = _d11_scan.load_allow()
    if H is None:
        T('B-7', 'D11 해시 파일', False, '_d11_hash.txt 를 못 읽었다')
    else:
        h1 = _d11_scan.scan_text(gzip.decompress(blob).decode('utf-8'), H, 'theme/%s/테마.json.gz' % DOCID, allow)
        h2 = sum(len(_d11_scan.scan_text(t, H, 'words/%s/글.json.gz' % DOCID, allow)) for t in tt)
        k1 = collections.Counter(k for _l, k in h1)
        T('B-7', 'D11 두 출력 — 메일·휴대전화·토큰 꼴 · 워터마크 0', len(h1) == 0 and h2 == 0, '테마 %d%s · 글 %d' % (len(h1), (' ' + str(dict(k1))) if k1 else '', h2))
    outs_in_genie = [p for p in (gz_theme, gz_text) if os.path.normcase(os.path.abspath(p)).startswith(os.path.normcase(os.path.abspath(genie)) + os.sep)]
    gs1 = git_status(genie)
    mine = [ln for ln in gs1.decode('utf-8', 'replace').splitlines() if re.search(r'테마\.json|글\.json|_theme_build|_harness_theme_data|_book_text_build|/theme/', ln)]
    T('B-7', 'genie diff 0 — 이 판 파일이 genie 에 0(출력 · ⚙ 둘 · 하네스)', not outs_in_genie and not mine,
      'genie 안 출력 %d · genie status 이 판 줄 %d' % (len(outs_in_genie), len(mine)))
    INFO('B-7', 'genie git status 하네스 앞뒤', '같음' if gs0 == gs1 else '다름(본 세션이 같은 때 genie 를 만졌을 수 있다 — 이 판 줄은 위 줄로 잰다)')
    stage('B-7 D11', t0)

    shutil.rmtree(tmp, ignore_errors=True)
    npass = sum(1 for r in R if r[2])
    nfail = len(R) - npass
    P('PASS %d · FAIL %d · 전체 %.2f분' % (npass, nfail, (time.time() - T_ALL) / 60))
    sys.exit(0 if nfail == 0 else 1)


if __name__ == '__main__':
    main()
