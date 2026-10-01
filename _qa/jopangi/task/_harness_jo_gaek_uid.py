# -*- coding: utf-8 -*-
r"""_task_jo_gaek_uid(+ _add1) 관문 하네스 — 데이터(원장 · jo/data) · 앱(별칭 찾기 · 기록 키 · 기출뷰 · 머리글 · ⭐ 옮기기) · 산재법 PDF.

  NEW 앱 = --new <파일>(없으면 genie 작업트리 jo/index.html) · NEW 데이터 = --data <폴더>(없으면 genie 작업트리 jo/data)
  BASE = genie HEAD — 앱 a9d72c1(md5 c9a35c4f) · 데이터 f3b74c9 (git show) · 헛잣대 = 바탕에서 FAIL(관문 규칙 3).
         바탕이 원래 통과하는 칸(유일 등)은 「일부러 깨뜨린 사본」 을 헛잣대로 쓴다(잣대가 거저 참이 아님을 보이려고).
  누름 = page.mouse.click(x, y) · 타자 = page.keyboard(관문 규칙 1 · el.click() 안 씀) · 보임 = display ≠ none 이고 높이 > 0(규칙 2).
  원격 기록 = studyplandata 클론 jopangi/기록.json 사본을 SEED 가 창마다 메모리(__REMOTE)로 대답(route 로 바깥 網 막음).
  PDF = --pdf <폴더>(쪼갠 ABBYY 판 다섯 · 없으면 TEMP/uid_abbyy) · 기출서재 앱 = genie gichul/index.html(+ 새 list.json 사본)

쓰기 : python _harness_jo_gaek_uid.py [--new 파일] [--data 폴더] [--pdf 폴더] [--out 폴더] [--only data,app,star,pdf,reg]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
NR = _roots.n()   # env_lanes_fix(9/29) — N: 작업 폴더 · 없으면(클라우드) None — 쓰는 자리가 건너뛴다
import csv, glob, hashlib, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse, collections
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(10 ** 9)
CJH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '공통', '_harness')   # env_lanes_fix(9/29) — 이 파일 자리 기준(N: · genie _qa 같은 모양 · 옛: N: 고정 자리)
sys.path.insert(0, CJH)
import _harness_canvas_jari as CJ          # noqa: E402 — SEED · VENDOR · route_filter · NOISE
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
JP = os.path.dirname(HERE)
sys.path.insert(0, JP)
import uid_rule as UR      # noqa: E402
import p7_head as PH       # noqa: E402
OUT = ARG('--out', HERE)
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
GENIE = CJ.GENIE
JOD = os.path.join(GENIE, 'jo')
DATA = ARG('--data', os.path.join(JOD, 'data'))
NEWF = ARG('--new', os.path.join(JOD, 'index.html'))
PDFD = ARG('--pdf', os.path.join(tempfile.gettempdir(), 'uid_abbyy'))
BASE_REV, BASE_MD5, BASE_DATA_REV = 'a9d72c1', 'c9a35c4f', 'f3b74c9'
WORK = os.path.join(tempfile.gettempdir(), 'h_gaekuid')
TESTS = io.open(os.path.join(HERE, '_harness_jo_gaek_uid_tests.js'), encoding='utf-8').read()
READY = "!!window.__HU&&typeof render==='function'"
LED = os.path.join(JP, u'특상디', u'_1차객_원장.csv')
UDIR = os.path.join(JP, u'특상디', u'_uid')
TOC = os.path.join(JP, u'특상디', u'_1차객_목차.json')
REC = _roots.spd(r'jopangi\기록.json')
SCAN = (2009, 2010, 2020, 2022, 2025)
LAWS = (u'특허', u'상표', u'디보')
LAB = u'[1-7ㄱㄴㄷㄹㅁㅂㅅ가나다라마바사]'
STMT = re.compile(u'^(?:[TSD]\\d{6}' + LAB + u'(?:[hr]\\d?)?|[TSD]R\\d{4}' + LAB + u'|T[HJ]\\d{6}' + LAB + u'?|TX\\d{4}' + LAB + u'?|[TSD]RU\\d{4}' + LAB + u'|T8N\\d{4})$')   # ★ A-6(a) 9/30 p8up A-1-8 새 uid 머리 T8N(8판 새 카드 19) · ★ uid_add2 §D(9/27) — 연도 모르는 리담 문항 = TRU+PM 번호(TRU0506ㄱ)
QKEY = re.compile(u'^[TSD]\\d{6}$')          # 제7판 객관식(문항째) 열쇠 = 법+연도2+회차2+문번2
SERVERS, RES = {}, []


def git(*a, repo=GENIE):
    return subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:420]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (grp, name, d[:420]), flush=True)


def jnew(name):
    return json.load(io.open(os.path.join(DATA, name), encoding='utf-8'))


def jhead(name):
    return json.loads(git('show', '%s:jo/data/%s' % (BASE_DATA_REV, name)).decode('utf-8'))


def stmts(get):
    """(법, uid, 글, 정답, 해, 어디) — 리담 지문(jimun_법) + 제7판 지문(jimun_7pan · 법 = 특허)"""
    out = []
    for law in LAWS:
        for q in get('jimun_%s.json' % law)[u'문제']:
            for z in q[u'지문']:
                out.append((law, z.get('uid') or '', z.get('t') or '', z.get('ox') or '', q[u'연도'], 'L:%s#%s' % (q['id'], z['n'])))
    P = get('jimun_7pan.json')
    for z in P[u'지문']:
        p8 = z.get(u'판8') or {}   # ★ A-6(a) 9/30 — p8up A-1-2·3: 제7판 줄 글·답이 8판으로 바뀌어도 uid 는 7판 글로 지은 그대로(열쇠 무변) → uid 대조(C2·C3)는 7판 글(판8.t7)·옛 답(판8.a7)으로
        out.append((u'특허', z.get('uid') or '', p8.get('t7') or z.get('t') or '', p8.get('a7') or z.get('ox') or '', '', 'P:' + z['id']))
    return out


# ══════════ 데이터 관문 ══════════
def g_form(S, tag):
    bad = [(w, u) for law, u, t, ox, y, w in S if not u or not STMT.match(u)]
    ge51 = [u for *_, u2, t, ox, y, w in [(None,) + s for s in S] for u in [u2] if re.match(u'^[TSD]\\d{6}', u) and int(u[5:7]) >= 51]
    p7 = [u for law, u, *_ in S if 'P7' in u]
    return bad, ge51, p7


def data_gates():
    NEWS, HEADS = stmts(jnew), stmts(jhead)
    # C-1 꼴 전수
    for S, tag in ((NEWS, 'NEW'), (HEADS, 'BASE')):
        bad, ge51, p7 = g_form(S, tag)
        if tag == 'NEW':   # uid 없음이 맞는 줄 = 조합 선지 줄(「ㄱ, ㄴ」 · 2026-63 상표 28·디보 36) — 지시서 A-1
            bad = [(w, u) for w, u in bad if not (not u and any(s[5] == w and UR.is_combo_text(s[2]) for s in S))]
        led = list(csv.DictReader(io.open(LED, encoding='utf-8-sig', newline=''))) if tag == 'NEW' else []
        lbad = [r[u'소스'] for r in led if r['uid'] and not (STMT.match(r['uid']) or QKEY.match(r['uid']))] + \
               [r[u'소스'] for r in led if r.get('uid7') and not STMT.match(r['uid7'])]
        noid = [r[u'소스'] for r in led if not r['uid'] and not (r[u'형식'] == u'오지선다' or UR.is_combo_text(r[u'문제']))]
        objs = (jnew if tag == 'NEW' else jhead)('jimun_7pan.json')[u'객관식']
        obad = [z['id'] for z in objs if not (z.get('uid') and (STMT.match(z['uid']) or QKEY.match(z['uid'])))]
        ok = not bad and not ge51 and not p7 and not lbad and not noid and not obad
        T('C1' if tag == 'NEW' else 'C1-헛', u'꼴 전수(%s)' % tag, ok if tag == 'NEW' else not ok,
          u'지문 %d · 꼴 밖·빈 uid %d %s · 문번≥51 %d · P7 꼬리 %d · 원장 꼴 밖 %d · 원장 uid 없음(조합 아님) %d · 객관식 꼴 밖 %d' %
          (len(S), len(bad), bad[:3], len(ge51), len(p7), len(lbad), len(noid), len(obad)))
    # C-2 유일 — 법 안에서 같은 uid = 같은 (정규화 글, 정답)
    def uniq_bad(S):
        # 같은 uid = 같은 정규화 글 · 정답은 O·X 끼리만 맞댄다(리담 정답 칸이 빈 줄 = 모름 · 다름이 아니다 — 응시2021 4번째 ③~⑤)
        m, a = collections.defaultdict(set), collections.defaultdict(set)
        for law, u, t, ox, y, w in S:
            if u:
                m[(law, u)].add(UR.norm(t))
                if ox in ('O', 'X'):
                    a[(law, u)].add(ox)
        return [k for k in m if len(m[k]) > 1 or len(a[k]) > 1]
    nb = uniq_bad(NEWS)
    T('C2', u'유일 — 글·정답이 다른데 uid 같음', not nb, u'%d %s' % (len(nb), nb[:3]))
    hb = uniq_bad(HEADS)
    if hb:
        T('C2-헛', u'유일 헛잣대(바탕)', True, u'바탕 FAIL %d %s' % (len(hb), hb[:3]))
    else:   # 바탕도 유일 — 일부러 두 글에 같은 uid 를 준 사본으로 잣대가 거저 참이 아님을 보인다
        fake = list(NEWS)
        a = next(i for i, s in enumerate(fake) if s[1] and s[0] == u'특허')
        b = next(i for i, s in enumerate(fake) if s[1] and s[0] == u'특허' and UR.norm(s[2]) != UR.norm(fake[a][2]))
        fake[b] = (fake[b][0], fake[a][1]) + fake[b][2:]
        T('C2-헛', u'유일 헛잣대(바탕도 유일 → 깨뜨린 사본)', bool(uniq_bad(fake)), u'바탕 0 · 사본 %d' % len(uniq_bad(fake)))
    # C-3 같은 글 한 uid
    def same_bad(S):
        m = collections.defaultdict(set)
        for law, u, t, ox, y, w in S:
            n = UR.norm(t)
            if n and n not in UR.PLACEHOLDER:
                m[(law, ox, n)].add(u)
        return [(k[0], sorted(v)) for k, v in m.items() if len(v) > 1]
    ns, hs = same_bad(NEWS), same_bad(HEADS)
    T('C3', u'같은 글 한 uid', not ns, u'어긋난 묶음 %d %s' % (len(ns), ns[:2]))
    T('C3-헛', u'같은 글 헛잣대(바탕)', bool(hs), u'바탕 %d 묶음(채팅 셈 92 안팎)' % len(hs))
    # C-4 2008 이후 — TR·TH 로 남은 수 = 못 찾음 목록 · §B 표본
    M = json.load(io.open(os.path.join(UDIR, 'exam_match.json'), encoding='utf-8'))
    U = M['units']
    # 못 찾음 목록 = 시험지에서 자리를 못 찾아 TR·SR·DR / TH 로 **남은** 지문(같은 글 합치기로 다른 uid 를 받은 것은 목록 밖)
    nfL = sorted(k for k, v in U.items() if v['how'] == 'R-notfound' and re.match(u'^[TSD]R', v['uid']))
    nfP = sorted(k for k, v in U.items() if v['how'] == 'H-notfound' and v['uid'].startswith('TH') and k != 'P|P7-1599')   # ★ A-6(a) 9/30 — p8up A-1-1 이 원장에서 지운 P7-1599(TH111599)는 N: 목록에만 남음
    ids_new = collections.Counter()
    objs_new = jnew('jimun_7pan.json')[u'객관식']
    for law, u, t, ox, y, w in NEWS + [(u'특허', z.get('uid') or '', '', '', '', 'P:' + z['id']) for z in objs_new]:   # 객관식 문항(P7-0390·0549)도
        if w.startswith('L:') and re.match(u'^[TSD]R', u) and y and int(y) >= 2008:
            ids_new['L'] += 1
        if w.startswith('P:') and u.startswith('TH'):
            v = U.get('P|' + w[2:])
            if v and v['how'] == 'H-notfound':
                ids_new['P'] += 1
    T('C4', u'2008 이후 TR·TH 로 남은 지문 = 못 찾음 목록', ids_new['L'] == len(nfL) and ids_new['P'] == len(nfP),
      u'리담 %d = 목록 %d · 제7판 %d = 목록 %d' % (ids_new['L'], len(nfL), ids_new['P'], len(nfP)))
    ledl = list(csv.DictReader(io.open(LED, encoding='utf-8-sig', newline='')))
    led = {r[u'소스']: r for r in ledl}

    def by_old(o):   # 옛 uid → 그 행들의 새 uid(리담 쪽 uid · 제7판 쪽 uid7)
        return sorted(set(x for r in ledl if o in (r.get(u'옛uid') or '').split('|') for x in (r['uid'], r.get('uid7')) if x))
    B8 = [('T1350717', 'T1350065'), ('T1350514', 'T1350065h'), ('T0845085', u'T084508ㅁ'), ('T0845511P7', u'T084508ㅁ'), ('T0845021', u'T084502ㄱr')]
    got = [(o, by_old(o), w) for o, w in B8]
    T('C4', u'§B 표본(2008 이후)', all(w in g for _, g, w in got), got)
    # 지시서 표 조건부 표본 — 시험지 대조가 가른 값(보고 · T0946093 「시험지와 같으면」 · T0845101 → 지시서 T084510ㄱ)
    N('C4', u'§B 조건부 표본', [(o, by_old(o)) for o in ('T0946093', 'T0946093P7', 'T0845101')])
    hp = {z['id']: z for z in jhead('jimun_7pan.json')[u'지문']}
    T('C4-헛', u'§B 표본 헛잣대(바탕 데이터)', (hp.get('P7-0036') or {}).get('uid') != 'T1350065h', u'바탕 P7-0036 uid %s' % (hp.get('P7-0036') or {}).get('uid'))
    # C-5 2007 이전·사법·미기출 · 법 섞임
    B7 = [('T0340742', ['TR03071']), ('T0542513', ['TR03071']), ('T0542511', ['TH050004', 'SR03093']), ('T9734727', [u'TR9704가'])]
    got = [(o, by_old(o), w) for o, w in B7]
    p1 = led['P7-0001']['uid']
    s28 = [r['uid'] for r in ledl if (r.get(u'옛uid') or '') == 'S2663281']
    T('C5', u'§B 표본(2007 이전·사법·조합)', all(set(w) <= set(g) for _, g, w in got) and p1 == 'TJ080001' and s28 == [''],
      {'표': got, 'P7-0001': p1, 'S2663281 행 uid': s28})
    LC = {u'특허': 'T', u'상표': 'S', u'디보': 'D'}
    mix = [s for s, r in led.items() if r['uid'] and r['uid'][:1] != LC.get(r[u'과목'], 'T')]
    cross = collections.defaultdict(set)
    for law, u, *_ in NEWS:
        if u:
            cross[u].add(law)
    xl = [u for u, v in cross.items() if len(v) > 1]
    T('C5', u'법 섞임 0(원장 uid 법 글자 · 두 법 데이터가 같은 uid)', not mix and not xl, u'원장 %d %s · 데이터 %d %s' % (len(mix), mix[:3], len(xl), xl[:3]))
    hx = collections.defaultdict(set)
    for law, u, *_ in HEADS:
        if u:
            hx[u].add(law)
    T('C5-헛', u'법 섞임 헛잣대(바탕)', any(len(v) > 1 for v in hx.values()), u'바탕 두 법 같은 uid %d' % sum(1 for v in hx.values() if len(v) > 1))
    # C-8 남은 옛 uid — 앱 데이터 파일(ou · uid_alias.json 빼고)
    A = json.load(io.open(os.path.join(UDIR, 'uid_alias.json'), encoding='utf-8'))
    dead = set(k for k in A['map'] if not k.startswith('P7:'))
    TOK = re.compile(u'[TSD][0-9A-Zㄱ-ㅎ가-힣]{5,10}')
    def old_in(folder, getf):
        c = collections.Counter()
        for f in sorted(os.listdir(folder)) if folder else []:
            if not f.endswith('.json') or f == 'uid_alias.json':
                continue
            try:
                J = getf(f)
            except Exception:
                continue
            def walk(v, key=None):
                if key == 'ou':
                    return
                if isinstance(v, str):
                    if v in dead:
                        c[f] += 1
                    elif len(v) > 12:
                        for m in TOK.findall(v):
                            for L in range(len(m), 6, -1):
                                if m[:L] in dead:
                                    c[f] += 1
                                    break
                elif isinstance(v, list):
                    for x in v:
                        walk(x)
                elif isinstance(v, dict):
                    for k2, x in v.items():
                        if k2 in dead:
                            c[f] += 1
                        walk(x, k2)
            walk(J)
        return c
    cn = old_in(DATA, jnew)
    T('C8', u'앱 데이터 안 옛 uid 0(ou·uid_alias 빼고)', not cn, dict(cn))
    hfiles = [l for l in git('ls-tree', '--name-only', BASE_DATA_REV, 'jo/data/').decode('utf-8').split('\n') if l.endswith('.json')]
    hc = collections.Counter()
    tmpd = os.path.join(WORK, 'headdata')
    os.makedirs(tmpd, exist_ok=True)
    for p in hfiles:
        f = os.path.basename(p)
        if f.startswith('jimun'):
            open(os.path.join(tmpd, f), 'wb').write(git('show', '%s:%s' % (BASE_DATA_REV, p)))
    hc = old_in(tmpd, lambda f: json.load(io.open(os.path.join(tmpd, f), encoding='utf-8')))
    T('C8-헛', u'옛 uid 헛잣대(바탕 jimun 파일)', bool(hc), dict(hc))
    # 볼트 · N: 노트 속 옛 uid — 수만(고치지 않는다)
    vault = os.path.expanduser(r"~\Documents\PA's archive")
    vc, nc = collections.Counter(), collections.Counter()
    cache = os.path.join(WORK, 'notes_count.json')     # 보고용 셈 — 마이박스 N: 훑기가 10분 걸려 6시간 캐시(옛 uid 묶음이 같을 때만)
    dsig = hashlib.md5(json.dumps(sorted(dead)).encode('utf-8')).hexdigest()
    try:
        C0 = json.load(io.open(cache, encoding='utf-8'))
        if C0.get('sig') == dsig and time.time() - C0.get('t', 0) < 6 * 3600:
            vc, nc = collections.Counter(C0['v']), collections.Counter(C0['n'])
            vault = None
    except Exception:
        pass
    if vault is None:
        N('C8', u'볼트 노트 속 옛 uid(수만 · 캐시)', {'합': sum(vc.values()), '폴더': dict(vc.most_common(6))})
        N('C8', u'N: 노트(md) 속 옛 uid(수만 · 캐시)', {'합': sum(nc.values()), '폴더': dict(nc.most_common(6))})
        vault = ''
    RX = re.compile(u'(?<![0-9A-Za-z])[TSD]\\d{7}(?:P7)?(?![0-9A-Za-z])')
    for root, ds, fs in (os.walk(vault) if vault else []):
        if '.obsidian' in root or '.trash' in root:
            continue
        for f in fs:
            if f.endswith('.md'):
                try:
                    t = io.open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
                except Exception:
                    continue
                for m in RX.findall(t):
                    if m in dead:
                        vc[os.path.relpath(os.path.join(root, f), vault).split(os.sep)[0]] += 1
    for f in (glob.glob(os.path.join(NR, '**', '*.md'), recursive=True) if vault != '' and NR else []):   # env_lanes_fix — N: 없으면(클라우드) 볼트 셈 건너뜀
        if '_지울것' in f or '_이전' in f:
            continue
        try:
            t = io.open(f, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        for m in RX.findall(t):
            if m in dead:
                nc[os.path.relpath(f, NR).split(os.sep)[0]] += 1
    if vault != '':
        io.open(cache, 'w', encoding='utf-8').write(json.dumps({'sig': dsig, 't': time.time(), 'v': dict(vc), 'n': dict(nc)}, ensure_ascii=False))
        N('C8', u'볼트 노트 속 옛 uid(수만)', {'합': sum(vc.values()), '폴더': dict(vc.most_common(6))})
        N('C8', u'N: 노트(md) 속 옛 uid(수만)', {'합': sum(nc.values()), '폴더': dict(nc.most_common(6))})
    # ── add1 E1 머리글 · E2 본문 속 제N편
    def heads(get):
        n, inl = 0, 0
        P = get('jimun_7pan.json')
        texts = []
        for z in P[u'지문'] + P[u'객관식']:
            texts += [z.get('t'), z.get('sol'), z.get(u'리담해설')]
        for law in LAWS:
            for q in get('jimun_%s.json' % law)[u'문제']:
                for z in q[u'지문']:
                    texts += [z.get('t'), z.get('sol'), z.get('p7sol'), (z.get('p7') or {}).get('t'), (z.get('p7') or {}).get('sol')]
        for t in texts:
            for ln in (t or '').split('\n'):
                if PH.head_of(ln) is not None:
                    n += 1
                elif re.search(u'제\\s*\\d+\\s*편', ln):
                    inl += 1
        return n, inl
    nh, ni = heads(jnew)
    bh, bi = heads(jhead)
    T('E1', u'쪽 머리글 0(지문·해설·선지 줄)', nh == 0, u'새 %d · 바탕 %d' % (nh, bh))
    T('E1-헛', u'머리글 헛잣대(바탕)', bh >= 18, u'바탕 %d(지시서 18 + 쪽 번호 붙은 꼴)' % bh)
    T('E2', u'본문 속 「제N편」 줄 수 무변', ni == bi, u'새 %d · 바탕 %d' % (ni, bi))
    # ── E3 빠진 문항
    TC = json.load(io.open(TOC, encoding='utf-8'))
    def have_ids(get):
        P = get('jimun_7pan.json')
        s = set(re.sub(u'-\\d$', u'', z['id']) for z in P[u'지문']) | set(z['id'] for z in P[u'객관식'])
        return s
    hn, hh = have_ids(jnew), have_ids(jhead)
    book = [(m['no'], m[u'제목'], m[u'책']) for m in TC[u'마디']]     # 모아보기(FP) 마디도
    miss_n = sorted(set(p for _, _, b in book for p in b) - hn)
    miss_h = sorted(set(p for _, _, b in book for p in b) - hh)
    # 지시서 셈 「28 = P7-2058 + 27」 — 지금 목차 재료 `책` 에는 P7-2058 이 없다(toc_fuse 가 모아보기 자리를 추록 P7-0285 로) → 빠진 것 ⊆ {P7-2058}
    # ★ A-6(a) 9/30 — p8up(775457c) A-1-1 이 원장·마디에서 P7-1207 · P7-1599 를 지웠다(N: 목차 재료 `책` 에는 남음) → 빠진 것에 둘 더함
    T('E3', u'빠진 문항 ⊆ {P7-2058}(추록 대체) + {P7-1207 · P7-1599}(8판 판올림이 지움)', set(miss_n) <= {'P7-2058', 'P7-1207', 'P7-1599'}, u'새 %s · 책에 P7-2058 %s' % (miss_n, any('P7-2058' in b for _, _, b in book)))
    T('E3-헛', u'빠진 문항 헛잣대(바탕)', len(set(miss_h) - {'P7-2058'}) == 27, u'바탕 %d %s…' % (len(miss_h), miss_h[:4]))
    cnt = TC.get(u'책수') or {}
    mism = []
    for no, t, b in book:
        k = no or t
        want = cnt.get(no) if isinstance(cnt, dict) else None
        got_n = len(set(x for x in b if x in hn))
        if want is not None and want != got_n:
            mism.append((no, t[:12], want, got_n))
    N('E3', u'마디별 번호 문항 ≠ 책수(까닭 = OMR·책 번호 건너뜀 등)', {'어긋난 마디': len(mism), '예': mism[:6]})
    # ── E6 다섯 해 대조
    sc = [k for k, v in U.items() if k.startswith('L|') and v['pos'] and int(v['pos'][0]) in SCAN and v['how'] in ('pos', 'pos-r')
          and (led.get(k[2:]) or {}).get(u'문번', '').isdigit()]
    sp = [k for k, v in U.items() if k.startswith('P|') and v['pos'] and int(v['pos'][0]) in SCAN and v['how'] in ('pos', 'pos-h', 'pos-h-ans', 'obj-pos')]
    T('E6', u'산재법 다섯 해 — 시험 문번 받은 특허·상표·디보 지문', len(sc) > 0 and len(sp) > 0, u'리담 %d · 제7판 %d' % (len(sc), len(sp)))
    hs2 = [s for s in HEADS if s[4] and int(s[4]) in SCAN and re.match(u'^[TSD]\\d{6}', s[1]) and int(s[1][5:7]) >= 51]
    N('E6', u'바탕 = 그 해 리담 문번 모름은 임시 번호(71↑) — 그림 판독·글자층 대조 없이 시험 문번 0', u'바탕 임시 번호 지문 %d' % len(hs2))
    N('E6', u'못 찾음(리담 문항)', [(k[0], k[1], k[2], y, n, s1) for (k, y, n, s1, s2) in [tuple(x) for x in M['_meta']['rep'].get('notfoundL_list', [])]] or M['_meta']['rep'].get('notfoundL'))


# ══════════ 앱 ══════════
# Claude 답 픽스처(A17) — 옛 uid(죽은 별칭)로 적힌 답 하나 · 본문 언급도 옛 uid. 저장소에 안 올린다(하네스 쪽 안에서만)
CL_OLD, CL_NEW, CL_MOLD, CL_MNEW = 'T0138603', 'TR01053', 'T0138599', 'TR01051'
CLFIX = {'v': 1, 'updatedAt': '2026-09-27', 'note': u'uid 하네스 픽스처 — 저장소에 안 올린다', 'answers': {
    'X901': {'law': u'특허', 'uid': CL_OLD, 'd': '2026-09-20', 'unit': u'하네스', 'title': u'옛 uid 로 적힌 답',
             'core': u'uid 판 전에 적힌 답 — 지문 열쇠가 옛 꼴이다.', 'md': u'**Q.** 옛 uid 답\n\n- 언급 → ' + CL_MOLD}}}
CLINJ = ("<script>(function(){var f0=window.fetch;window.fetch=function(u,o){var s=String((u&&u.url)||u);"
         "if(/\\/contents\\/jopangi\\/claude\\.json/.test(s)&&window.__CLFIX){window.__CLGETS=(window.__CLGETS||0)+1;"
         "return Promise.resolve(new Response(JSON.stringify(window.__CLFIX),{status:200}));}return f0(u,o);};})();</script>")


def serve(tag, src, data, alias_off=False, cl=False, slow_alias=0):
    key = tag + '|' + data + '|' + str(alias_off) + '|' + str(cl) + '|' + str(slow_alias)
    if key in SERVERS:
        return SERVERS[key][1]
    out = os.path.join(WORK, 'srv_%s_%d' % (tag, len(SERVERS)))
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    src = src.replace('\r\n', '\n')
    b = src.index('<body')
    bb = src.index('>', b) + 1
    # 실제 기기 = autoImportant 를 8/28 에 한 번 돈 기기(jopangi_auto 표시 있음 · 다시 안 돈다) — 새 프로필이면 SEED 가 저장소를 비워
    #   autoImportant 가 새 uid 로 ⭐ 를 다시 단다(9/27 첫 돌림 ⭐ 459 로 헛잣대가 흐려졌다) → SEED 바로 뒤에 표시를 넣는다
    AUTO = "<script>try{localStorage.setItem('jopangi_auto',JSON.stringify({important:'v1',at:'2026-08-28T16:48:32.584Z'}));}catch(e){}</script>"
    CLS = ('<script>window.__CLFIX=%s;</script>' % json.dumps(CLFIX, ensure_ascii=False) + CLINJ) if cl else ''
    html = src[:bb] + CJ.SEED + AUTO + CLS + src[bb:]
    e = html.rindex('</body>')
    html = html[:e] + '<script>\n' + TESTS + '\n</script>\n' + html[e:]
    io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(html)

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=out, **k)

        def translate_path(self, path):
            p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
            if p.startswith('/__vendor/'):
                return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
            if p.startswith('/data/'):
                if alias_off and p.endswith('/uid_alias.json'):
                    return os.path.join(out, '__nope.json')      # 헛잣대 — 별칭표가 없는 판(옮기기 꺼짐)
                if slow_alias and p.endswith('/uid_alias.json'):
                    time.sleep(slow_alias)                       # 답이 별칭표보다 먼저 오는 차례(다시 색인 길)
                return os.path.join(data, p[6:].replace('/', os.sep))
            if p in ('/index.html', '/'):
                return super().translate_path(path)
            f = os.path.join(JOD, p.lstrip('/').replace('/', os.sep))
            return f if os.path.exists(f) else super().translate_path(path)

        def log_message(self, *a, **k):
            pass
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[key] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    def __init__(self, br, tag, src, data, remote=None, alias_off=False, keep=False, W=1440, H=900, port=None, ctx=None, cl=False, slow_alias=0):
        self.port = port or serve(tag, src, data, alias_off, cl, slow_alias)
        self.ctx = ctx or br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1)
        self.ctx.route('**/*', CJ.route_filter)
        if remote is not None:
            self.ctx.add_init_script('window.__REMOTE={text:%s,sha:"H_seed",puts:0};' % json.dumps(remote, ensure_ascii=False))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(180000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:240]))
        self.pg.on('console', lambda m: self.errs.append('console: ' + m.text[:240]) if m.type == 'error' else None)
        self.pg.goto('http://127.0.0.1:%d/index.html?tok=1&who=%s%s' % (self.port, urllib.parse.quote('꼬까'), '&keep=1' if keep else ''),
                     wait_until='load', timeout=180000)
        self.pg.wait_for_function(READY, timeout=180000)
        self.pg.wait_for_timeout(600)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def until(self, expr, arg=None, ms=20000):
        t0 = time.time()
        while time.time() - t0 < ms / 1000:
            v = self.ev(expr, arg)
            if v:
                return v
            self.pg.wait_for_timeout(100)
        return self.ev(expr, arg)

    def click(self, at, wait=500):
        if not at or not at.get('on'):
            return False
        self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def errs_all(self):
        return [y for y in (self.errs + (self.ev("()=>__HU.errs()") or [])) if not CJ.NOISE(y)]

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def type_id(p, q):
    """🔍 칸을 진짜 포인터로 누르고 → 지우고 → 키보드로 치고 → Enter"""
    at = p.ev("()=>__HU.srInp()")
    if not p.click(at, 200):
        return False
    p.pg.keyboard.press('Control+A')
    p.pg.keyboard.press('Delete')
    p.pg.keyboard.type(q, delay=20)
    p.pg.keyboard.press('Enter')
    p.pg.wait_for_timeout(900)
    return True


SEARCH = [('T0845511P7', u'T084508ㅁ'), ('T0542511', 'TH050004'), ('T0340742', 'TR03071')]


def app_gates(br):
    new = io.open(NEWF, encoding='utf-8').read()
    base = git('show', '%s:jo/index.html' % BASE_REV).decode('utf-8')
    assert hashlib.md5(base.encode('utf-8')).hexdigest()[:8] == BASE_MD5
    for tag, src, data in (('NEW', new, DATA), ('BASE', base, DATA)):
        p = Pg(br, 'app' + tag, src, data)
        try:
            p.ev("()=>__HU.home('특허법')")
            p.until("()=>__HU.migReady().alias || !(typeof UIDALIAS!=='undefined')", ms=8000)
            res = []
            for old, want in SEARCH:
                p.ev("()=>__HU.closeAll()")
                typed = type_id(p, old)
                pop = p.until("k=>{const r=__HU.pop(k);return r.open?r:null;}", want, ms=4000) or p.ev("k=>__HU.pop(k)", want)
                res.append((old, want, typed, pop.get('open') and pop.get('vis'), pop.get('id'), p.ev("()=>__HU.srRows()")[:1]))
            ok = all(r[3] for r in res)
            if tag == 'NEW':
                T('C6', u'옛 uid 키보드 치고 Enter → 새 uid 지문 팝업 보임', ok, res)
            else:
                T('C6-헛', u'별칭 찾기 헛잣대(바탕 앱 + 새 데이터)', not ok, res)
            if tag == 'NEW':
                # C-7 기록 키 — 표본 카드 O 를 page.mouse → 기록 키 = 새 uid(리담 줄 T084510ㄱr)
                k = u'T084510ㄱr'
                p.ev("()=>__HU.closeAll()")
                type_id(p, k)
                p.until("k=>__HU.pop(k).open", k, ms=4000)
                go = p.ev("k=>__HU.goBtn(k)", k)
                moved = p.click(go, 1200)
                row = p.until("k=>{const r=__HU.row(k);return r&&r.vis?r:null;}", k, ms=6000)
                ob = p.ev("k=>__HU.oxAt(k,'O')", k)
                clicked = p.click(ob, 600)
                rec = p.ev("k=>__HU.rec(k)", k)
                T('C7', u'표본 카드 O 누름 → 기록 키 = 새 uid(%s)' % k, bool(moved and row and clicked and rec and rec.get('m') == 'O'),
                  {'이동': moved, '카드': row, 'O': clicked, '기록': rec})
                n = p.ev("y=>__HU.gi(y)", 2013)
                p.ev("k=>__HU.giShow(k)", u'특허:2013:6')   # ★ mbsame_add3 §A-2 — 새 기출뷰 한 쪽 5 문항(옛 판은 무동작)
                gc = p.ev("k=>__HU.giCard(k)", u'특허:2013:6')
                J = jnew(u'jimun_특허.json')
                q6 = [q for q in J[u'문제'] if q[u'연도'] == '2013' and q[u'시험문번'] == '6']
                z5 = (q6[0][u'지문'][4] if q6 and len(q6[0][u'지문']) > 4 else {})
                T('C7', u'기출뷰 2013 6번 ⑤ 줄 = T1350065', bool(gc and gc['vis'] and z5.get('uid') == 'T1350065' and len(gc['rows']) >= 5
                                                          and gc['rows'][4][:20] == re.sub(r'\s+', ' ', z5.get('t', ''))[:20]),
                  {'카드': gc, '⑤ uid': z5.get('uid')})
                # add1 E1 앱 — pdf 224(P7-0717-5) 카드에 「제5편」 안 보임 · 카드까지 = 🔍 치고 Enter → 팝업 「↪ 이 지문으로 이동」(page.mouse)
                #   (그 마디 카드가 20 장씩 쪽으로 나뉘어 서랍 누름만으로는 그 쪽이 안 선다 — 이동 단추가 쪽까지 찾아간다)
                P7 = {z['id']: z for z in jnew('jimun_7pan.json')[u'지문']}
                u5 = P7['P7-0717-5']['uid']
                p.ev("()=>__HU.home('특허법')")
                type_id(p, u5)
                p.until("k=>__HU.pop(k).open", u5, ms=4000)
                mv5 = p.click(p.ev("k=>__HU.goBtn(k)", u5), 1200)
                # 그 지문이 리담 선지와 같은 uid 로 합쳐졌으면(TR07095) 제7판 카드 대신 리담 문항 카드의 한 줄로 선다 — 줄도 본다
                ct = p.until("k=>{const c=__HU.cardText(k);if(c&&c.vis)return c;const r=__HU.row(k);return r&&r.vis?{vis:true,t:r.t,row:true}:null;}", u5, ms=6000)
                T('E1', u'pdf 224 · P7-0717-5(%s) 카드 끝 「제5편」 안 보임' % u5, bool(mv5 and ct and ct['vis'] and u'제5편' not in ct['t']),
                  {'이동': mv5, '마디': p.ev("k=>__HU.nodeOf(k)", u5), '카드 끝': (ct or {}).get('t', '')[-80:]})
            errs = p.errs_all()
            T('APP' if tag == 'NEW' else 'APP-B', u'오류 0(%s)' % tag, not errs, errs[:4])
        finally:
            p.close()


def e1_base(br):
    """E1 헛잣대 — 바탕 앱 + 바탕 데이터(genie HEAD 트리 통째)에서 옛 T0744661 카드 끝에 「제5편」 이 보인다"""
    hd = os.path.join(WORK, 'headdata_full')
    if not os.path.isdir(hd):
        os.makedirs(hd)
        tar = subprocess.run(['git', '-C', GENIE, 'archive', BASE_DATA_REV, 'jo/data'], capture_output=True).stdout
        import tarfile
        tarfile.open(fileobj=io.BytesIO(tar)).extractall(hd)
    base = git('show', '%s:jo/index.html' % BASE_REV).decode('utf-8')
    p = Pg(br, 'e1base', base, os.path.join(hd, 'jo', 'data'))
    try:
        p.ev("()=>__HU.home('특허법')")
        p.ev("k=>{try{linkGo(k);}catch(e){}return 1;}", 'T0744661')      # 헛잣대 쪽은 옛 앱의 이동 함수로 카드까지(누름 관문 아님)
        ct = p.until("k=>{const c=__HU.cardText(k);return c&&c.vis?c:null;}", 'T0744661', ms=8000)
        T('E1-헛', u'바탕(앱 a9d72c1 + 데이터 f3b74c9) T0744661 카드 끝 「제5편」 보임', bool(ct and u'제5편' in ct['t']), (ct or {}).get('t', '')[-80:])
    finally:
        p.close()


GSEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.alert=function(){};window.confirm=function(){return true;};
try{localStorage.clear();}catch(e){}
</script>"""
GJS = r"""(()=>{const vis=e=>!!e&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0;
const R=e=>{const r=e.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,w:r.width,h:r.height};};
const hit=t=>{if(!t)return null;try{t.scrollIntoView({block:'center'});}catch(e){}const r=R(t);const at=document.elementFromPoint(r.cx,r.cy);
  return Object.assign(r,{on:!!at&&(at===t||t.contains(at))&&r.w>0&&r.h>0,vis:vis(t)});};
window.__HG={hit,vis,
  empty(){return hit(document.getElementById('emptyRepo'));},
  dlg(){const d=document.getElementById('repoDlg');return !!d&&d.open&&document.querySelectorAll('#repoList .repo-row').length>1;},
  row(y,s){const r=[...document.querySelectorAll('#repoList .repo-row')].find(x=>x.textContent.includes(y)&&x.textContent.includes(s));
    return r?hit(r.querySelector('input[type=checkbox]')):null;},
  get(){return hit(document.getElementById('repoGet'));},
  cover(){const c=document.querySelector('#grid .cover');return c?hit(c):null;},
  toast(){const t=document.querySelector('.toast, #toast');return t?t.textContent.trim().slice(0,80):'';},
  view(){const v=document.getElementById('viewer'),c=document.getElementById('pdfCanvas');if(!v||v.hidden||!c)return null;
    let ink=0;try{const x=c.getContext('2d').getImageData(0,0,c.width,c.height).data;for(let i=0;i<x.length;i+=4*97){if(x[i]<200)ink++;}}catch(e){ink=-1;}
    return {vis:vis(v)&&vis(c),w:c.width,h:c.height,pg:(document.getElementById('pgInput')||{}).value,tot:(document.getElementById('pgTotal')||{}).textContent,ink:ink,
            title:(document.getElementById('vTitle')||{}).textContent};},
  errs(){return (window.__ERR||[]).slice(0,5);}};})();"""


