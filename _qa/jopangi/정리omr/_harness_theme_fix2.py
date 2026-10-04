# -*- coding: utf-8 -*-
"""관문 A — 조판기 테마 데이터 고침(_task_jo_theme_fix2 §A-6 · 2026-10-02 · 하위 에이전트 E)
   박스 묶음 = 채팅 그림 검수 표(_theme_small_1002.csv) 대로 · 구역 그림 · 테마 점 새 규칙 · 두문자 두 줄 · 이름 둘

  python _harness_theme_fix2.py [--tables <표 폴더>] [--skip-e2e]
  자리: N:(정리omr 주석1 PDF · _테마 표 · jopangi\\task\\_theme_small_1002.csv — need_n) · MBPDF_ROOT(테마.json.gz · img\\ — 읽기만) · GENIE_ROOT(조문 재료 · 읽기만)
  쓰는 것: %TEMP% 시험 굽기(표 사본 · gz · img) 뿐 — N: 표 · 배달 출력은 안 고친다
  헛잣대 = minbeoppdf 착수 바탕 e9e7e8e3 의 테마.json.gz(2841972d — 거리 묶음 · 그림 0 · 옛 점 규칙) · 같은 상자에 옛 거리 규칙을 다시 돌린 셈
  A-1 테마 수 · A-2 박스 191 표대로 · A-3 거리 묶음 0 · A-4 그림 든 테마 · A-5 t71 구역 · A-6 이름·박스·두문자 · A-7 테마 점 · A-8 구역 그림 · A-9 멱등 · A-10 D11
  끝 줄 = 「PASS n · FAIL m」 · 종료 코드 0 = FAIL 0
"""
# --mode gate|regress|smoke (qa_slim 2026-10-04 · 없으면 gate = 지금과 같음 · ⚙ 판 관문)
#   regress = 산출 파일(테마.json.gz · img 폴더) · N: 표만 읽는다 — 주석1 PDF 다시 뽑기(TB.extract · pikepdf 셈) · 옛 배달본 git 꺼내기 · A-9 두 번 굽기(subprocess) · genie git status · 헛잣대 셋은 gate 에서만(굽기 재현성 = ⚙ 판 관문 몫) ·
#             남는 것 = A-1 · A-5(구역 · XML) · A-6 · A-7(t06 · t71 · t09) · A-8(크기) — A-10 D11 은 theme_data B-7(두 출력)이 더 넓게 잰다(합침)
#   smoke   = regress 가운데 A-1(테마 수 · 표 줄 = 굽은 테마)만
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — qa_slim(2026-10-04) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다(argparse 는 그것을 못 본다)
import argparse, collections, csv, gzip, hashlib, io, json, math, os, re, shutil, statistics, subprocess, sys, tempfile, time
import xml.etree.ElementTree as ET

NROOT = _roots.need_n('정리omr 주석1 PDF · _테마 표 · 채팅 그림 검수 표')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _theme_build as TB   # noqa: E402
sys.path.append(NROOT)
import _d11_scan   # noqa: E402

DOCID = 'patent_hr8'
BASE_MBPDF = 'e9e7e8e3'                       # 착수 바탕(배달 테마.json.gz 2841972d)
SMALL = os.path.join(NROOT, 'jopangi', 'task', '_theme_small_1002.csv')
WANT = dict(themes=95, old_themes=70, new_themes=25, kigan=39, kigan_green=18, kigan_text=37, n01_text_task=25, n01_path=24)
N01 = ('t71', 1, [120.0, 0.0, 270.0, 32.0], ['52', '53', '52-2', '67-2'])
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


def md5b(b):
    return hashlib.md5(b).hexdigest()


