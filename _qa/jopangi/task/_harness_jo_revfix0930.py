# -*- coding: utf-8 -*-
r"""_task_jo_revfix0930 §B 관문 — 다른 법 인용 링크(볼트 · 데이터 · 화면) · 1차객 서랍 넘침 · 터치 누름 자리 · 민소 편 목록 · 장 머리 한 줄 · 교재 자리 창 자리 · 화면 훑기

  python _harness_jo_revfix0930.py [--new <앱>] [--base <앱 파일 | genie git 판>] [--data <새 데이터 폴더>] [--eng chromium,webkit] [--only B1,..,B9,WK] [--res <결과>] [--yardstick]

  NEW  = 이 판 앱(기본 genie jo/index.html) · 데이터 = genie jo/data(⚙ 로 다시 만든 것) · BASE = 착수 HEAD(기본 genie 9143a83 · 앱과 jo/data 둘 다 그 판)
  --yardstick = BASE 앱 + BASE 데이터 + 고치기 전 볼트 사본(jopangi/task/_vault_before_0930)으로 B1~B8 이 저마다 FAIL 해야 통과 · B9 화면 훑기 = 새 판 흠 − 바탕 흠이라 해당 없음
  도구 = 같은 폴더 _harness_jo_revfix0929b(서버 · SEED · __RB 도구 · 기기 흉내 · 누름 영역 더듬기 tgt · 교재 자리 창 열기 · 화면 훑기)를 불러 쓴다 + 이 판 도구 __RF(격자 훑기 · 글자 훑기)
  규칙 = ⚙ jo_common.other_law_cite(파이썬) ↔ 앱 wmAutoOther(JS) — B2 가 같은 글 묶음으로 둘을 맞댄다
  WebKit = 터치 칸(B4 · B5)만 · 이 컴퓨터에 WebKit 이 없으면 「안 잼」
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import collections, hashlib, io, json, os, re, sys, tempfile, time, subprocess   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', '9143a83')
YARD = '--yardstick' in sys.argv
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_revfix0930_result.txt'))
NEWDATA = ARG('--data', _roots.genie('jo', 'data'))
BK = os.path.join(HERE, '_vault_before_0930')


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def data_dir(rev):
    """genie git 판 rev 의 jo/data 를 임시 폴더로(한 번만)"""
    d = os.path.join(tempfile.gettempdir(), 'h_rf30_data_' + rev)
    if os.path.isfile(os.path.join(d, '_ok')):
        return d
    os.makedirs(d, exist_ok=True)
    names = [x for x in git('ls-tree', '--name-only', rev, 'jo/data/').decode('utf-8').split('\n') if x]
    for n in names:
        b = git('show', '%s:%s' % (rev, n))
        open(os.path.join(d, n.split('/')[-1]), 'wb').write(b)
    open(os.path.join(d, '_ok'), 'w').write(rev)
    return d


DATA = data_dir(BASE) if YARD else NEWDATA
# 도구 하네스(revfix0929b)는 제 인자를 sys.argv 에서 읽는다 — 앱 · 데이터 자리를 넘겨 둔다(BASE 는 이 하네스가 따로 쓴다)
_argv = sys.argv
sys.argv = [sys.argv[0], '--new', NEW, '--data', DATA] + [x for k in ('--exam', '--mbpdf', '--vendor') if k in _argv for x in (k, _argv[_argv.index(k) + 1])]
sys.path.insert(0, HERE)
import _harness_jo_revfix0929b as H   # noqa: E402
sys.argv = _argv
sys.path.insert(0, os.path.dirname(HERE))
try:
    import jo_common as JC   # noqa: E402  ⚙ 공용(N: jopangi\) — 볼트 판정 · 다른 법 인용 규칙(파이썬 한 벌)
except Exception:   # 클라우드 _qa 사본 — ⚙ 모듈 · 볼트가 없다 → B1 · B2 는 「N: 필요」
    JC = None

T, N, RES = H.T, H.N, H.RES
PC, PC2, PHONE, PAD = H.PC, H.PC2, H.PHONE, H.PAD
LAWS = ['특허법', '상표법', '디자인보호법', '민사소송법']

# ── 이 판 도구 __RF — 격자 훑기(누를 것의 보이는 사각형 안 점을 둘레가 빼앗는가) · 글자 훑기(본문 글자 가운데를 둘레가 빼앗는가) ──
#   빼앗김 = 둘레(::before · ::after) 켠 채 elementFromPoint 가 그 요소 밖 · 둘레 끈 채(html.__nh) 그 요소 안 — 둘레가 만든 가로챔만 센다(팝업 · 붙박이 층이 덮은 것은 안 센다)
RF_TOOLS = r"""<script>
(function(){
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const sig = e => e.tagName.toLowerCase() + '.' + String(e.className && e.className.baseVal !== undefined ? e.className.baseVal : e.className).split(' ').filter(Boolean).slice(0, 2).join('.') + ':' + (e.textContent || '').replace(/\s+/g, ' ').trim().replace(/\d+/g, '#').slice(0, 12);
const TSEL = 'button, a[href], [role=button], [role=menuitem], .wmlk, .joLink, .jno, input, select, textarea, label, [tabindex], .mbbrow, .ncb-pic, .tree .r.jhead, .tree .r.jsub';   /* 누를 것 + 머리 줄(장·편·절) · 서랍 조 줄 · 카드처럼 줄 전체가 누름 자리인 큰 그릇은 뺀다(0929b 하네스 ACT 와 같은 결) */
const inT = (t, a) => !!a && (a === t || t.contains(a));
window.__RF = {
  steal(rootSel, step){ step = step || 4;
    const roots = [...document.querySelectorAll(rootSel)].filter(vis), T = [];
    roots.forEach(r => { if (r.matches(TSEL)) T.push(r); r.querySelectorAll(TSEL).forEach(e => { if (vis(e)) T.push(e); }); });
    const H = document.documentElement; let pts = 0, n = 0; const ex = [], who = {};
    for (const t of T) for (const rc of t.getClientRects()){ if (rc.width < 2 || rc.height < 2) continue;
      for (let y = rc.top + 1; y < rc.bottom - 0.5; y += step) for (let x = rc.left + 1; x < rc.right - 0.5; x += step){
        if (y < 1 || y > innerHeight - 1 || x < 1 || x > innerWidth - 1) continue; pts++;
        const a = document.elementFromPoint(x, y); if (inT(t, a)) continue;
        H.classList.add('__nh'); const b = document.elementFromPoint(x, y); H.classList.remove('__nh');
        if (inT(t, b)){ n++; const k = sig(t) + ' <- ' + (a ? sig(a) : 'null'); who[k] = (who[k] || 0) + 1; if (ex.length < 6) ex.push([sig(t), Math.round(x), Math.round(y), a ? sig(a) : null]); } } }
    return { targets: T.length, pts, steal: n, who, ex }; },
  /* 자리 재기 — 그 요소 위·아래로 남은 자리: 누를 것(TSEL)까지는 틈의 반 · 글이 든 칸까지는 틈 전부 · 팝업 안이면 그 창 안만 */
  room(el, rootSel){ const r = el.getBoundingClientRect(), L = r.left + 1, R = r.right - 1, pop = el.closest('.pop'); const cl = pop ? pop.getBoundingClientRect() : { top: -1e4, bottom: 1e4 };
    let up = r.top - cl.top, dn = cl.bottom - r.bottom; const same = e => pop ? pop.contains(e) : !e.closest('.pop');
    const root = document.querySelector(rootSel) || document.body; const C = [];
    root.querySelectorAll(TSEL).forEach(e => { if (e === el || e.contains(el) || el.contains(e) || !vis(e) || !same(e)) return; for (const q of e.getClientRects()) C.push([q, 1, sig(e)]); });
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); let tn;
    while ((tn = tw.nextNode())){ if (!tn.nodeValue.trim()) continue; const pe = tn.parentElement; if (!pe || !vis(pe) || el.contains(pe) || !same(pe) || pe.closest(TSEL)) continue;
      const q0 = pe.getBoundingClientRect(); if (q0.bottom < r.top - 60 || q0.top > r.bottom + 60) continue; for (const q of pe.getClientRects()) C.push([q, 0, sig(pe)]); }
    let bu = null, bd = null;
    for (const [q, isT, s] of C){ if (q.right <= L || q.left >= R || q.width < 1 || q.height < 1) continue;
      if (q.bottom <= r.top + 0.5){ const d = (r.top - q.bottom) / (isT ? 2 : 1); if (d < up){ up = d; bu = s; } }
      else if (q.top >= r.bottom - 0.5){ const d = (q.top - r.bottom) / (isT ? 2 : 1); if (d < dn){ dn = d; bd = s; } } }
    up = Math.max(0, up); dn = Math.max(0, dn);
    return { h: Math.round(r.height * 10) / 10, up: Math.round(up * 10) / 10, dn: Math.round(dn * 10) / 10, room: Math.round((r.height + up + dn) * 10) / 10, bu, bd }; },
  glyph(rootSel, every){ every = every || 2;
    const roots = [...document.querySelectorAll(rootSel)].filter(vis), H = document.documentElement; let pts = 0, n = 0; const ex = [];
    for (const R0 of roots){ const tw = document.createTreeWalker(R0, NodeFilter.SHOW_TEXT); let tn;
      while ((tn = tw.nextNode())){ const s = tn.nodeValue; if (!s || !s.trim()) continue; const pe = tn.parentElement; if (!pe || !vis(pe)) continue;
        for (let i = 0; i < s.length; i += every){ if (!s[i].trim()) continue;
          const rg = document.createRange(); rg.setStart(tn, i); rg.setEnd(tn, i + 1); const rc = rg.getBoundingClientRect(); if (rc.width < 1 || rc.height < 1) continue;
          const x = rc.left + rc.width / 2, y = rc.top + rc.height / 2; if (y < 1 || y > innerHeight - 1 || x < 1 || x > innerWidth - 1) continue; pts++;
          const a = document.elementFromPoint(x, y); if (a && (a === pe || pe.contains(a) || a.contains(pe))) continue;
          H.classList.add('__nh'); const b = document.elementFromPoint(x, y); H.classList.remove('__nh');
          if (b && (b === pe || pe.contains(b) || b.contains(pe))){ n++; if (ex.length < 6) ex.push([s.slice(Math.max(0, i - 3), i + 4), Math.round(x), Math.round(y), a ? sig(a) : null]); } } } }
    return { pts, steal: n, ex }; },
};
})();
</script>"""
if RF_TOOLS not in H.TOOLS:
    H.TOOLS = H.TOOLS + '\n' + RF_TOOLS


def app_src(x):
    return H.app_src(x)


RO_LOOP = 'ResizeObserver loop'


def real_errs(G, name, errs):
    """JS 오류 — ResizeObserver loop 알림(바탕도 냄 · 브라우저 알림일 뿐 앱 오류 아님)은 INFO 로 세고 뺀다"""
    ro = [e for e in errs if RO_LOOP in e]
    if ro:
        N(G, name + ' — ResizeObserver loop 알림(거름)', '%d 건' % len(ro))
    return [e for e in errs if RO_LOOP not in e]


def jload(d, name):
    return json.load(io.open(os.path.join(d, name), encoding='utf-8'))


def ovl(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


# 채팅 ① 표(20 링크 · 8 조) — (법, 인용한 조, 잘못 이어진 대상 조, 수)
CHAT_T1 = [('특허법', '제165조', '제108조', 1), ('특허법', '제165조', '제111조', 1), ('특허법', '제165조', '제112조', 1),
           ('특허법', '제209조', '제35조', 1), ('특허법', '제214조', '제25조', 4),
           ('상표법', '제152조', '제108조', 1), ('상표법', '제152조', '제111조', 1), ('상표법', '제152조', '제112조', 1), ('상표법', '제152조', '제116조', 1),
           ('디자인보호법', '제153조', '제108조', 1), ('디자인보호법', '제153조', '제111조', 1), ('디자인보호법', '제153조', '제112조', 1), ('디자인보호법', '제153조', '제116조', 1),
           ('디자인보호법', '제183조', '제16조', 1), ('디자인보호법', '제185조', '제10조', 1), ('디자인보호법', '제196조', '제7조', 2)]
VRULES = [('특허법', r'산업재산권법\1.특허법\조문', '특-'), ('상표법', r'산업재산권법\2.상표법\조문', '상-'),
          ('디자인보호법', r'산업재산권법\3.디보법\조문', '디-'), ('민사소송법', r'민사소송법\민소법조문', '민소-')]
JOKEY = re.compile(r'^(?:특|상|디|민소)-(제(\d+)조(?:의(\d+))?)(?:\((.*)\))?')
RAWLINK = re.compile(r'(?<!!)\[\[([^\[\]|]+)(?:\|([^\[\]|]+))?\]\]')


def law_of(rel):
    rel = rel.replace('/', '\\')
    return next(l for l, r, p in VRULES if rel.startswith(r))


def vault_census(root, only=None):
    """볼트(또는 사본) 조문 노트의 다른 법 인용 사슬 안 이 법 조 링크 — [(법, 파일, 줄, 대상, 표시)] · only = 볼 파일(상대) 집합 · 대상 = 볼트 그 법 조문 노트"""
    out = []
    V = JC.find_vault()[0]
    for law, rel, pre in VRULES:
        d = os.path.join(root, rel)
        if not os.path.isdir(d):
            continue
        allnames = {f[:-3] for f in os.listdir(os.path.join(V, rel)) if f.endswith('.md') and JOKEY.match(f)}
        for f in sorted(os.listdir(d)):
            if not (f.endswith('.md') and JOKEY.match(f)):
                continue
            if only is not None and os.path.join(rel, f) not in only:
                continue
            edit, _ = JC.split_note(io.open(os.path.join(d, f), encoding='utf-8').read())
            for li, ln in enumerate(edit):
                if '[[' not in ln:
                    continue
                plain, els, _b = JC.plainize(ln)
                for e in els:
                    if e['kind'] == 'link' and e['target'].split('#')[0] in allnames and JC.other_law_cite(plain[max(0, e['a'] - 160):e['a']]):
                        out.append((law, f, li, e['target'], e.get('disp')))
    return out


# ════════════════════════ B1 볼트 ════════════════════════
def b1():
    G = 'B1'
    if JC is None or not os.path.isdir(BK):
        N(G, 'N: 필요', '볼트 · 고치기 전 사본 · ⚙ jo_common 이 있는 본 세션에서만')
        return True
    M = jload(BK, '_목록.json')
    notes = M['노트']
    rels = {m['노트'].replace('/', '\\') for m in notes}
    N(G, '사본 · 목록', '%s · 노트 %d · 링크 %d · 법별 %s' % (BK, len(notes), len(M['링크']), dict(collections.Counter(law_of(x['노트']) for x in M['링크']))))
    if YARD:   # 헛잣대 — 고치기 전 사본에 대상이 남아 있다(= 이 잣대가 대상을 본다)
        left = vault_census(BK, rels)
        T(G, '볼트(고치기 전 사본) 대상 = 0', not left, '대상 %d(사본)' % len(left))
        return not left
    V = JC.find_vault()[0]
    bad, user = [], []
    for m in notes:
        rel = m['노트'].replace('/', '\\')
        ob = open(os.path.join(BK, rel), 'rb').read()
        nb = open(os.path.join(V, rel), 'rb').read()
        if hashlib.md5(ob).hexdigest() != m['md5']:
            bad.append((rel, '사본 md5'))
            continue
        old, new = ob.decode('utf-8'), nb.decode('utf-8')
        if hashlib.md5(nb).hexdigest() != m.get('고친 뒤 md5'):
            user.append(rel)   # 고친 뒤 사용자가 그 노트를 또 고쳤다 — 치환 대조 대신 대상 0 · 원본 칸만
        else:
            lines = old.split('\n')
            hits = {}
            for x in [x for x in M['링크'] if x['노트'] == m['노트']]:
                hits.setdefault(x['줄'] - 1, set()).add(x['차례'])
            for li, ns in hits.items():
                ln = lines[li]
                ms = list(RAWLINK.finditer(ln))
                for n in sorted(ns, reverse=True):
                    mm = ms[n]
                    ln = ln[:mm.start()] + (mm.group(2) if mm.group(2) is not None else mm.group(1)) + ln[mm.end():]
                lines[li] = ln
            if '\n'.join(lines) != new:
                bad.append((rel, '링크 → 보이는 글자 치환 말고 다른 글자가 다름'))
        if JC.split_note(old)[1] != JC.split_note(new)[1]:
            bad.append((rel, '원본 칸 다름'))
    left = vault_census(V)
    ok = not bad and not left
    T(G, '볼트 — 노트마다 링크 → 보이는 글자 치환만 · 원본 칸 무변 · 남은 대상 0(네 법 전수)', ok,
      {'노트': len(notes), '푼 링크': len(M['링크']), '어긋남': bad[:5], '남은 대상': len(left), '예': left[:3], '고친 뒤 사용자가 또 고친 노트': user})
    got = collections.Counter()
    for x in M['링크']:
        got[(law_of(x['노트']), JOKEY.match(x['노트'].split('/')[-1]).group(1), JOKEY.match(x['대상']).group(1))] += 1
    miss = [(l, j, t, n, got[(l, j, t)]) for l, j, t, n in CHAT_T1 if got[(l, j, t)] < n]   # 표 수 이상(디보 제183조 = 「헤이그협정 제16조」 · 「같은 협정 제16조」 둘 — 표는 뒤 하나만 셌다)
    T(G, '채팅 ① 표(20 링크 · 8 조) ⊂ 푼 링크', not miss, {'어긋남': miss, '표 밖 더 푼 것': sum(got.values()) - sum(n for *_, n in CHAT_T1)})
    return ok and not miss


# ════════════════════════ B2 데이터 · 규칙 한 벌 ════════════════════════
PARITY_JS = r"""(pres) => pres.map(s => { try{ return wmAutoOther(s) ? 1 : 0; }catch(e){ return -1; } })"""
CITE_JS = r"""async (a) => { const [law, B, jos] = a; const L = await get('jo_' + law + '_목록.json'); const TT = {}; L.조.forEach(x => { TT[x.k] = x.t || ''; });
  const out = {}; for (const jo of jos){ const j = B.조[jo]; if (!j){ out[jo] = null; continue; } try{ out[jo] = wmCiteOut(j, jo, TT); }catch(e){ out[jo] = ['ERR ' + e.message]; } } return out; }"""
SAMPLE = ['「민사소송법」 제98조부터 제103조까지, 제107조제1항ㆍ제2항, 제108조, ', '같은 협정 ', '헤이그협정 ', '“헤이그협정 ', '마드리드 의정서 ', '비송사건절차법 제248조 및 ',
          '이 법 ', '재판장의 명령 또는 제136조 및 ', '제136조제3항부터 제5항까지의 규정(', '「실용신안법」 제15조에 따라 준용되는 이 법 ', '법률 제5355호 상표법중개정법률 ',
          '국가(헤이그협정 ', '같은 법 시행령 ', '영업비밀(부정경쟁방지및영업비밀보호에관한법률 ']


def all_L(d):
    out = {}
    for law in LAWS:
        B = jload(d, 'jo_%s_본문.json' % law)
        for jo, j in B['조'].items():
            for ri, r in enumerate(j['행']):
                for e in r.get('e', []):
                    if e.get('k') == 'L':
                        out[(law, jo, ri, e['a'], e['b'])] = (e.get('to'), e.get('j'), r['t'][max(0, e['a'] - 160):e['a']], r['t'][e['a']:e['b']])
    return out


def b2(br):
    G = 'B2'
    if JC is None:
        N(G, 'N: 필요', '⚙ jo_common(다른 법 인용 규칙 파이썬 한 벌)이 있는 본 세션에서만')
        return True
    ok = True
    L1 = all_L(DATA)
    left = [(k[0], k[1], v[3]) for k, v in L1.items() if v[1] and JC.other_law_cite(v[2])]
    g1 = not left
    ok &= g1
    T(G, '네 법 본문 — 다른 법 인용 사슬 안 이 법 L 링크 0', g1, {'남음': len(left), '법별': dict(collections.Counter(x[0] for x in left)), '예': left[:4]})
    meta = jload(DATA, '_meta.json')
    lx = [r for r in meta.get('검산', []) if r.get('코드') == 'LX']
    g2 = bool(lx) and lx[0]['판정'] == 'OK' and lx[0]['실측'] == '버림 0'
    ok &= g2
    T(G, '⚙ 가드 로그 = 버림 0(데이터 _meta 검산 LX)', g2, lx[:1] or '검산 LX 없음(가드 없는 ⚙)')
    idx = jload(DATA, 'jo_링크역인덱스.json')
    chk = [('특허법:제108조', '제165조'), ('특허법:제35조', '제209조'), ('디자인보호법:제7조', '제196조')]
    g3 = all(w not in (idx.get(k) or []) for k, w in chk)
    ok &= g3
    T(G, '역인덱스 — 특허 제108조 ∌ 제165조 · 특허 제35조 ∌ 제209조 · 디보 제7조 ∌ 제196조', g3, {k: idx.get(k) for k, _ in chk})
    pn = H.dev_page(br, 'b2n', app_src(BASE if YARD else NEW), PC)
    pres = [v[2] for v in L1.values()]
    if not YARD:
        BD = data_dir(BASE)
        L0 = all_L(BD)
        pres += [v[2] for v in L0.values()]
        gone = [k for k in L0 if k not in L1]
        new = [k for k in L1 if k not in L0]
        chg = [k for k in L1 if k in L0 and L1[k][:2] != L0[k][:2]]
        M = jload(BK, '_목록.json')
        g4 = len(gone) == len(M['링크']) and not new and not chg
        ok &= g4
        T(G, '다른 L 링크 무변 — 빠진 것 = 볼트에서 푼 링크 수 · 새로 생김 0 · to/j 바뀜 0', g4, {'바탕 L': len(L0), '새 L': len(L1), '빠짐': len(gone), '푼 링크': len(M['링크']), '새로': len(new), '바뀜': len(chg)})
        bidx = jload(BD, 'jo_링크역인덱스.json')
        pi = sorted((k, len(bidx.get(k) or []), len(idx.get(k) or [])) for k in set(bidx) | set(idx) if (bidx.get(k) or []) != (idx.get(k) or []))
        citing = collections.defaultdict(set)
        for k in gone:
            citing[k[0]].add(k[1])
        pb = H.dev_page(br, 'b2b', app_src(BASE), PC)
        ins = {}
        for law in LAWS:
            jos = sorted(citing.get(law, []))
            if not jos:
                continue
            on = pn.ev(CITE_JS, [law, jload(DATA, 'jo_%s_본문.json' % law), jos])
            ob = pb.ev(CITE_JS, [law, jload(BD, 'jo_%s_본문.json' % law), jos])
            for jo in jos:
                a, b = ob.get(jo) or [], on.get(jo) or []
                if a != b:
                    ins[law + ' ' + jo] = '%d → %d(뺌 %s · 더함 %s)' % (len(a), len(b), '·'.join(x for x in a if x not in b) or '-', '·'.join(x for x in b if x not in a) or '-')
        pb.close()
        N(G, '바뀐 ↩피 셈(역인덱스 %d 열쇠)' % len(pi), ' · '.join('%s %d→%d' % x for x in pi))
        N(G, '바뀐 🔗인 셈(%d 조 · 바탕 앱+바탕 데이터 → 새 앱+새 데이터)' % len(ins), ' · '.join('%s %s' % kv for kv in sorted(ins.items())) or '없음')
        keep = {(k[0], k[1], v[1]) for k, v in L1.items() if v[1]}   # 인용 조에 같은 대상으로 가는 정상 링크가 남아 있으면 역인덱스에 남는 것이 맞다(상표 제152조 ③ 「제115조 또는 제116조」)
        miss = [(l, j, t) for l, j, t, n in CHAT_T1 if j not in (bidx.get(l + ':' + t) or []) or (j in (idx.get(l + ':' + t) or []) and (l, j, t) not in keep)]
        g5 = not miss
        ok &= g5
        T(G, '바뀐 셈이 ① 표와 맞다(표의 대상 조 ↩피 에서 인용 조가 빠짐 · 표 밖 더 찾은 것은 위 목록)', g5, {'어긋남': miss})
    corpus = sorted(set(pres + SAMPLE))
    js = pn.ev(PARITY_JS, corpus)
    py = [1 if JC.other_law_cite(s) else 0 for s in corpus]
    mis = [(s[-30:], a, b) for s, a, b in zip(corpus, js, py) if a != b]
    g6 = not mis
    ok &= g6
    T(G, '규칙 한 벌 — 앱 wmAutoOther = ⚙ other_law_cite(글 %d · 다른 법 %d)' % (len(corpus), sum(py)), g6, {'어긋남': len(mis), '예': mis[:5]})
    pn.close()
    return ok


# ════════════════════════ B3 화면 ════════════════════════
B3Q = r"""(a) => { const [head, word] = a; const box = document.querySelector('#slot .main .box'); if (!box) return null;
  const tw = document.createTreeWalker(box, NodeFilter.SHOW_TEXT); const nodes = []; let n; while ((n = tw.nextNode())) nodes.push(n);
  const str = nodes.map(x => x.nodeValue).join(''); const p = str.indexOf(head + word); if (p < 0) return null;
  const q0 = p + head.length; let k = 0, i = -1; while ((i = str.indexOf(word, i + 1)) >= 0 && i < q0) k++;
  const r = __RB.findText(box, word, k); if (!r) return null;
  const e = r.startContainer.parentElement; e.scrollIntoView({ block: 'center' }); const q = r.getBoundingClientRect(); const lk = e.closest('.wmlk, .joLink, a');
  return { cx: q.left + Math.min(q.width, 20) / 2, mx: q.left + q.width / 2, cy: q.top + q.height / 2, on: true, link: lk ? String(lk.className || lk.tagName) : null, ctx: (e.closest('.ln') || e).textContent.slice(0, 60) }; }"""


def b3(br):
    G = 'B3'
    ok = True
    p = H.dev_page(br, 'b3', app_src(BASE if YARD else NEW), PC2)
    cases = [('특허법', '제165조', '「민사소송법」 제98조부터 제103조까지, 제107조제1항ㆍ제2항, ', '제108조', ['제108조', '제111조', '제112조']),
             ('디자인보호법', '제173조', '헤이그협정 ', '제1조', ['제1조']),
             ('민사소송법', '제224조', '비송사건절차법 ', '제248조', ['제248조', '제250조'])]
    for law, jo, head, word, bad in cases:
        p.ev("async a => await __RB.jo(a[0], a[1], false)", [law, jo])
        p.wait(400)
        w = p.ev(B3Q, [head, word])
        link = w and w['link']
        if w:
            p.click(w['cx'], w['cy'], 800)
        pop = p.ev("() => POPS.filter(x => (x._pk || '').indexOf('jo|') === 0).map(x => (x.querySelector('.pt') || {}).textContent)")
        p.ev("() => closeAllPops(true)")
        outs = p.ev("async a => { const B = await get('jo_' + a[0] + '_본문.json'); return wmCiteOut(B.조[a[1]], a[1]); }", [law, jo])
        chip = p.ev("() => __RB.txt(document.querySelector('#slot .conn .plgb.wmin'))")
        good = bool(w) and not link and not pop and not any(b in (outs or []) for b in bad)
        ok &= good
        T(G, '%s %s 「…%s」 — 링크 없음 · 누르면 창 없음 · 🔗인 에 %s 없음' % (law, jo, (head + word)[-16:], '·'.join(bad)), good,
          {'링크': link, '뜬 창': pop, '🔗인 칩': chip, '🔗인': outs, '줄': w and w['ctx']})
    p.ev("async () => await __RB.jo('특허법', '제165조', false)")
    p.ev("() => { try{ window.getSelection().removeAllRanges(); }catch(e){} }")
    w = p.ev(B3Q, [cases[0][2], '제108조'])
    if w:
        p.pg.mouse.move(w['mx'] - 20, w['cy'])
        p.pg.mouse.down()
        p.pg.mouse.move(w['mx'] + 20, w['cy'])
        p.pg.mouse.up()
        p.wait(600)
    bar = p.ev("() => { const b = document.querySelector('.mk9bar, #c2mark'); return !!b && __RB.vis(b); }")
    T(G, '특허 제165조 「제108조」 끌어 고르기 → 칠 막대 뜸(링크 밖 글자 고르기 그대로)', bool(bar), bar)
    ok &= bool(bar)
    T(G, 'JS 오류', not p.errs, p.errs[:3])
    ok &= not p.errs
    p.close()
    return ok


# ════════════════════════ B4 1차객 서랍 넘침 ════════════════════════
JTQ = r"""() => { const L = document.getElementById('jtlist'); if (!L) return null; const lr = L.getBoundingClientRect();
  const over = [...L.querySelectorAll('.l1')].filter(e => e.getBoundingClientRect().right > lr.left + L.clientWidth + 0.5 || [...e.children].some(c => c.getBoundingClientRect().right > lr.left + L.clientWidth + 0.5)).slice(0, 4).map(e => (e.textContent || '').slice(0, 30));
  const rows = [...L.querySelectorAll('.jtit, .jtch')].map(r => { const q = r.getBoundingClientRect(); return [Math.round(q.width), Math.round(q.height * 10) / 10]; });
  const lab = [...L.querySelectorAll('.jtit .l1')].filter(l => l.querySelector('.jochips')).map(l => Math.round(l.querySelector('.tx').getBoundingClientRect().width));
  return { sw: L.scrollWidth, cw: L.clientWidth, over, rows, zeroLab: lab.filter(w => w < 1).length, labs: lab.length }; }"""


def jt_open(p):
    p.ev("async () => { await __RB.home('특허법'); S.jtFold = false; uiSave(); await render(); await __RB.idle(); }")
    p.wait(700)
    return p.ev(JTQ)


def b4(br, tag='b4', eng='chromium'):
    G = 'B4' if eng == 'chromium' else 'B4-wk'
    ok = True
    src = app_src(BASE if YARD else NEW)
    for dn, dev in (('폰390', PHONE), ('iPad834', PAD)):
        p = H.dev_page(br, tag + dn, src, dev)
        q = jt_open(p)
        good = bool(q) and q['sw'] <= q['cw'] and q['zeroLab'] == 0
        ok &= good
        T(G, '%s 1차객 문제 서랍 가로 넘침 0 · 이름 0 폭 줄 0' % dn, good, q and {'sw': q['sw'], 'cw': q['cw'], '넘친 줄': q['over'], '이름 0 폭': q['zeroLab'], '칩 달린 줄': q['labs']})
        p.close()
    if eng == 'chromium' and not YARD:
        pn, pb = H.dev_page(br, tag + 'pcN', src, PC), H.dev_page(br, tag + 'pcB', app_src(BASE), PC)
        qn, qb = jt_open(pn), jt_open(pb)
        same_dom = pn.ev("() => document.getElementById('jtlist').innerHTML") == pb.ev("() => document.getElementById('jtlist').innerHTML")
        diff = [i for i, (a, b) in enumerate(zip(qn['rows'], qb['rows'])) if a != b]
        good = same_dom and qn['sw'] <= qn['cw'] and len(qn['rows']) == len(qb['rows']) and len(diff) <= len(qb['over'])
        ok &= good
        T(G, 'PC — DOM = 착수 HEAD · 넘침 0(착수 HEAD 도 넘쳤다 → 넘친 줄만 크기 바뀜)', good,
          {'DOM 같음': same_dom, '넘침(새/바탕)': [qn['sw'] - qn['cw'], qb['sw'] - qb['cw']], '크기 바뀐 줄': len(diff), '바탕 넘친 줄': qb['over']})
        pn.close()
        pb.close()
    return ok


# ════════════════════════ B5 터치 누름 자리 · 격자 훑기 ════════════════════════
FOUR = [('연결 줄 칩', '#slot .main .conn>.plgb', '#slot .main .conn>.plgb', '#slot .main'), ('팝업 머리 단추', '.pop[data-rftop] .ph>button', '.pop .ph>button', '.pop[data-rftop]'), ('1차객 카드 칩', '#slot .mbqhd button.qb', '#slot .mbqhd button.qb', '#slot')]
ROOMQ = r"""([sel, root, n]) => [...document.querySelectorAll(sel)].filter(__RB.vis).slice(0, n || 6).map(e => { e.scrollIntoView({ block: 'center' }); return __RF.room(e, root); })"""
TOPPOP = r"""() => { let top = null, z = -1; document.querySelectorAll('.pop').forEach(p => { p.removeAttribute('data-rftop'); const zz = +p.style.zIndex || 0; if (zz >= z){ z = zz; top = p; } }); if (top) top.setAttribute('data-rftop', '1'); return !!top; }"""
LINKQ = r"""(sel) => [...document.querySelectorAll(sel)].filter(__RB.vis).slice(0, 4).map(e => { e.scrollIntoView({ block: 'center' }); const rs = [...e.getClientRects()]; const q = rs[0];
  const at = (x, y) => { const a = document.elementFromPoint(x, y); return !!a && (a === e || e.contains(a)); }; const cx = q.left + Math.min(q.width, 30) / 2;
  let up = 0, dn = 0; const cy = q.top + q.height / 2; while (up < 40 && at(cx, cy - up - 1)) up++; while (dn < 40 && at(cx, cy + dn + 1)) dn++;
  const cs = getComputedStyle(e), g = q.height - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
  return { t: (e.textContent || '').slice(0, 12), h: Math.round(q.height * 10) / 10, glyph: Math.round(g * 10) / 10, eff: up + dn + 1, frags: rs.length }; })"""


def open_two_pops(p):
    at = p.ev(r"""() => { const L = [...document.querySelectorAll('#slot .main .wmlk')].filter(__RB.vis); return L.length ? __RB.hitOn(L[0]) : null; }""")
    p.press(at, 900)
    at2 = p.ev(r"""() => { const L = [...document.querySelectorAll('#slot .main .wmlk')].filter(__RB.vis); return L.length > 1 ? __RB.hitOn(L[1]) : null; }""")
    if at2:
        p.press(at2, 900)


def meas_four(p):
    out = {}
    p.ev("async () => await __RB.jo('특허법', '제6조', false)")
    p.wait(300)
    out['연결 줄 칩'] = p.ev(H.MEAS, [FOUR[0][1], FOUR[0][2], 5])
    out['연결 줄 칩 자리'] = p.ev(ROOMQ, [FOUR[0][1], FOUR[0][3], 5])
    out['본문 조 링크'] = p.ev(LINKQ, '#slot .main .wml .wmlk, #slot .main .joLink')
    open_two_pops(p)
    p.ev(TOPPOP)
    out['팝업 머리 단추'] = p.ev(H.MEAS, [FOUR[1][1], FOUR[1][2], 4])
    out['팝업 머리 단추 자리'] = p.ev(ROOMQ, [FOUR[1][1], FOUR[1][3], 4])
    p.ev("() => closeAllPops(true)")
    p.ev("async () => await __RB.home('특허법')")
    p.ev("async k => await __RB.goKey(k)", H.U_PIN)
    p.wait(300)
    out['1차객 카드 칩'] = p.ev(H.MEAS, [FOUR[2][1], FOUR[2][2], 6])
    out['1차객 카드 칩 자리'] = p.ev(ROOMQ, [FOUR[2][1], FOUR[2][3], 6])
    return out


def grid_scan(p):
    """서랍(특허 · 민소) · 연결 줄·본문 · 팝업 · 1차객 카드 · 1차객 서랍 — 빼앗긴 점 · 글자"""
    out = {}
    for law, jo in (('특허법', '제6조'), ('민사소송법', '제30조')):
        p.ev("async a => { localStorage.removeItem('jopangi_ui_jofold'); await __RB.jo(a[0], a[1], true); const t = document.querySelector('#slot > .tree'); if (t) t.scrollTop = 0; }", [law, jo])
        p.wait(300)
        out['서랍 %s' % law] = p.ev("() => __RF.steal('#slot > .tree')")
    p.ev("async () => await __RB.jo('특허법', '제6조', false)")
    p.wait(300)
    out['연결 줄·본문'] = p.ev("() => __RF.steal('#slot .main')")
    out['본문 글자'] = p.ev("() => __RF.glyph('#slot .main .box', 2)")
    open_two_pops(p)
    out['팝업'] = p.ev("() => __RF.steal('.pop')")
    out['팝업 글자'] = p.ev("() => __RF.glyph('.pop .pb', 2)")
    p.ev("() => closeAllPops(true)")
    p.ev("async () => await __RB.home('특허법')")
    p.ev("async k => await __RB.goKey(k)", H.U_PIN)
    p.wait(300)
    out['1차객 카드'] = p.ev("() => __RF.steal('#slot')")
    out['1차객 카드 글자'] = p.ev("() => __RF.glyph('#slot .qwrap', 3)")
    p.ev("async () => { S.jtFold = false; uiSave(); await render(); await __RB.idle(); }")
    p.wait(300)
    out['1차객 서랍'] = p.ev("() => __RF.steal('#jtree')")
    return out


def b5(br, tag='b5', eng='chromium'):
    G = 'B5' if eng == 'chromium' else 'B5-wk'
    ok = True
    src = app_src(BASE if YARD else NEW)
    for dn, dev in (('폰390', PHONE), ('iPad834', PAD)):
        p = H.dev_page(br, tag + dn, src, dev)
        m = meas_four(p)
        for nm, arr in m.items():
            if nm.endswith(' 자리'):
                continue
            if nm == '본문 조 링크':
                good = bool(arr) and all(x['eff'] >= x['glyph'] + 2 for x in arr if x['frags'] == 1)
                T(G, '%s 본문 조 링크 실효 높이(제 줄 칸 안 · 줄 간격 21.9px 라 36 못 채움 — 적기)' % dn, good, arr)
                ok &= good
                continue
            rm = m.get(nm + ' 자리') or []
            rows, bad = [], []
            for x, rr in zip(arr, rm):
                need = min(36, rr['room']) - 1.5
                g1 = x['dh'] >= need and x['center'] and not x['steal']
                rows.append('%s %sx%s 설계 %sx%s 실제 %sx%s 자리 %s(위 %s %s · 아래 %s %s) 가로챔 %s 먼쪽 %s' % (x['t'], x['w'], x['h'], x['dw'], x['dh'], x['ew'], x['eh'], rr['room'], rr['up'], rr['bu'] or '끝', rr['dn'], rr['bd'] or '끝', x['steal'], x['near']))
                if not g1:
                    bad.append(rows[-1])
            good = bool(arr) and len(arr) == len(rm) and not bad
            ok &= good
            T(G, '%s %s 누름 높이 ≥ 36(이웃이 막으면 남은 자리까지 · 보이는 사각형 빼앗음 0)' % (dn, nm), good, bad or rows[:4])
        gs = grid_scan(p)
        for scr, r in gs.items():
            good = bool(r) and r['steal'] == 0 and r['pts'] > 0
            ok &= good
            d = dict(r) if r else {}
            T(G, '%s 격자 훑기 %s — 빼앗긴 점 0' % (dn, scr), good, d)
        er = real_errs(G, '%s JS 오류' % dn, p.errs)
        if er:
            ok = False
            T(G, '%s JS 오류' % dn, False, er[:3])
        p.close()
    if eng == 'chromium' and not YARD:
        pn, pb = H.dev_page(br, tag + 'pcN', src, PC), H.dev_page(br, tag + 'pcB', app_src(BASE), PC)
        mn, mb = meas_four(pn), meas_four(pb)
        for nm in mn:
            if nm.endswith(' 자리'):
                continue
            if nm == '본문 조 링크':
                same = mn[nm] == mb[nm]
                det = (mn[nm][:2], mb[nm][:2])
            elif nm == '팝업 머리 단추':
                # ★ jo_theme(10/1) A-7(_task_jo_theme.md 82줄) — 머리 단추 틀(12px 700 · 테두리 1px · 안쪽 2px 8px)로 보이는 크기가 바뀜 → 글자 차례 = 착수 HEAD · PC 누름 = 보이는 크기(±1 · 터치 넓힘이 PC 로 안 샘)
                same, det = H.pc_same(mn[nm], mb[nm])   # ★ 10/2 바로잡음 — 옛 잣대(착수 HEAD 와 같음)를 먼저 받고 아니면 A-7 꼴(옛 머리 앱은 모두 닫기 누름 20 vs 보이는 18.9 라 ±1 에 안 듦)
                same = same or ([x['t'] for x in mn[nm]] == [x['t'] for x in mb[nm]] and all(abs(x['dw'] - x['w']) <= 1 and abs(x['dh'] - x['h']) <= 1 for x in mn[nm]))
                det = ([(x['t'], x['w'], x['h'], x['dw'], x['dh']) for x in mn[nm]], [(x['t'], x['w'], x['h'], x['dw'], x['dh']) for x in mb[nm]])
            else:
                same, det = H.pc_same(mn[nm], mb[nm])
            ok &= same
            T(G, 'PC %s = 착수 HEAD' % nm, same, det)
        pn.close()
        pb.close()
    return ok


# ════════════════════════ B6 민소 편 목록 ════════════════════════
TREEQ = r"""() => { const t = document.querySelector('#slot > .tree'); if (!t) return null; const heads = [...t.querySelectorAll('.r.jhead, .r.jsub')];
  const st = t.querySelector('.jtbar .jstep');
  return { step: st ? st.textContent : null, heads: heads.map(h => [h.className, Math.round(parseFloat(getComputedStyle(h).paddingLeft)), __RB.txt(h.querySelector('.nm')).replace(/^[▾▸]\s*/, '').slice(0, 20), (h.querySelector('.jrange') || {}).textContent || '']) }; }"""
VISN = r"""() => [...document.querySelectorAll('#slot > .tree .r')].filter(__RB.vis).length"""


def tree_html(p, law):
    p.ev("async a => { localStorage.removeItem('jopangi_ui_jofold'); await __RB.jo(a, '제1조', true); }", law)
    p.wait(300)
    # ★ jo_theme(10/1) A-1(_task_jo_theme.md 14줄) — 머리 줄에 더해진 거름 점(.tmdot) · 「테마 N」(.tmtg)은 빼고 맞댄다(그 둘 말고 서랍 DOM 은 착수 HEAD 와 바이트 같음 · 10/2 잼)
    return p.ev("() => { const t = document.querySelector('#slot > .tree'); if (!t) return null; const c = t.cloneNode(true); c.querySelectorAll('.tmtg, .tmdot').forEach(e => e.remove()); return c.innerHTML; }"), p.ev(TREEQ)


def fold_seq(p, law):
    p.ev("async a => { localStorage.removeItem('jopangi_ui_jofold'); await __RB.jo(a, '제1조', true); }", law)
    p.wait(300)
    seq = []
    for _ in range(6):
        at = p.ev("() => { const b = document.querySelector('#slot > .tree .jtbar .jstep'); return b ? __RB.hitOn(b) : null; }")
        if not at:
            break
        seq.append(at['t'])
        p.press(at, 500)
        seq.append(p.ev(VISN))
        if at['t'] == '펴기':
            break
    return seq


def b6(br):
    G = 'B6'
    ok = True
    L = jload(DATA, 'jo_민사소송법_목록.json')
    H0 = L['장']
    pyeon = [i for i, h in enumerate(H0) if re.match(r'제\d+편', h['no'])]
    rows = []
    for i in pyeon:
        e = i + 1
        while e < len(H0) and not re.match(r'제\d+편', H0[e]['no']):
            e += 1
        ks = [x['k'] for x in L['조'] if x.get('j') is not None and i <= x['j'] < e]
        rows.append((H0[i]['no'], H0[i]['lv'], H0[i]['from'], H0[i]['to'], (ks[0], ks[-1]) if ks else ('', '')))
    lv_jang = {h['lv'] for h in H0 if re.match(r'제\d+장', h['no'])}
    g1 = len(pyeon) >= 4 and all(r[1] not in lv_jang and (r[2], r[3]) == r[4] for r in rows) and rows[0][2:4] == ('제1조', '제247조')
    ok &= g1
    T(G, '민소 목록 편 %d — 층 ≠ 장 층 · from/to = 하위 첫~마지막 조 · 제1편 = 제1조~제247조' % len(pyeon), g1, {'편': rows, '장 층': sorted(lv_jang)})
    src = app_src(BASE if YARD else NEW)
    p = H.dev_page(br, 'b6n', src, PC)
    _, q = tree_html(p, '민사소송법')
    pads = {}
    for c, pad, nm, rg in q['heads']:
        k = '편' if re.match(r'제\d+편', nm) else ('장' if re.match(r'제\d+장', nm) else '절')
        pads.setdefault(k, set()).add(pad)
    g2 = len(pads) == 3 and all(len(v) == 1 for v in pads.values()) and max(pads['편']) < min(pads['장']) < min(pads['절'])
    ok &= g2
    T(G, '민소 서랍 편 → 장 → 절 들여쓰기', g2, {k: sorted(v) for k, v in pads.items()})
    seq = fold_seq(p, '민사소송법')
    txt = [x for x in seq if isinstance(x, str)]
    nums = [x for x in seq if isinstance(x, int)]
    g3 = txt[:4] == ['접기1', '접기2', '접기3', '펴기'] and len(nums) >= 4 and nums[0] == len(pyeon) and nums[0] < nums[1] < nums[2] < nums[3]
    ok &= g3
    T(G, '민소 단계 접기 = 깊이 셋(접기1 편만 → 접기2 +장 → 접기3 +절 → 펴기 전부)', g3, seq)
    mism = []
    for law in LAWS:
        _, qq = tree_html(p, law)
        LL = jload(DATA, 'jo_%s_목록.json' % law)
        drng = {}
        for h in LL['장']:
            drng[(h['no'] + ' ' + (h.get('t') or '')).strip()[:20]] = ('%s~%s' % (h['from'], h['to'])) if h['from'] and h['to'] else ''
        for c, pad, nm, rg in qq['heads']:
            if 'jsub' in c:
                continue
            if nm[:20] in drng and drng[nm[:20]] != rg:
                mism.append((law, nm, rg, drng[nm[:20]]))
    g4 = not mism
    ok &= g4
    T(G, '화면 머리 범위(revfix0929b 하위 셈 길) = 데이터 from~to(네 법 · 둘이 다르면 FAIL)', g4, mism[:5])
    if not YARD:
        pb = H.dev_page(br, 'b6b', app_src(BASE), PC)
        same = []
        for law in ('특허법', '상표법', '디자인보호법'):
            hn, _qn = tree_html(p, law)
            hb, _qb = tree_html(pb, law)
            fn, fb = fold_seq(p, law), fold_seq(pb, law)
            same.append((law, hn == hb, fn == fb, fn))
        g5 = all(s[1] and s[2] for s in same)
        ok &= g5
        T(G, '특허 · 상표 · 디보 서랍 DOM · 접기 글자·동작 = 착수 HEAD', g5, same)
        _, qo = tree_html(pb, '민사소송법')
        N(G, '옛 앱 + 새 데이터 — 민소 서랍(보고용 · 새로고침 안 한 탭 · 아이패드 PWA)', {'머리 갈래': dict(collections.Counter(h[0] for h in qo['heads'])), '접기': fold_seq(pb, '민사소송법')})
        pb.close()
    T(G, 'JS 오류', not p.errs, p.errs[:3])
    ok &= not p.errs
    p.close()
    return ok


# ════════════════════════ B7 장 머리 한 줄 ════════════════════════
B7Q = r"""() => { const t = document.querySelector('#slot > .tree'); if (!t) return null; const hs = [...t.querySelectorAll('.r.jhead')].filter(__RB.vis);
  const hh = hs.map(h => Math.round(h.getBoundingClientRect().height * 10) / 10);
  const rs = hs.map(h => h.querySelector('.jrange')).filter(Boolean);
  const clip = rs.filter(r => r.scrollWidth > r.clientWidth + 0.5).map(r => r.textContent);
  const out = rs.filter(r => { const a = r.getBoundingClientRect(), b = r.closest('.r').getBoundingClientRect(); return a.right > b.right + 0.5 || a.width < 1; }).map(r => r.textContent);
  const long = hs.map(h => h.querySelector('.nm')).filter(n => /제10장/.test(n.textContent)).map(n => ({ sw: n.scrollWidth, cw: n.clientWidth, to: getComputedStyle(n).textOverflow, title: n.title }));
  return { n: hs.length, min: Math.min(...hh), max: Math.max(...hh), clip, out, long, sw: t.scrollWidth, cw: t.clientWidth }; }"""


def b7(br):
    G = 'B7'
    ok = True
    src = app_src(BASE if YARD else NEW)
    for nm, dev, tw in (('폰390', PHONE, None), ('iPad834', PAD, None), ('PC212', PC, 212), ('PC276', PC, 276), ('PC320', PC, 320)):
        p = H.dev_page(br, 'b7' + nm, src, dev)
        for law in LAWS:
            p.ev("async a => { localStorage.removeItem('jopangi_ui_jofold'); if (a[1]) { S.treeW = a[1]; document.documentElement.style.setProperty('--trw', a[1] + 'px'); } await __RB.jo(a[0], '제1조', true); }", [law, tw])
            q = p.ev(B7Q)
            good = bool(q) and q['n'] > 0 and 28 <= q['min'] and q['max'] <= 32 and not q['clip'] and not q['out'] and q['sw'] <= q['cw']
            if law == '특허법' and q and q['long']:
                L0 = q['long'][0]
                good = good and bool(L0['title']) and (L0['sw'] <= L0['cw'] or L0['to'] == 'ellipsis')
            ok &= good
            T(G, '%s %s 머리 높이 30±2 · 범위 잘림 0 · 서랍 넘침 0' % (nm, law), good, q)
        p.close()
    return ok


# ════════════════════════ B8 교재 자리 창 자리 ════════════════════════
NCB_JS = r"""async (y) => { S.law = '민사소송법'; const [{ N }, NCA] = await Promise.all([noteData(), ncData()]); const P = (NCA || {}).p || {}; let f = null, e = null;
  for (const k of Object.keys(P)){ for (const en of Object.keys(P[k] || {})){ const v = P[k][en]; if (v && (v.b || []).length){ f = k; e = en; break; } } if (f) break; }
  if (!f) return null; document.querySelectorAll('.__rfchip').forEach(x => x.remove());
  const b = document.createElement('button'); b.className = '__rfchip'; b.textContent = '📘'; b.style.cssText = 'position:fixed;left:300px;top:' + (y - 10) + 'px;width:28px;height:20px;z-index:1;padding:0;border:1px solid #999';
  document.body.appendChild(b); b.onclick = ev => { ev.stopPropagation(); ncBookOpen(f, e, ev); };
  const r = b.getBoundingClientRect(); return { file: f, end: e, cx: r.left + r.width / 2, cy: r.top + r.height / 2, on: true, x: r.left, y: r.top, r: r.right, b: r.bottom }; }"""
NCB_R = r"""() => { const w = POPS.filter(x => (x._pk || '').indexOf('ncbook|') === 0).pop(); if (!w) return null; const r = w.getBoundingClientRect(); const B = __RB.vv();
  return { rect: [r.left, r.top, r.right, r.bottom], vv: [B.w, B.h], over: !!w._bkOver }; }"""


def b8(br):
    G = 'B8'
    ok = True
    src = app_src(BASE if YARD else NEW)
    for (W, Hh, touch) in ((1440, 900, False), (1511, 1043, False), (834, 1194, True)):
        ys = (300, 500, 700, 850)
        p = H.Pg(br, 'chromium', 'b8%d' % W, src, W, Hh, touch=touch, dsf=2 if touch else 1)
        p.ev("async () => await __RB.home('특허법')")
        p.ev("() => __RB.wordsDelay(400)")
        for pic in (False, True):
            if pic:
                p.ev("a => __RB.pinSeed(a[0], a[1], a[2])", [H.U_PIN, H.PIN_P, H.PIN_R])
            p.ev("async k => await __RB.goKey(k)", H.U_PIN)
            for y in ys:
                at, b = H.open_box(p, H.U_PIN, y, pic)
                p.wait(500)
                b = p.ev("() => __RB.box()")
                over = p.ev("() => { const w = POPS.filter(x => /^cell\\|📚/.test(x._pk || '')).pop(); return !!(w && w._bkOver); }")
                if not (at and b):
                    ok = False
                    T(G, '%d×%d %s 칩 y %d' % (W, Hh, '그림' if pic else '그림 없음', y), False, '창·칩 못 잼')
                    continue
                chip = [at['x'], at['y'], at['r'], at['b']]
                win = [b['rect']['x'], b['rect']['y'], b['rect']['r'], b['rect']['b']]
                o = ovl(chip, win)
                good = (o == 0 or over) and win[1] >= 7.5 and win[3] <= b['vv']['h'] - 7.5 and bool(b['sz']) and b['sz']['on'] and (b['pic'] if pic else True)
                ok &= good
                T(G, '%d×%d %s 칩 y %d — 칩 안 덮음 · 화면 안 · 손잡이' % (W, Hh, '그림' if pic else '그림 없음', y), good,
                  {'칩': [round(v) for v in chip], '창': [round(v) for v in win], '겹침': round(o), '④ 덮기 허용': over, '손잡이': b['sz'] and b['sz']['on'], '그림': b['pic']})
        p.ev("() => __RB.closeBox()")
        for y in (500, 700):
            at = p.ev(NCB_JS, y)
            if not at:
                T(G, '%d×%d 목차노트 교재 자리 창 y %d' % (W, Hh, y), False, '목차노트 짝 없음')
                ok = False
                continue
            p.press(at, 1500)
            q = p.ev(NCB_R)
            chip = [at['x'], at['y'], at['r'], at['b']]
            o = ovl(chip, q['rect']) if q else -1
            good = bool(q) and (o == 0 or q['over']) and q['rect'][1] >= 7.5 and q['rect'][3] <= q['vv'][1] - 7.5
            ok &= good
            T(G, '%d×%d 목차노트 교재 자리 창 y %d — 칩 안 덮음 · 화면 안' % (W, Hh, y), good, q and {'칩': [round(v) for v in chip], '창': [round(v) for v in q['rect']], '겹침': round(o), '④': q['over']})
            p.ev("() => { closeAllPops(true); document.querySelectorAll('.__rfchip').forEach(x => x.remove()); S.law = '특허법'; }")
        if p.errs:
            ok = False
            T(G, 'JS 오류 %d' % W, False, p.errs[:3])
        p.close()
    if not YARD:
        rs = {}
        for which, s in (('new', src), ('base', app_src(BASE))):
            p = H.Pg(br, 'chromium', 'b8ph' + which, s, 390, 844, touch=True, dsf=3)
            p.ev("async () => await __RB.home('특허법')")
            p.ev("a => __RB.pinSeed(a[0], a[1], a[2])", [H.U_PIN, H.PIN_P, H.PIN_R])
            p.ev("() => __RB.wordsDelay(400)")
            p.ev("async k => await __RB.goKey(k)", H.U_PIN)
            rr = []
            for y in (300, 420, 600, 420):
                at, b = H.open_box(p, H.U_PIN, y, True)
                ph = p.ev("() => { const w = POPS.filter(x => /^cell\\|📚/.test(x._pk || '')).pop(); const h = w && w.querySelector('.ph'); return h ? +h.getBoundingClientRect().height.toFixed(2) : null; }")   # ★ jo_theme(10/1) 머리 높이
                rr.append(b and [round(b['rect']['y']), round(b['rect']['b']), ph])
            rs[which] = rr
            p.close()
        # ★ jo_theme(10/1) A-7(_task_jo_theme.md 82줄) — 창 머리(.ph) 높이가 바뀜(chromium 31.44 → 39) → 「그대로(±2)」 또는 「아래 끝 +머리 차 · 또는 바닥 붙은 창 위 끝 −머리 차(±2)」
        dph = lambda a, b: (a[2] or 0) - (b[2] or 0)
        same8 = lambda a, b: (abs(a[0] - b[0]) <= 2 and abs(a[1] - b[1]) <= 2) or (abs(a[0] - b[0]) <= 2 and abs(a[1] - b[1] - dph(a, b)) <= 2) or (abs(a[1] - b[1]) <= 2 and abs(a[0] - b[0] + dph(a, b)) <= 2)
        good = all(a and b and same8(a, b) for a, b in zip(rs['new'], rs['base']))
        ok &= good
        T(G, '폰 390 교재 자리 창 = 착수 HEAD(±2 · 칩 y 300→420→600→420)', good, rs)
    return ok


# ════════════════════════ B9 화면 훑기 ════════════════════════
def sweep_more(br, src, tag, dev):
    out, errs = H.sweep_screens(br, src, tag, dev)
    p = H.dev_page(br, tag + 'x', src, dev)
    touch = dev in (PHONE, PAD)
    p.ev("async () => await __RB.jo('민사소송법', '제30조', true)")
    out['조문 화면(민소 서랍)'] = p.ev("a => __RB.sweep(a[0], a[1])", ['#slot > .tree', touch])
    p.ev("async () => { await __RB.home('특허법'); S.jtFold = false; uiSave(); await render(); await __RB.idle(); }")
    out['1차객 서랍'] = p.ev("a => __RB.sweep(a[0], a[1])", ['#jtree', touch])
    errs = list(errs) + p.errs
    p.close()
    return out, errs


def b9(br):
    G = 'B9'
    ok = True
    for dn, dev in (('PC', PC), ('폰390', PHONE), ('iPad834', PAD)):
        n, en = sweep_more(br, app_src(NEW), 'b9N' + dn, dev)
        b, eb = sweep_more(br, app_src(BASE), 'b9B' + dn, dev)
        for scr in n:
            nn = set(H.B12_RENAME.get(x, x) for x in n[scr])   # ★ jo_theme(10/1) — revfix0929b B12 와 같은 고침: 「이동 ↗」 이름표 = 옛 「뷰로 이동 ↗」(A-7 85줄)
            new = sorted(nn - set(b.get(scr, [])))
            gone = sorted(set(b.get(scr, [])) - nn)
            dot = None
            if H.B12_DOT in new and dev in (PHONE, PAD):   # ★ 거름 점 = fix1 A-34-3(_task_jo_theme_fix1.md 57줄) 잣대로 따로 잰다(높이 ≥ 36 · 가운데 · 가로챔 0)
                dot = H.b12_dot(br, app_src(NEW), 'b9D' + dn, dev)
                if dot[0]:
                    new.remove(H.B12_DOT)
            good = not new
            ok &= good
            det = {'새로': new[:6], '없어짐': gone[:4], '남은(바탕에도 있음)': len(nn & set(b.get(scr, [])))}
            if dot:
                det['거름 점(fix1 A-34-3 · 높이 ≥ 36 · 가로 값 적기)'] = dot[1]
            T(G, '%s %s 새로 생긴 흠 0' % (dn, scr), good, det)
        en = [e for e in en if 'ResizeObserver loop' not in e]
        if en:
            ok = False
            T(G, '%s JS 오류' % dn, False, en[:3])
    return ok


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    print('관문 _task_jo_revfix0930%s · 앱 = %s · 데이터 = %s · 바탕 = %s' % (' — 헛잣대' if YARD else '', BASE if YARD else NEW, DATA, BASE))
    got = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        steps = [('B1', lambda: b1()), ('B2', lambda: b2(br)), ('B3', lambda: b3(br)), ('B4', lambda: b4(br)), ('B5', lambda: b5(br)),
                 ('B6', lambda: b6(br)), ('B7', lambda: b7(br)), ('B8', lambda: b8(br)), ('B9', lambda: b9(br))]
        for g, fn in steps:
            if ONLY and g not in ONLY:
                continue
            if YARD and g == 'B9':
                N(g, '헛잣대 해당 없음', '화면 훑기 = 새 판 흠 − 바탕 흠 · 바탕끼리 견주면 늘 0(잣대가 아니라 잠금)')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            print('   (%s %.0f초)' % (g, time.time() - t1), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and (not ONLY or 'WK' in ONLY):
            wk = H.webkit_try(pw)
            if wk:
                for g, fn in (('B4', lambda: b4(wk, 'wk4', 'webkit')), ('B5', lambda: b5(wk, 'wk5', 'webkit'))):
                    print('── %s-wk' % g, flush=True)
                    try:
                        fn()
                    except Exception as e:
                        T(g + '-wk', 'WebKit 돌다 멈춤', False, str(e).splitlines()[0][:200])
                wk.close()
    lines = []
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    for g in sorted(got, key=lambda x: int(x[1:])):
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = ('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL')
        s = '  %-4s %s (%d 칸 중 FAIL %d)' % (g, verdict, len(cells), nf)
        print(s)
        lines.append(s)
    wkc = [r for r in RES if r[0].endswith('-wk') and r[2] is not None]
    if wkc:
        s = '  WK   %s (%d 칸 중 FAIL %d)' % ('PASS' if all(r[2] for r in wkc) else 'FAIL', len(wkc), sum(1 for r in wkc if not r[2]))
        print(s)
        lines.append(s)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