def gichul_gate(br):
    """기출서재 앱(genie 루트 index.html) — 새 list.json 사본 + 쪼갠 ABBYY 판에서 2020 산재법을 진짜 포인터로 받아 열어 1쪽 보임.
       헛잣대 = 옛 list.json(옛 해시) + 새 파일 → 앱이 해시가 달라 받지 않는다(list.json 을 안 바꾸면 못 연다)."""
    src = git('show', 'HEAD:index.html').decode('utf-8').replace('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/', '/__vendor/')
    b = src.index('<head')
    bb = src.index('>', b) + 1
    src = src[:bb] + GSEED + src[bb:]
    lj_new = os.path.join(WORK, 'list_new.json')
    lj_old = os.path.join(WORK, 'list_old.json')
    open(lj_old, 'wb').write(git('show', '%s:gichul/pdf/list.json' % BASE_REV))   # ★ A-6(d) 9/30 — 옛 list.json = uid 판 앞 바탕(a9d72c1) · HEAD 는 17094a5 인도 뒤 이미 새 해시
    for mode in ('new', 'old'):
        out = os.path.join(WORK, 'gich_' + mode)
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(out)
        io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(src)
        lj = lj_new if mode == 'new' else lj_old

        class H(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=out, **k)

            def translate_path(self, path):
                p = urllib.parse.unquote(urllib.parse.urlparse(path).path)
                if p.startswith('/__vendor/'):
                    return os.path.join(CJ.VENDOR, p[len('/__vendor/'):].replace('/', os.sep))
                if p == '/gichul/pdf/list.json':
                    return lj
                m = re.match(r'^/gichul/pdf/((?:2009|2010|2020|2022|2025)-1-sanjae\.pdf)$', p)
                if m:
                    return os.path.join(PDFD, m.group(1))
                if p in ('/index.html', '/'):
                    return super().translate_path(path)
                return os.path.join(GENIE, p.lstrip('/').replace('/', os.sep))

            def log_message(self, *a, **k):
                pass
        srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
        srv.daemon_threads = True
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        ctx = br.new_context(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
        ctx.route('**/*', CJ.route_filter)
        pg = ctx.new_page()
        pg.set_default_timeout(120000)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        try:
            pg.goto('http://127.0.0.1:%d/index.html' % srv.server_address[1], wait_until='load')
            pg.wait_for_timeout(1500)
            pg.evaluate(GJS)
            step = {}

            def clk(expr, name, wait=800):
                at = pg.evaluate(expr)
                ok = bool(at and at.get('on'))
                if ok:
                    pg.mouse.click(at['cx'], at['cy'])
                    pg.wait_for_timeout(wait)
                step[name] = ok
                return ok
            clk("()=>__HG.empty()", '빈 서재 단추')
            t0 = time.time()
            while time.time() - t0 < 20 and not pg.evaluate("()=>__HG.dlg()"):
                pg.wait_for_timeout(200)
            clk(u"()=>__HG.row('2020','산재법')", '2020 산재법 칸', 300)
            clk("()=>__HG.get()", '받기', 1500)
            t0 = time.time()
            while time.time() - t0 < 30 and not pg.evaluate("()=>__HG.cover()"):
                pg.wait_for_timeout(300)
            step['토스트'] = pg.evaluate("()=>__HG.toast()")
            # 저장소 창(모달)이 떠 있으면 표지를 가린다 — 「닫기」를 진짜 포인터로
            if pg.evaluate("()=>{const d=document.getElementById('repoDlg');return !!d&&d.open;}"):
                clk("()=>__HG.hit(document.getElementById('repoClose'))", '저장소 창 닫기', 600)
            if pg.evaluate("()=>__HG.cover()"):
                clk("()=>__HG.cover()", '표지', 1500)
            v = None
            t0 = time.time()
            while time.time() - t0 < 30:
                v = pg.evaluate("()=>__HG.view()")
                if v and v['w'] > 0 and v['ink'] > 50:
                    break
                pg.wait_for_timeout(300)
            ok = bool(v and v['vis'] and v['pg'] == '1' and v['ink'] > 50)
            if mode == 'new':
                T('E5', u'기출서재 — 2020 산재법 진짜 포인터로 받아 열기 → 1쪽 보임(캔버스 글자 픽셀)', ok, {'단계': step, '보기': v, '오류': errs[:3]})
            else:
                T('E5-헛', u'기출서재 헛잣대 — 옛 list.json(옛 해시) + 새 파일 → 못 받음', not ok, {'단계': step, '보기': v})
        finally:
            ctx.close()
            srv.shutdown()


def cl_gates(br):
    """A17 — Claude 답이 옛 uid(죽은 별칭)로 적혀 있어도 새 uid 카드에 붙는다(색인 · 언급 · 카드 단추 · 진짜 포인터로 창).
       NEW 는 별칭표를 3초 늦게 내준다(답이 먼저 와 옛 열쇠로 색인된 뒤 다시 색인하는 길) · 헛잣대 둘 = 별칭표 없는 판 · 바탕 앱 + 새 데이터."""
    new = io.open(NEWF, encoding='utf-8').read()
    base = git('show', '%s:jo/index.html' % BASE_REV).decode('utf-8')
    ks = [CL_OLD, CL_NEW, CL_MOLD, CL_MNEW]
    for tag, src, kw in ((u'NEW', new, {'slow_alias': 3}), (u'NEW-별칭없음', new, {'alias_off': True}), (u'BASE', base, {})):
        p = Pg(br, 'cl' + tag, src, DATA, cl=True, **kw)
        try:
            p.ev("()=>__HU.home('특허법')")
            st = p.until("ks=>{const c=__HU.cl(ks);return c.state==='ok'?c:null;}", ks, ms=20000)
            p.pg.wait_for_timeout(4500)          # 늦은 별칭표(3초) · 다시 색인까지
            st = p.ev("ks=>__HU.cl(ks)", ks)
            card = p.ev("k=>__HU.clCard(k)", CL_NEW)
            cw = None
            if tag == u'NEW' and card and card.get('on'):      # 잰 자리에서 바로 누른다(다른 카드로 옮기면 자리가 바뀐다)
                p.click(card, 700)
                cw = p.until("k=>{const w=__HU.clWin(k);return w.vis?w:null;}", CL_NEW, ms=4000)
            ment = p.ev("k=>__HU.clCard(k)", CL_MNEW)
            if tag == u'NEW':
                T('CL', u'Claude 답 옛 uid %s → 새 카드 %s 색인 · 언급 %s → %s · 옛 열쇠 0' % (CL_OLD, CL_NEW, CL_MOLD, CL_MNEW),
                  st['by'] == {CL_NEW: ['X901']} and st['ment'] == {CL_MNEW: ['X901']}, st)
                T('CL', u'다시 색인 길 — 처음 받은 순간은 별칭표 전 · 옛 열쇠로 색인됐다', bool(st.get('first')) and not st['first']['alias']
                  and CL_OLD in st['first']['by'], st.get('first'))
                T('CL', u'%s 카드 Claude 단추 「Claude1」(주황 수) · 진짜 포인터로 누르면 답 창(답 번호 X901 · 본문 「옛 uid 답」)' % CL_NEW,
                  bool(card and card.get('on') and card['text'] == 'Claude1' and cw and 'X901' in cw['t'] and u'옛 uid 답' in cw['t']), {'단추': card, '창': cw})
                T('CL', u'%s 카드 — 언급 표시 「↩」' % CL_MNEW, bool(ment and ment.get('vis') and u'↩' in (ment.get('text') or '')), ment)
                errs = p.errs_all()
                T('APP', u'오류 0(Claude 답)', not errs, errs[:4])
            else:
                T('CL-헛', u'%s — 답이 옛 열쇠 %s 에 남고 새 카드 %s 단추에 수 없음' % (tag, CL_OLD, CL_NEW),
                  st['by'] == {CL_OLD: ['X901']} and bool(card and card.get('text') == 'Claude'), {'색인': st, '단추': card})
        finally:
            p.close()


def star_gates(br):
    new = io.open(NEWF, encoding='utf-8').read()
    remote = git('show', 'aa5eb366:jopangi/기록.json', repo=_roots.spd()).decode('utf-8')   # ★ A-6(d) 9/30 — 인도 때(09-27 02:24) 기록으로 박음: studyplandata aa5eb366(⭐ 328 · 옛 열쇠 131) · 지금 클론(REC)은 기기가 이미 옮겨 ⭐ 351 · 옛 열쇠 0(_task_jo_wonmun.md 362)
    R0 = json.loads(remote)
    ox0 = R0['data']['jopangi.ox']
    A = json.load(io.open(os.path.join(UDIR, 'uid_alias.json'), encoding='utf-8'))
    # 헛잣대 먼저 — 별칭표 없는 판(옮기기 꺼짐)
    p = Pg(br, 'starOFF', new, DATA, remote=remote, alias_off=True)
    try:
        p.ev("()=>__HU.home('특허법')")
        p.until("()=>(window.__REMOTE||{}).puts>=1", ms=25000)
        s0 = p.ev("()=>__HU.stars()")
        T('E7-헛', u'옮기기 끈 판 = ⭐ 44 이상 사라짐', 328 - s0['pool'] >= 44, s0)
    finally:
        p.close()
    ctx = br.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
    port = serve('starON', new, DATA)
    p = Pg(br, 'starON', new, DATA, remote=remote, port=port, ctx=ctx)
    try:
        p.ev("()=>__HU.home('특허법')")
        mg = p.until("()=>{const m=__HU.migReady();return (m.last&&m.last.total>0&&m.puts>=1)?m:null;}", ms=30000)
        p.ev("()=>__HU.home('특허법')")
        s1 = p.ev("()=>__HU.stars()")
        keys = p.ev("()=>__HU.starKeys()")
        T('E7', u'⭐ 옮긴 뒤 수 = 351 · 옛 열쇠 0', s1['pool'] == 351 and s1['store'] == 351 and s1['dead'] == 0,   # A-6(a) 9/30 — uid_add2(genie 6242678 · 09-27 18:15 「별칭 옮기기(포스트잇·split ⭐)」 · 앱 16530줄 bump('ox-tag')) — 옛 열쇠의 포스트잇(태그)만 있는 칸도 옮김 → 인도 때 기록(studyplandata aa5eb366)을 지금 앱으로 옮기면 ⭐ 328 + 포스트잇 23 = 351(첫 저장본 뒤 두 번째 실행 값 moved ox 131 · ox-tag 23)
          {'옮김': (mg or {}).get('last'), '셈': s1})
        # 표본 — 옛 T0845101 ⭐ → T084510ㄱr 카드 ⭐ 보임(진짜 포인터로 카드까지)
        k = u'T084510ㄱr'
        type_id(p, 'T0845101')
        p.until("k=>__HU.pop(k).open", k, ms=4000)
        go = p.ev("k=>__HU.goBtn(k)", k)
        moved = p.click(go, 1200)
        row = p.until("k=>{const r=__HU.row(k);return r&&r.vis?r:null;}", k, ms=6000)
        T('E7', u'표본 T0845101 ⭐ → %s 카드 ⭐ 보임' % k, bool(moved and row and row.get('star') and row['star']['vis'] and row['star']['on']),
          {'이동': moved, '줄': row})
        # 두 번째 켜기 — 옮김 0
        p2 = Pg(br, 'starON', new, DATA, port=port, ctx=ctx, keep=True)
        m2 = p2.until("()=>{const m=__HU.migReady();return m.last?m:null;}", ms=15000)
        T('E7', u'두 번째 켜기 옮김 0', bool(m2) and m2['last']['total'] == 0, (m2 or {}).get('last'))
        # 옛 열쇠를 다시 넣은 원격(옛 판 기기가 되올림) → 받은 뒤 또 옮김 · 화면 ⭐ 수 같음
        rt = json.loads(p2.ev("()=>__HU.remote()"))
        now = int(time.time() * 1000) + 60000
        back = 0
        for kk, v in ox0.items():
            if kk in A['map'] or kk in A['split']:
                rt['data']['jopangi.ox'][kk] = v
                rt['u']['jopangi.ox|' + kk] = now
                rt.get('gone', {}).pop('jopangi.ox|' + kk, None)
                back += 1
        p2.ev("t=>__HU.setRemote(t)", json.dumps(rt, ensure_ascii=False))
        p2.ev("()=>__HU.sync()")
        p2.ev("()=>__HU.home('특허법')")
        s3 = p2.ev("()=>__HU.stars()")
        T('E7', u'옛 열쇠 되올린 원격(%d칸) 받은 뒤 ⭐ 수 같음 · 옛 열쇠 0' % back, s3['pool'] == 351 and s3['dead'] == 0,   # A-6(a) 9/30 — 옮긴 뒤 수 351(위 칸과 같은 까닭)
          {'셈': s3, '옮기기': p2.ev("()=>__HU.migReady().last")})
        errs = p.errs_all() + p2.errs_all()
        T('APP', u'오류 0(⭐)', not errs, errs[:4])
        p2.close()
    finally:
        p.close()


# ══════════ 산재법 PDF ══════════
def pdf_gates(br):
    L = json.loads(git('show', 'HEAD:gichul/pdf/list.json').decode('utf-8'))
    items = {it['file']: it for it in L['items']}
    ok_all, rows = True, []
    for y in SCAN:
        f = '%d-1-sanjae.pdf' % y
        p_new = os.path.join(PDFD, f)
        b = open(p_new, 'rb').read()
        ptt = subprocess.run(['pdftotext', '-enc', 'UTF-8', p_new, '-'], capture_output=True).stdout
        old = git('show', '%s:gichul/pdf/%s' % (BASE_REV, f))   # ★ A-6(d) 9/30 — 옛 원본 = uid 판 앞 바탕 a9d72c1(HEAD 는 17094a5 인도 뒤 ABBYY 새 판)
        tmp = os.path.join(WORK, 'old_' + f)
        open(tmp, 'wb').write(old)
        pto = subprocess.run(['pdftotext', '-enc', 'UTF-8', tmp, '-'], capture_output=True).stdout
        txt = ptt.decode('utf-8', 'ignore')
        kw = all(k in txt for k in (u'특허', u'상표', u'디자인'))
        rows.append((y, len(b), hashlib.sha256(b).hexdigest()[:10], len(ptt), len(pto), kw))
        ok_all &= len(ptt) > 30000 and kw
    T('E5', u'산재법 다섯 해 글자층 > 30,000 B(pdftotext) · 세 법 낱말', ok_all, rows)
    T('E5-헛', u'글자층 헛잣대(바탕 = uid 판 앞 원본 — 30,000 B 못 넘음)', all(r[4] < 30000 for r in rows), [(r[0], r[4]) for r in rows])
    # 새 list.json 사본 — 다섯 줄만 해시·바이트·쪽
    import pymupdf
    L2 = json.loads(json.dumps(L))
    for it in L2['items']:
        m = re.match(r'^(\d{4})-1-sanjae\.pdf$', it['file'])
        if m and int(m.group(1)) in SCAN:
            b = open(os.path.join(PDFD, it['file']), 'rb').read()
            it['hash'] = hashlib.sha256(b).hexdigest()
            it['bytes'] = len(b)
            it['pages'] = len(pymupdf.open(os.path.join(PDFD, it['file'])))
    Lb = json.loads(git('show', '%s:gichul/pdf/list.json' % BASE_REV).decode('utf-8'))   # ★ A-6(d) 9/30 — 「다섯 줄만 바뀜」은 uid 판 앞 바탕(a9d72c1) list.json 과 맞댄다(HEAD 는 17094a5 인도 뒤 이미 새 해시) · L(HEAD)은 새 사본(기출서재 칸이 받는 것) 그대로
    same = sum(1 for a, b in zip(Lb['items'], L2['items']) if a == b)
    lj = os.path.join(WORK, 'list_new.json')
    io.open(lj, 'w', encoding='utf-8', newline='\n').write(json.dumps(L2, ensure_ascii=False, indent=1) + '\n')
    T('E5', u'list.json 새 사본 — 다섯 줄만 바뀜 · 해시 = 파일 sha256', same == len(L['items']) - 5 and all(
        it['hash'] == hashlib.sha256(open(os.path.join(PDFD, it['file']), 'rb').read()).hexdigest()
        for it in L2['items'] if re.match(r'^(2009|2010|2020|2022|2025)-1-sanjae\.pdf$', it['file'])), u'무변 %d / %d · 사본 %s' % (same, len(L['items']), lj))
    N('E5', u'새 list.json 사본(인도 때 genie 에 넣을 값)', lj)


UIDTOK = re.compile(u'(?<![0-9A-Za-z])(?:[TSD][RHJX]?\\d{4,7}(?:[1-7ㄱ-ㅎ가나다라마바사])?(?:[hr]\\d?)?(?:P7)?)(?![0-9A-Za-z])')


def reg_gates(br):
    """§C-9 · add1 E-8 — 화면 글을 바탕(앱 a9d72c1 + 데이터 f3b74c9)과 맞대 uid 글자 말고 무엇이 달라졌나(까닭은 보고에).
       화면 = 특허·상표 1차객 첫 화면 · 마디 셋(2.2.1 · 3.3 · 상표 첫 마디)의 첫 쪽."""
    hd = os.path.join(WORK, 'headdata_full', 'jo', 'data')
    new = io.open(NEWF, encoding='utf-8').read()
    base = git('show', '%s:jo/index.html' % BASE_REV).decode('utf-8')
    shots = {}
    for tag, src, data in (('BASE', base, hd), ('NEW', new, DATA)):
        p = Pg(br, 'reg' + tag, src, data)
        try:
            out = {}
            p.ev("()=>__HU.home('특허법')")
            out[u'특허 첫 화면'] = p.ev("()=>__HU.dump()")
            for lab in (u'2.2.1', u'3.3'):
                sel = p.ev("no=>{const i=(VJ.M||[]).findIndex(n=>String(n.no)===no);return i>=0?'__mg'+i:null;}", lab)
                if sel:
                    p.ev("s=>__HU.goNode(s)", sel)
                    out[u'특허 ' + lab] = p.ev("()=>__HU.dump()")
            p.ev("()=>__HU.home('상표법')")
            out[u'상표 첫 화면'] = p.ev("()=>__HU.dump()")
            shots[tag] = out
        finally:
            p.close()
    import difflib
    summ = {}
    for k in shots['NEW']:
        a = UIDTOK.sub('<ID>', shots['BASE'].get(k, ''))
        b = UIDTOK.sub('<ID>', shots['NEW'].get(k, ''))
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        ops = [(t, a[i1:i2][:60], b[j1:j2][:60]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
        summ[k] = {'같음': round(sm.ratio(), 4), '바뀐 조각': len(ops), '예': ops[:6]}
    N('C9', u'화면 글 바탕 대조(uid 글자 가림) — 달라진 조각(까닭은 수행 결과)', summ)
    io.open(os.path.join(WORK, 'reg_screens.json'), 'w', encoding='utf-8').write(json.dumps(shots, ensure_ascii=False))


def report():
    P = sum(1 for r in RES if r[2] is True)
    F = [r for r in RES if r[2] is False]
    lines = ['# _harness_jo_gaek_uid 결과 — %s' % time.strftime('%Y-%m-%d %H:%M'), '',
             'NEW 앱 %s (md5 %s) · NEW 데이터 %s · BASE %s/%s' % (NEWF, hashlib.md5(open(NEWF, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8], DATA, BASE_REV, BASE_DATA_REV),
             'PASS %d · FAIL %d · INFO %d' % (P, len(F), sum(1 for r in RES if r[2] is None)), '']
    for g, n, ok, d in RES:
        lines.append('%s | %s · %s | %s' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, n,
                                           d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)[:900]))
    f = os.path.join(OUT, '_harness_jo_gaek_uid_result.txt')
    io.open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('\n== PASS %d · FAIL %d → %s' % (P, len(F), f))
    return len(F)


def main():
    os.makedirs(WORK, exist_ok=True)
    if not ONLY or 'data' in ONLY:
        data_gates()
    if not ONLY or 'pdf' in ONLY:
        pdf_gates(None)
    if not ONLY or set(ONLY) & {'app', 'cl', 'star', 'pdf', 'reg'}:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            try:
                if not ONLY or 'app' in ONLY:
                    app_gates(br)
                    e1_base(br)
                if not ONLY or 'pdf' in ONLY:
                    gichul_gate(br)
                if not ONLY or 'app' in ONLY or 'cl' in ONLY:
                    cl_gates(br)
                if not ONLY or 'star' in ONLY:
                    star_gates(br)
                if not ONLY or 'reg' in ONLY:
                    if not os.path.isdir(os.path.join(WORK, 'headdata_full')):
                        e1_base(br)
                    reg_gates(br)
            finally:
                br.close()
    sys.exit(1 if report() else 0)


if __name__ == '__main__':
    main()