def git_blob(repo, rev, path):
    r = subprocess.run(['git', '-C', repo, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def rows_of(path):
    return list(csv.reader(io.StringIO(open(path, 'rb').read().decode('utf-8-sig'))))


def center_in(b, p, reg):
    cx, cy = (b['rect'][0] + b['rect'][2]) / 2, (b['rect'][1] + b['rect'][3]) / 2
    return b['p'] == p and reg[0] <= cx <= reg[2] and reg[1] <= cy <= reg[3]


def old_distance_attach(X, nsc, O):
    """헛잣대 — 옛 ⚙ 의 「같은 쪽 사각 거리 가장 가까운 큰 박스에 +k」 규칙을 하네스가 따로 다시 짜서 돌린 붙임 → (붙인 수, 바탕 배달본 묶음과 같은 수)"""
    boxes = X['boxes']
    big = [b['k'] for b in boxes if nsc[b['k']] >= TB.BIG]
    owner = {}
    for t in (O or {}).get('themes', []):
        for k in t['boxes']:
            owner[k] = t['boxes'][0]
    n = same = 0
    for b in boxes:
        if not (0 < nsc[b['k']] < TB.BIG):
            continue
        cand = []
        for g in big:
            if boxes[g]['p'] != b['p']:
                continue
            a, c = b['rect'], boxes[g]['rect']
            dx = max(0.0, max(a[0], c[0]) - min(a[2], c[2]))
            dy = max(0.0, max(a[1], c[1]) - min(a[3], c[3]))
            cand.append((math.hypot(dx, dy), g))
        if cand:
            n += 1
            same += 1 if owner.get(str(b['k'])) == str(min(cand)[1]) else 0
    return n, same


def runs_in(X, lay, p, reg, ks):
    """하네스가 따로 센 구역 text 수 — ks 박스(None = 그 쪽 모든 박스)의 글리프 줄을 구역 안 · 색 바뀜 · 뛴 자리 · 공백 둘에서 끊어 센다"""
    rx0, ry0, rx1, ry1 = reg
    n = 0
    for b in X['boxes']:
        if b['p'] != p or not b['chars'] or (ks is not None and b['k'] not in ks):
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


def inks_in(pdf_path, p, reg):
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


def green_strokes(pdf_path):
    """하네스가 따로 — pikepdf 로 Ink /C · /BS /W 를 읽어 초록·연두 굵기 ≥ 2.5 획(쪽 · 가운데)"""
    import pikepdf
    pdf = pikepdf.open(pdf_path)
    out = []
    for pi, pg in enumerate(pdf.pages):
        H = float(pg.MediaBox[3])
        for a in pg.get('/Annots', []):
            if str(a.get('/Subtype')) != '/Ink':
                continue
            c = tuple(round(float(q), 3) for q in (a.get('/C') or []))
            bs = a.get('/BS')
            w = float(bs.get('/W')) if bs is not None and bs.get('/W') is not None else 1.0
            if c not in ((0.0, 1.0, 0.0), (0.694, 1.0, 0.0)) or w < 2.5:
                continue
            pts = []
            for s in a.get('/InkList', []):
                v = [float(q) for q in s]
                pts += [(v[i], H - v[i + 1]) for i in range(0, len(v) - 1, 2)]
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            out.append((pi + 1, (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, c))
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--tables', help='표 폴더(기본 N: jopangi\\정리omr\\_테마)')
    ap.add_argument('--skip-e2e', action='store_true', help='A-9 처음부터 두 번 굽기를 건너뜀(개발용)')
    a = ap.parse_args()
    d = TB.default_paths()
    tables = a.tables or d['tables']
    mb = _roots.mbpdf()
    gz_path = _roots.mbpdf('theme', DOCID, '테마.json.gz')
    img_dir = os.path.join(os.path.dirname(gz_path), TB.IMG_DIR)
    genie = _roots.genie()
    P('MBPDF_ROOT = %s · GENIE_ROOT = %s · 표 = %s' % (mb, genie, tables))
    T_ALL = time.time()
    tmp = tempfile.mkdtemp(prefix='h_theme_fix2_')

    # ═════ 재료 ═════
    t0 = time.time()
    if QJ.GATE:   # 주석1 PDF 다시 뽑기(TB.extract · layout_all) — regress 는 산출 파일(테마.json.gz)만 읽는다
        X = TB.extract(d['pdf'])
        lay = TB.layout_all(X)
        boxes = X['boxes']
        nsc = {b['k']: sum(1 for c in b['chars'] if c['t'] != ' ') for b in boxes}
    blob = open(gz_path, 'rb').read()
    J = json.loads(gzip.decompress(blob).decode('utf-8'))
    if QJ.GATE:
        QJ.sub('git:show-data')
        ob = git_blob(mb, BASE_MBPDF, 'theme/%s/테마.json.gz' % DOCID)
        O = json.loads(gzip.decompress(ob).decode('utf-8')) if ob else None
    else:
        ob = O = None   # regress — 헛잣대 바탕(옛 배달본)을 git 에서 꺼내지 않는다
    INFO('재료', '배달 테마.json.gz', '%d B · md5 %s · 헛잣대 바탕 %s %s' % (len(blob), md5b(blob), BASE_MBPDF, ('%d B · md5 %s' % (len(ob), md5b(ob))) if ob else '없음'))
    sm = rows_of(SMALL)
    assert sm[0][:6] == ['박스', '쪽', '글자수', '지금', '판정', '갈 곳'], sm[0]
    sm = sm[1:]
    th_rows = rows_of(os.path.join(tables, TB.F_THEME))
    assert th_rows[0] == TB.H_THEME
    themes, acr, subj = TB.read_tables(tables, len(boxes) if QJ.GATE else len(J['boxes']))
    TH = {t['id']: t for t in themes}
    JT = {t['id']: t for t in J['themes']}
    stage('재료', t0)

    # ═════ A-1 테마 수 ═════
    ids = [t['id'] for t in J['themes']]
    T('A-1', '테마 95 = 70 + 25(t71~t95) · 표 줄 = 굽은 테마', len(ids) == WANT['themes'] and ids == ['t%02d' % i for i in range(1, 96)] and [t['id'] for t in themes] == ids,
      '%d(헛잣대 바탕 %s)' % (len(ids), len(O['themes']) if O else '?'))

    if QJ.SMOKE:   # smoke — A-1 만
        shutil.rmtree(tmp, ignore_errors=True)
        npass = sum(1 for r in R if r[2])
        nfail = len(R) - npass
        P('PASS %d · FAIL %d · 전체 %.2f분' % (npass, nfail, (time.time() - T_ALL) / 60))
        sys.exit(0 if nfail == 0 else 1)

    if QJ.GATE:   # A-2 = 주석1 PDF 에서 다시 뽑은 상자(nsc · boxes) · 옛 배달본(git)과 맞댄다 → regress 에서 안 돈다 · A-6 이 쓰는 새 테마 이름 짝(nmap)만 아래 else 에서 만든다
        # ═════ A-2 박스 191 표대로 ═════
        t0 = time.time()
        newids = sorted({r[5] for r in sm if r[5].startswith('N')}, key=lambda s: int(s[1:]))
        nmap = {nid: 't%02d' % (70 + i) for i, nid in enumerate(newids, 1)}
        want_of = {}
        for r in sm:
            dest = r[5]
            want_of[int(r[0])] = None if dest == '두문자 후보' else nmap.get(dest, dest)
        big = [b['k'] for b in boxes if nsc[b['k']] >= TB.BIG]
        if O:
            for t in O['themes']:
                want_of[int(t['boxes'][0])] = t['id']   # 큰 박스 = 옛 테마 첫 칸(무변)
        in_table = {}
        dup = []
        for t in themes:
            for k in t['boxes']:
                if int(k) in in_table:
                    dup.append(int(k))
                in_table[int(k)] = t['id']
        bad_t = [k for k in range(191) if in_table.get(k) != want_of.get(k)]
        T('A-2', '표 — 박스 191 전부 표대로(작은 글 78 · 그림 43 = 채팅 표 「갈 곳」 · 큰 박스 70 = 옛 테마 · 두 번 0)', len(want_of) == 191 and not bad_t and not dup,
          '어긋남 %d %s · 두 번 %d' % (len(bad_t), bad_t[:8], len(dup)))
        # 굽은 꼴 — 박스가 실제로 보이는 테마(줄 칸 · 구역 박스 안)
        shown = {}
        for t in J['themes']:
            tt = TH[t['id']]
            for k in tt['boxes']:
                b = boxes[int(k)]
                if t['region'] and center_in(b, tt['region'][0], tt['region'][1]):
                    rk = t['id'] + 'r'
                    ok = rk in t['boxes'] and J['boxes'][rk]['svg']
                    shown.setdefault(int(k), []).append((t['id'], 'svg' if ok else 'svg?'))
                elif k in t['boxes']:
                    shown.setdefault(int(k), []).append((t['id'], 'line'))
        bad_s = [k for k in range(191) if (want_of.get(k) is None and k in shown) or (want_of.get(k) is not None and [x[0] for x in shown.get(k, [])] != [want_of[k]])]
        T('A-2', '굽은 테마.json — 박스마다 그 테마 한 곳에만(줄 칸 또는 구역 SVG) · 테마 밖 = 16 하나', not bad_s and [k for k in range(191) if k not in shown] == [16],
          '어긋남 %d %s · 테마 밖 %s' % (len(bad_s), bad_s[:8], [k for k in range(191) if k not in shown]))
        same_lines = O is not None and all(J['boxes'][str(k)]['lines'] == O['boxes'][str(k)]['lines'] and J['boxes'][str(k)]['p'] == O['boxes'][str(k)]['p']
                                           and J['boxes'][str(k)]['r'] == O['boxes'][str(k)]['r'] for k in range(191))
        big_ok = O is not None and all(any(x == (t['id'], 'line') for x in shown.get(int(t['boxes'][0]), [])) for t in O['themes'])
        T('A-2', '큰 박스 70 무변 — 박스 191 글 줄(lines·p·r) = 바탕 · 큰 박스는 옛 테마 줄 칸 그대로', same_lines and big_ok and len(big) == 70,
          '글 줄 같음 %s · 큰 박스 자리 %s' % (same_lines, big_ok))
        stage('A-2 박스', t0)

    else:
        newids = sorted({r[5] for r in sm if r[5].startswith('N')}, key=lambda s: int(s[1:]))
        nmap = {nid: 't%02d' % (70 + i) for i, nid in enumerate(newids, 1)}
    if QJ.GATE:   # A-3 = ⚙ 초안(draft_tables · 조문 데이터 jd)을 PDF 상자에서 다시 만들어 맞댄다 → gate 에서만
        # ═════ A-3 거리 묶음 0 ═════
        t0 = time.time()
        plus = sum(1 for r in th_rows[1:] for tk in r[2].split() if tk.startswith('+'))
        jd = TB.load_jodata(d['jodata'])
        dr = TB.draft_tables(X, lay, jd)
        dth = list(csv.reader(io.StringIO(dr['theme'].decode('utf-8-sig'))))[1:]
        dsmall = sum(1 for r in dth for tk in r[2].split() if 0 < nsc[int(tk.lstrip('+'))] < TB.BIG or nsc[int(tk.lstrip('+'))] == 0)
        src = open(os.path.join(HERE, '_theme_build.py'), 'rb').read().decode('utf-8')
        code_dist = len(re.findall(r'rect_dist|\+%d', src))
        old_n = sum(len(t['boxes']) - 1 for t in O['themes']) if O else None
        T('A-3', '거리로 붙인 박스 0 — 표 「+k」 0 · ⚙ 초안 작은 조각·그림 0 · ⚙ 안 거리 묶음 코드(rect_dist · 「+%d」) 0', plus == 0 and dsmall == 0 and code_dist == 0,
          '표 + %d · 초안 %d · 코드 %d' % (plus, dsmall, code_dist))
        hz, hz_same = old_distance_attach(X, nsc, O)
        T('A-3 헛잣대', '바탕 배달본 = 거리로 붙은 작은 조각 78 · 같은 상자에 옛 거리 규칙을 하네스가 따로 돌리면 78 붙고 78 이 바탕 묶음과 같음', old_n == 78 and hz == 78 and hz_same == 78,
          '바탕 %s · 다시 돌림 %d · 같음 %d' % (old_n, hz, hz_same))
        stage('A-3 거리', t0)

    if QJ.GATE:   # A-4 = 그림 도장 43 을 PDF 에서 다시 센다(pic_info) → gate 에서만
        # ═════ A-4 그림 도장이 든 테마 ═════
        t0 = time.time()
        pics = [k for k in range(191) if nsc[k] == 0]
        want_pt = collections.defaultdict(list)
        for k in pics:
            if want_of.get(k):
                want_pt[want_of[k]].append(k)
        got_pt = collections.defaultdict(list)
        for k in pics:
            for tid, how in shown.get(k, []):
                got_pt[tid].append(k)
        T('A-4', '그림 도장 43 이 든 테마 = 표대로(테마 %d · 그림 %d)' % (len(want_pt), sum(len(v) for v in want_pt.values())),
          dict(want_pt) == dict(got_pt) and len(pics) == 43, '굽은 테마 %d · 그림 %d' % (len(got_pt), sum(len(v) for v in got_pt.values())))
        old_pt = sum(1 for t in O['themes'] if any(nsc[int(k)] == 0 for k in t['boxes'] if k.isdigit())) if O else None
        T('A-4 헛잣대', '바탕 배달본 = 그림 도장이 든 테마 0', old_pt == 0, old_pt)
        drawn = {}
        for t in J['themes']:
            rk = t['id'] + 'r'
            if rk in t['boxes']:
                svg = J['boxes'][rk]['svg']
                for m in re.finditer(r'href="theme/patent_hr8/img/(\d+)\.webp"', svg):
                    drawn[int(m.group(1))] = t['id']
        vec = [k for k in pics if TB.pic_info(X, k)['kind'] == 'vec']
        emp = [k for k in pics if TB.pic_info(X, k)['kind'] == 'empty']
        nodraw = sorted(k for k in pics if k not in drawn and k not in vec and k not in emp)
        INFO('A-4', '그림 도장 갈래', '그림 %d(구역 SVG <image> %d) · 벡터 %d %s · 모양 없음 %s · 그림인데 구역 밖(구역 미상) %s' % (
            len(pics) - len(vec) - len(emp), len(drawn), len(vec), vec, emp, nodraw))
        stage('A-4 그림', t0)

    # ═════ A-5 t71 구역 ═════
    t0 = time.time()
    tid, p1, reg1, jo1 = N01
    t71 = JT.get(tid, {})
    svg = J['boxes'].get(tid + 'r', {}).get('svg') or ''
    nt, npth = svg.count('<text '), svg.count('<path ')
    mem = {int(k) for k in TH[tid]['boxes']}
    if QJ.GATE:   # 따로 셈(PDF 글리프 줄 · pikepdf Ink) = 굽기 재현성 쪽 → gate 에서만
        want_t_mem = runs_in(X, lay, p1, reg1, mem)
        want_t_all = runs_in(X, lay, p1, reg1, None)
        want_p = inks_in(d['pdf'], p1, reg1)
    T('A-5', 't71 {분변분재 기간} 구역 = 1쪽 120 0 270 32 · 박스 39 40 41 44 · 구역 박스 하나',
      TH[tid]['region'] and TH[tid]['region'][0] == p1 and TH[tid]['region'][1] == reg1 and sorted(mem) == [39, 40, 41, 44] and t71.get('boxes') == [tid + 'r'],
      '%s · %s' % (TH[tid]['region'], t71.get('boxes')))
    if QJ.GATE:   # path 24 · text = 구역 박스 run 따로 셈 · 지시서 25 갈음 INFO — 위 따로 셈과 맞대는 칸 → gate 에서만(regress 는 구역 위치 · XML · 크기 칸이 남는다)
        T('A-5', 't71 구역 SVG path 24 = 그 사각 안 Ink(pikepdf 로 따로 셈) · theme_data B-4 값 ±0', npth == want_p == WANT['n01_path'], '%d · %d' % (npth, want_p))
        T('A-5', 't71 구역 SVG text = 구역 테마 박스(39·40·41·44) run(하나하나 따로 셈) — 지시서 25(갈음 · 아래 줄)', nt == want_t_mem and nt > 0,
          '%d · %d' % (nt, want_t_mem))
        INFO('A-5', '지시서 「text 25(theme_data B-4 값 ±0)」 갈음', '구역 안 모든 박스 run = %d(theme_data B-4 정의) − 구역 박스 run %d = %d · 차 = 테마 밖 k16 「성산신진불확선명1」 앞 6자 조각(구역 오른쪽 끝 x 270 에서 잘림) — fix2 는 구역 SVG 에 그 테마 박스 글자만 그린다(채팅 첫 실측 24 와 같음)' % (
            want_t_all, want_t_mem, want_t_all - want_t_mem))
    try:
        ET.fromstring(svg)
        okx = True
    except Exception:
        okx = False
    T('A-5', 't71 SVG XML 성함 · 「성산」 조각 0 · 크기 ≤ 60KB', okx and '성산' not in svg and len(svg.encode('utf-8')) <= 60 * 1024, '%d B' % len(svg.encode('utf-8')))
    stage('A-5 t71', t0)

    # ═════ A-6 이름 · 박스 · 두문자 ═════
    T('A-6', 't03 n = 주체능력 · t06 n = 기일기간 · t06 boxes = [\'6\']', JT['t03']['n'] == '주체능력' and JT['t06']['n'] == '기일기간' and JT['t06']['boxes'] == ['6'],
      '%s · %s · %s' % (JT['t03']['n'], JT['t06']['n'], JT['t06']['boxes']))
    T('A-6', "acr['분변분재'].jo = 52·53·52-2·67-2 · 뜻 빈칸 · t71 조 = 같음", J['acr'].get('분변분재', {}).get('jo') == jo1 and J['acr']['분변분재']['m'] == '' and JT[tid]['jo'] == jo1,
      J['acr'].get('분변분재'))
    T('A-6', '「테마 밖」 16 = 두문자 후보 줄 「성산신진불확선명1」(뜻 빈칸)', J['acr'].get('성산신진불확선명1') == {'m': '', 'jo': []}, J['acr'].get('성산신진불확선명1'))
    if O:
        INFO('A-6', '두문자 수', '%d → %d(+분변분재 · +성산신진불확선명1 · 나머지 377 무변 %s)' % (len(O['acr']), len(J['acr']), all(J['acr'].get(w) == v for w, v in O['acr'].items())))
    newn = {nmap[r[5]]: r[6] for r in sm if r[5].startswith('N')}
    T('A-6', '새 줄 이름 = 표 「갈 곳 이름」(25)', all(JT[t]['n'] == n for t, n in newn.items()) and len(newn) == 25, '%d' % len(newn))

    # ═════ A-7 테마 점 ═════
    t0 = time.time()
    dist = collections.Counter(''.join(map(str, t['bk'])) for t in J['themes'])
    INFO('A-7', 'bk(내용·주체·기간) 분포', ' · '.join('(%s) %d' % (','.join(k), n) for k, n in sorted(dist.items(), reverse=True)))
    on = [t['id'] for t in J['themes'] if t['bk'][2]]
    if QJ.GATE:   # 초록·연두 획(pikepdf) → 가운데가 든 박스(PDF 상자) → 표 테마 = 굽기 재현성 쪽 → gate 에서만
        # 하네스가 따로 — 초록 획(pikepdf) → 가운데가 든 박스(둘이면 가장 가까운 글자) → 표 테마 · 「기간」 글(박스 줄 글 · 구역 SVG text)
        gs = green_strokes(d['pdf'])
        marks = TB.green_marks(X, lay)
        gth = set()
        for (p, cx, cy, c), m in zip(gs, marks):
            assert m['p'] == p and abs(m['cx'] - cx) < 0.01 and abs(m['cy'] - cy) < 0.01
            k = m['k']
            for t in themes:
                if (k is not None and str(k) in t['boxes']) or (t['region'] and t['region'][0] == p and t['region'][1][0] <= cx <= t['region'][1][2] and t['region'][1][1] <= cy <= t['region'][1][3]):
                    gth.add(t['id'])
    kth = set()
    for t in J['themes']:
        txt = []
        for k in t['boxes']:
            bx = J['boxes'][k]
            if bx['svg']:
                txt += [m.group(1) for m in re.finditer(r'<text [^>]*>([^<]*)</text>', bx['svg'])]
            else:
                txt += [''.join(r['t'] for r in ln['runs']) for ln in bx['lines']]
        if any(TB.KIGAN in s for s in txt):
            kth.add(t['id'])
    if QJ.GATE:   # 기간 켜짐 39 = 획 18 ∪ 글 37(하네스가 따로 셈) — 획은 PDF → gate 에서만
        want_on = sorted(gth | kth, key=lambda s: int(s[1:]))
        T('A-7', '기간 켜짐 39 = 초록·연두 획 테마 18 ∪ 「기간」 글 테마 37(지시서 채팅 셈과 같은 수 · 하네스가 따로 셈 = 굽은 bk)',
          len(on) == WANT['kigan'] and len(gth) == WANT['kigan_green'] and len(kth) == WANT['kigan_text'] and on == want_on,
          '%d(획 %d · 글 %d · 따로 셈 %d) · 초록 획 %d(쪽 %s)' % (len(on), len(gth), len(kth), len(want_on), len(gs), dict(collections.Counter(g[0] for g in gs))))
    INFO('A-7', '기간 켜진 테마(채팅 목록 대조용)', ' '.join(on))
    if QJ.GATE:
        INFO('A-7', '초록·연두 획 테마', ' '.join(sorted(gth, key=lambda s: int(s[1:]))))
    INFO('A-7', '「기간」 글 테마', ' '.join(sorted(kth, key=lambda s: int(s[1:]))))
    T('A-7', '{기일기간}(t06) · {분변분재 기간}(t71) · t09 기간 켜짐', all(JT[x]['bk'][2] for x in ('t06', 't71', 't09')), [JT[x]['bk'] for x in ('t06', 't71', 't09')])
    if QJ.GATE:   # 주체 점 · 내용 점 따로 셈(박스 글줄 · 조문 데이터 jd) · 헛잣대(바탕 배달본 · 옛 규칙) → gate 에서만
        subj_l = sorted(set(subj))
        sb_bad = []
        for t in J['themes']:
            txt = []
            for k in t['boxes']:
                bx = J['boxes'][k]
                txt += [''.join(r['t'] for r in ln['runs']) for ln in bx['lines']] if not bx['svg'] else []
            tt = TH[t['id']]
            if t['region']:
                p, reg = tt['region']
                for k in tt['boxes']:
                    b = boxes[int(k)]
                    if center_in(b, p, reg):
                        for gl in lay[int(k)]['glines']:
                            txt.append(''.join(g['t'] for g in gl['g'] if reg[0] <= (g['x0'] + g['x1']) / 2 <= reg[2] and reg[1] <= gl['b'] - g['size'] * 0.35 <= reg[3]))
            s_on = 1 if any(w in s for s in txt for w in subj_l) else 0
            c_on = TB.bk_of(tt['jo'], jd['bk'])[0]
            if [c_on, s_on] != t['bk'][:2]:
                sb_bad.append(t['id'])
        T('A-7', '주체 점 = 테마 글에 주체 목록 낱말 · 내용 점 = 테마 조 내용 빈칸(옛 규칙) — 하네스가 따로 셈 = 굽은 bk', not sb_bad, sb_bad[:6])
        if O:
            od = collections.Counter(''.join(map(str, t['bk'])) for t in O['themes'])
            INFO('A-7 헛잣대', '바탕 배달본(인용 조 OR)', ' · '.join('(%s) %d' % (','.join(k), n) for k, n in sorted(od.items(), reverse=True)) + ' · 기간 켜짐 %d/%d' % (
                sum(1 for t in O['themes'] if t['bk'][2]), len(O['themes'])))
            T('A-7 헛잣대', '바탕 기간 켜짐 55/70(옛 규칙 = 못 거름) ≠ 새 39/95', sum(1 for t in O['themes'] if t['bk'][2]) == 55 and len(on) != 55)
        oldrule = sum(1 for t in themes if TB.bk_of(t['jo'], jd['bk'])[2])
        INFO('A-7 헛잣대', '같은 새 표에 옛 규칙(인용 조 OR)', '기간 켜짐 %d/%d' % (oldrule, len(themes)))
    stage('A-7 점', t0)

    # ═════ A-8 구역 그림 ═════
    t0 = time.time()
    if QJ.GATE:   # 구역 SVG 글자 = 구역 박스 글자 · <image> = img webp · 화소/pt(PDF 상자 · pic_info 로 다시 센다) → gate 에서만
        regions = [t for t in J['themes'] if t['region']]
        xml_bad, lost, foreign, href_bad, img_bad, big_dim = [], 0, [], [], [], []
        files = sorted(f for f in os.listdir(img_dir)) if os.path.isdir(img_dir) else []
        from PIL import Image
        for t in regions:
            tt = TH[t['id']]
            p, reg = tt['region']
            svg = J['boxes'][t['id'] + 'r']['svg']
            try:
                ET.fromstring(svg)
            except Exception:
                xml_bad.append(t['id'])
            mem = {int(k) for k in tt['boxes'] if center_in(boxes[int(k)], p, reg) and nsc[int(k)] > 0}
            # SVG 글자 = 구역 박스 글자 중 구역 안(남의 글자 0 · 빠진 글자 0)
            want_chars = sum(1 for k in mem for gl in lay[k]['glines'] for g in gl['g'] if g['t'] != ' ' and reg[0] <= (g['x0'] + g['x1']) / 2 <= reg[2] and reg[1] <= gl['b'] - g['size'] * 0.35 <= reg[3])
            out_chars = sum(1 for k in mem for gl in lay[k]['glines'] for g in gl['g'] if g['t'] != ' ' and not (reg[0] <= (g['x0'] + g['x1']) / 2 <= reg[2] and reg[1] <= gl['b'] - g['size'] * 0.35 <= reg[3]))
            lost += out_chars
            got_chars = sum(len(re.sub(r'\s', '', ET.fromstring('<a>%s</a>' % m.group(1)).text or '')) for m in re.finditer(r'<text [^>]*>([^<]*)</text>', svg))
            if got_chars != want_chars:
                foreign.append((t['id'], got_chars, want_chars))
            for m in re.finditer(r'<image [^>]*href="([^"]*)"', svg):
                h = m.group(1)
                mm = re.match(r'^theme/patent_hr8/img/(\d+)\.webp$', h)
                if not mm or not os.path.isfile(os.path.join(img_dir, '%s.webp' % mm.group(1))):
                    href_bad.append((t['id'], h[:40]))
                    continue
                k = int(mm.group(1))
                im = Image.open(os.path.join(img_dir, '%d.webp' % k))
                r = boxes[k]['rect']
                nat = TB.pic_info(X, k)['nat']
                if abs(im.size[0] - nat[0]) > 1 or abs(im.size[1] - nat[1]) > 1:
                    img_bad.append((k, im.size, nat))
                big_dim.append(min(im.size[0] / (r[2] - r[0]), im.size[1] / (r[3] - r[1])))
        T('A-8', '구역 %d — SVG XML 성함 · 구역 박스 글자 = SVG 글자(남의 박스 글자 0) · 구역 박스 글자 중 구역 밖 0' % len(regions),
          not xml_bad and not foreign and lost == 0, 'XML %s · 글자 어긋남 %s · 구역 밖 %d' % (xml_bad, foreign[:4], lost))
        nimg = sum(J['boxes'][t['id'] + 'r']['svg'].count('<image ') for t in regions)
        T('A-8', '<image> %d = img\\ webp %d · href = theme/patent_hr8/img/<k>.webp · 원본 그림 화소 그대로(±1) · 화소/pt ≥ 2(흐림 없이 2배 이상)' % (nimg, len(files)),
          not href_bad and not img_bad and nimg == len(files) == len(drawn) and big_dim and min(big_dim) >= 2,
          'href 틀림 %s · 화소 틀림 %s · 화소/pt 최소 %.1f' % (href_bad[:3], img_bad[:3], min(big_dim) if big_dim else 0))
    else:
        files = sorted(f for f in os.listdir(img_dir)) if os.path.isdir(img_dir) else []
    tot = sum(os.path.getsize(os.path.join(img_dir, f)) for f in files)
    T('A-8', '테마.json.gz ≤ 1MB(그림은 따로 — data URI 로 넣으면 1MB 넘음)', len(blob) <= 1 << 20 and 'data:image' not in json.dumps(J['boxes'], ensure_ascii=False),
      '%d B · img %d 장 %d B' % (len(blob), len(files), tot))
    stage('A-8 그림', t0)

    if QJ.GATE:   # A-9 = 처음부터 두 번 굽기(subprocess 둘 · PYTHONHASHSEED 1·2) → gate 에서만 · 같은 일을 theme_data B-5 도 하나(합침 → 이 칸이 더 엄하다: webp 34 장 md5 까지)
        # ═════ A-9 멱등 ═════
        t0 = time.time()
        if a.skip_e2e:
            INFO('A-9', '건너뜀(--skip-e2e)')
        else:
            res = []
            for seed in ('1', '2'):
                ctab = os.path.join(tmp, 'tab%s' % seed)
                shutil.copytree(tables, ctab, ignore=shutil.ignore_patterns('_check.md'))
                outp = os.path.join(tmp, 'e2e%s' % seed, 'theme', DOCID, '테마.json.gz')
                env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONIOENCODING='utf-8')
                r = subprocess.run([sys.executable, os.path.join(HERE, '_theme_build.py'), '--tables', ctab, '--out', outp, '--no-pdf1'], capture_output=True, env=env)
                if r.returncode or not os.path.isfile(outp):
                    res.append(('rc%d' % r.returncode, {}))
                    continue
                idir = os.path.join(os.path.dirname(outp), TB.IMG_DIR)
                res.append((md5b(open(outp, 'rb').read()), {f: md5b(open(os.path.join(idir, f), 'rb').read()) for f in sorted(os.listdir(idir))}))
            mine = {f: md5b(open(os.path.join(img_dir, f), 'rb').read()) for f in files}
            T('A-9', '멱등 — 처음부터 두 번 굽기(PYTHONHASHSEED 1·2) gz md5 · webp %d 장 md5 = 배달본' % len(files),
              res[0][0] == res[1][0] == md5b(blob) and res[0][1] == res[1][1] == mine, '%s · %s · 배달 %s · webp 같음 %s' % (res[0][0], res[1][0], md5b(blob), res[0][1] == res[1][1] == mine))
        stage('A-9 멱등', t0)

    # ═════ A-10 D11 ═════
    t0 = time.time()
    if QJ.GATE:   # A-10 D11 = theme_data B-7(두 출력 · 테마 + 글)이 더 넓게 잰다(합침) · genie git status(subprocess) = 이 판 인도 때만 → gate 에서만
        H = _d11_scan.load_hash()
        if H is None:
            T('A-10', 'D11 해시 파일', False, '_d11_hash.txt 를 못 읽었다')
        else:
            hits = _d11_scan.scan_text(gzip.decompress(blob).decode('utf-8'), H, 'theme/%s/테마.json.gz' % DOCID, _d11_scan.load_allow())
            T('A-10', 'D11 테마.json(글 · SVG) — 메일·휴대전화·토큰 꼴 · 워터마크 0', not hits, len(hits))
        in_genie = os.path.normcase(os.path.abspath(img_dir)).startswith(os.path.normcase(os.path.abspath(genie)) + os.sep)
        gs1 = subprocess.run(['git', '--no-optional-locks', '-C', genie, '-c', 'core.quotepath=false', 'status', '--porcelain'], capture_output=True).stdout.decode('utf-8', 'replace')
        mine_g = [ln for ln in gs1.splitlines() if re.search(r'테마\.json|/theme/|\.webp|_theme_build|_harness_theme', ln)]
        T('A-10', '글·그림 = 비공개 minbeoppdf 에만 — genie 안 출력 0 · genie status 이 판 줄 0', not in_genie and not mine_g, '%s · %d' % (in_genie, len(mine_g)))
    stage('A-10 D11', t0)

    shutil.rmtree(tmp, ignore_errors=True)
    npass = sum(1 for r in R if r[2])
    nfail = len(R) - npass
    P('PASS %d · FAIL %d · 전체 %.2f분' % (npass, nfail, (time.time() - T_ALL) / 60))
    sys.exit(0 if nfail == 0 else 1)


if __name__ == '__main__':
    main()
