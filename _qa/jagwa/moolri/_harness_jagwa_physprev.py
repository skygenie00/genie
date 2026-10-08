# -*- coding: utf-8 -*-
r"""_task_jagwa_physprev §B 관문 — 자과 물리 미리보기 = 발문 앞 글자(ABBYY) + 작은 그림

  python _harness_jagwa_physprev.py [--new <앱 파일 | genie git 판>] [--base <앱 파일 | git 판>] [--prev <미리보기.json>] [--spd <studyplandata 자리>]
                                    [--orig <원본 합본 PDF>] [--check <표본 폴더>] [--eng chromium,webkit] [--only B1,B2,B3,B4,B5,B6] [--res <결과>]

  NEW  = 이 판 앱(기본 genie jagwa/index.html) · BASE(헛잣대) = 착수 HEAD 의 앱 = merge-jagwa d3762af(자과 한 번에 합치기 — physphone · revfix0928_0929 · search_claude · 그 뒤 c04b3b7 은 _qa 만 고쳐 앱이 같다)
  미리보기 = studyplandata phys/미리보기.json(기본 SPD_ROOT · --prev 로 다른 파일) — 앱이 받는 길(api.github.com contents)을 Playwright route 가 그 파일로 준다(밖으로 안 나감)
  관문
    B1 뽑기 전수 — 577칸 · 열쇠 = 물리 GGU(P+번호) · c = F.CODE · src 수(abbyy/orig/none) · none 목록 · 머리 줄 꼴 0 · 〈보기〉 머리·선택지(① 과 ② 함께) 0 · 그림 자리 꼴
    B2 표본 대조 — 무작위 20문항(시드 고정 · 장마다 고르게) 발문 글 · 그림 자리를 원본 쪽 그림과 나란히 한 장씩 → --check 폴더(채팅 검수 · 눈으로)
    B3 앱 — 폰 390 · 아이패드 820 · PC 1440 × 첫 화면 · 📋 정리 창 1.1
         미리보기 빈 줄 0(none 뺌) · 글 = t 전부(줄 수 안 자름 · 잘림 0) · 〈보기〉·선택지 0 · 그림 높이 ≤ 44 · 폭 ≤ 줄 60% · 그림 없는 문항 그림 칸 0 · 줄 가로 넘침 0
         그림은 보일 때만(처음 화면 밖 줄 그림 0 · 화면 안 줄은 그려짐) · 첫 화면 처음 그리기 시간 = 바탕 ±20%(PC · 번갈아 다시 열기 다섯 번씩 · 첫 번 데움 빼고 넷의 가운데 값 · 미리보기 받기는 첫 그리기 뒤)
    B4 검색 — ABBYY 에만 있는 말 표본 셋(쪽 16 「자동차의 속력」 + BODY 가 빈 문항의 t 에서 고른 둘) → 물리 검색 결과에 그 문항 · 바탕 0건(헛잣대)
    B5 D11 — 앱에 미리보기 글(t) 0 · 앱 파일 _d11_scan 걸림 0(N: 이 있을 때)
    B6 화면 훑기(규칙 60) — 첫 화면 · 정리 창 × 세 기기 — 새로 생긴 넘침·잘림·덮임·작은 누름 0(바탕과 견줌 · physphone 의 __H.sweep)
  기기 = 브라우저 문맥 하나 · 기록·시험지·미리보기 = studyplandata 로컬 사본(가짜 원격 · PUT 은 담기만) · 서버·route = _harness_jagwa_physphone 그대로 불러 씀
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — 글자 · 자리 · 개수 · getBoundingClientRect · 그림이 실제로 보이는지는 「사용자 확인」(B2 표본은 채팅 눈 검수)
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import json, os, random, re, statistics, subprocess, sys, time   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('jagwa', 'index.html'))
BASEF = ARG('--base', 'd3762af')   # 착수 HEAD(merge-jagwa — 세 판 합친 뒤 · physprev 앞) · 커밋 뒤에도 이 판에 박는다(A-6 꼴)
SPD = ARG('--spd', _roots.spd())
PREVF = ARG('--prev', os.path.join(SPD, 'phys', '미리보기.json'))
NR = _roots.n_root()
ORIGF = ARG('--orig', os.path.join(HERE, '물리시험지_합본549.pdf'))
CHECK = ARG('--check', os.path.join(HERE, '_physprev_check'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_physprev_result.txt'))
JG.conf(SPD_PP=SPD)   # 가짜 원격(JG.Remote)이 읽는 studyplandata 자리 — 옛 PP.SPD = SPD(physphone 모듈 값)
F = dict(NO=0, PG=1, FILE=2, FPG=3, BIG=4, SUB=5, LNO=6, STAR=7, TYPE=8, CODE=9, YEAR=10, SRC=11, LV=12, ANS=13, BODY=14, VLT=15)
MOFF = {'111': 0, '222': 99, '333': 206, '444': 303, '555': 410, '666': 500}
RES = []   # 옛 RES = PP.RES(physphone 의 결과 통) — 제 통(아래 T · N 사본이 여기 담는다)
# ← jagwa/moolri/_harness_jagwa_physphone.py:355-359 T 사본(글자 그대로 · 갈래 ④ · JG 밖 — 띄우기가 아니라 옮기지 않음)
def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:700]), flush=True)
    return ok

# ← jagwa/moolri/_harness_jagwa_physphone.py:362-365 N 사본(글자 그대로 · 갈래 ④ · JG 밖 — 띄우기가 아니라 옮기지 않음)
def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:900]), flush=True)
RX_HEAD = re.compile(r'답\s*[①-⑤]|PEM\d+|변리사\s*[］\]]')
RX_TAIL = re.compile(r'[-─—]{3,}\s*[<＜〈]?\s*보\s*기\s*[>＞〉]?\s*[-─—]{3,}')


def want(g):
    return not ONLY or g in ONLY


# ── _task_qa_slim2 A-1·A-2(10/8 · J2) regress 갈래 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 도우미(gate 에서 도는 줄은 글자 그대로) ──
#   regress = NEW 만 띄운다(바탕 d3762af 풀기 · 띄우기 0) · B3-헛 · B4 「바탕은 그 문항 없음」 · B2 표본 PNG(PDF 렌더) · B5 _d11_scan(하위 파이썬 · g_push 가 잼) · B6 📋 정리 창(합침→physphone B7) = gate 만
#   「= 바탕」 칸(B3 첫 그리기 시간 · B5 바탕에 있던 글 · B6 새로 생긴 흠) = QC.base 기준 스냅샷(앞 인도판의 같은 칸 새 판 값 · 미리보기 글은 md5 만)
#   smoke = chromium 폰 390 한 판 — B3 첫 화면 · 📋 1.1 칸(+ 그 쪽 JS 오류)
_RG_KEEP = set(x for x in (os.environ.get('QA_SLIM_KEEP_FIXED') or '').split(',') if x)   # 흔들리는 자리만 고정 대기로 되돌리는 손잡이(자리 이름 쉼표 · * = 전부)
_RG_JNW = "()=>{const b=document.getElementById('jnw');const p=b&&b.querySelector(':scope>.panel');return !!p&&p.classList.contains('float')}"   # 표지 = jnOpen 끝 makeFloat(동기 · 창 섬)


def _rg_cid(name, *parts):
    return '%s%s' % (name, ''.join('@' + str(x) if i == 0 else '/' + str(x) for i, x in enumerate(parts)))


def _rg_wait(p, ms, js, what):
    """regress — 고정 대기 대신 앱 표지(상한 = gate 의 ms · 못 만나면 남은 시간을 채워 gate 와 같은 길이) · QA_SLIM_KEEP_FIXED 자리는 고정"""
    if js is None or what in _RG_KEEP or '*' in _RG_KEEP:
        QC.sleep(ms, what, p.pg)
        return
    t = time.time()
    if not QC.until(p.pg, js, ms, what):
        left = ms - (time.time() - t) * 1000.0
        if left > 1:
            p.pg.wait_for_timeout(left)


def _rg_first_draw_ms(br, src, n=5):
    """regress — first_draw_ms 의 새 판 몫만(바탕 문맥 0) · 같은 차례(다시 열기 n 번 · 첫 번 데움)"""
    QC.launch('new')
    pn = JG.fresh(br, 'b3t_new', src, 'phys', JG.PC, remote=Rem())
    tn, tv = [], []
    try:
        pn.ctx.add_init_script(FD_JS)
        for i in range(n):
            pn.pg.reload(wait_until='load')
            pn.pg.wait_for_function("() => window.__fd !== null && window.__fd !== undefined", timeout=90000)
            pn.wait(1500)
            tn.append(round(pn.ev("() => window.__fd"), 1))
            v = pn.ev("() => window.__pv")
            tv.append(round(v, 1) if v is not None else None)
    finally:
        pn.close()
    return tn, tv


def src_of(x):
    return JG.app_src(x)


def data_of(src):
    i = src.index('const DATA = [')
    j = src.index('\n', i)
    return json.loads(src[i:j].rstrip('\r').rstrip()[len('const DATA = '):].rstrip(';'))


def uid(r):
    return 'P%03d' % r[F['NO']]


def leak(t):
    return ('①' in t and '②' in t) or bool(RX_TAIL.search(t))


class Rem(JG.Remote):
    """가짜 원격 — phys/미리보기.json 만 --prev 파일로(없으면 404 = 앱은 지금처럼 BODY)"""
    def get(self, repo, path):
        if path.strip('/') == 'phys/미리보기.json' and repo.endswith('/studyplandata'):
            return open(PREVF, 'rb').read() if PREVF and os.path.isfile(PREVF) else None
        return super().get(repo, path)


# ── B1 ─────────────────────────────────────────────────────────────────────────────────────────
def b1(PV, DATA):
    G = 'B1'
    keys = {uid(r): r for r in DATA}
    miss = sorted(set(keys) - set(PV))
    extra = sorted(set(PV) - set(keys))
    badc = sorted(k for k, v in PV.items() if k in keys and v.get('c') != keys[k][F['CODE']])
    srcs = {}
    for v in PV.values():
        srcs[v.get('src')] = srcs.get(v.get('src'), 0) + 1
    none = sorted(k for k, v in PV.items() if v.get('src') == 'none')
    none_bad = [k for k in none if PV[k].get('t')]
    empty_bad = [k for k, v in PV.items() if v.get('src') != 'none' and not str(v.get('t') or '').strip()]
    head = sorted(k for k, v in PV.items() if RX_HEAD.search(str(v.get('t') or '')))
    tail = sorted(k for k, v in PV.items() if leak(str(v.get('t') or '')))
    figbad = []
    for k, v in PV.items():
        r = keys.get(k)
        f = v.get('fig')
        if r is None:
            continue
        if r[F['FILE']] == 'IMG':
            if f != 'img':
                figbad.append(k)
        elif not (isinstance(f, list) and all(isinstance(x, list) and len(x) == 4 and 0 <= x[0] < x[2] <= 1 and 0 <= x[1] < x[3] <= 1 for x in f)):
            figbad.append(k)
    nfig = {}
    for v in PV.values():
        kk = 'img' if v.get('fig') == 'img' else str(len(v.get('fig') or []))
        nfig[kk] = nfig.get(kk, 0) + 1
    T(G, '미리보기.json 577칸 = DATA 행마다 하나(열쇠 = GGU · c = F.CODE)', len(PV) == len(DATA) == 577 and not miss and not extra and not badc,
      {'칸': len(PV), 'DATA': len(DATA), '빠짐': miss[:5], '남음': extra[:5], 'c 다름': badc[:5]})
    T(G, 'src 수 · none 은 글 0 · 나머지는 글 있음', not none_bad and not empty_bad, {'src': srcs, 'none': len(none), 'none 인데 글': none_bad[:5], '글 없음': empty_bad[:5]})
    N(G, 'none 목록', ' '.join('%s(%s)' % (k, PV[k].get('c')) for k in none))
    T(G, '발문 글에 쪽 머리 줄 꼴(「답 ①~⑤」 · 「PEM\\d+」 · 「변리사 ］」) 0', not head, head[:10])
    T(G, '〈보기〉 머리 · 선택지(① 과 ② 함께) 0', not tail, tail[:10])
    T(G, '그림 자리 꼴 — IMG 행 = "img" · 나머지 = [[x0,y0,x1,y1]…](0~1 · x0<x1 · y0<y1)', not figbad, {'틀림': figbad[:8], '그림 수': nfig})
    return not (miss or extra or badc or none_bad or empty_bad or head or tail or figbad)


# ── B2 ─────────────────────────────────────────────────────────────────────────────────────────
def b2(PV, DATA):
    G = 'B2'
    if not os.path.isfile(ORIGF):
        N(G, '표본 대조', 'N: 필요(원본 합본 PDF 없음 — %s) · 건넘' % ORIGF)
        return True
    import pymupdf
    from PIL import Image, ImageDraw, ImageFont
    rng = random.Random(20261001)
    by = {}
    for r in DATA:
        if r[F['FILE']] != 'IMG' and PV.get(uid(r), {}).get('src') != 'none':
            by.setdefault(r[F['BIG']], []).append(r)
    bigs = sorted(by)
    pick = []
    i = 0
    while len(pick) < 20:   # 장마다 돌아가며 하나씩(고르게)
        b = bigs[i % len(bigs)]
        cand = [r for r in by[b] if r not in pick]
        if cand:
            pick.append(rng.choice(cand))
        i += 1
    os.makedirs(CHECK, exist_ok=True)
    for f in os.listdir(CHECK):
        if f.endswith('.png'):
            os.remove(os.path.join(CHECK, f))
    doc = pymupdf.open(ORIGF)
    font = None
    for fp in (r'C:\Windows\Fonts\malgun.ttf', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'):
        if os.path.isfile(fp):
            font = ImageFont.truetype(fp, 17)
            break
    font = font or ImageFont.load_default()
    made = []
    for n, r in enumerate(pick, 1):
        k = uid(r)
        e = PV[k]
        p = MOFF[r[F['FILE']]] + r[F['FPG']]
        pg = doc[p - 1]
        W, H = pg.rect.width, pg.rect.height
        clip = pymupdf.Rect(0, 0, W, H * 0.62)
        pix = pg.get_pixmap(dpi=110, clip=clip)
        im = Image.frombytes('RGB', (pix.w, pix.h), pix.samples)
        d = ImageDraw.Draw(im)
        k2 = 110 / 72.0
        for f in e.get('fig') or []:
            d.rectangle([f[0] * W * k2, f[1] * H * k2, f[2] * W * k2, f[3] * H * k2], outline=(220, 30, 30), width=3)
        tw = 560
        canvas = Image.new('RGB', (im.width + tw + 30, max(im.height, 200)), 'white')
        canvas.paste(im, (0, 0))
        dd = ImageDraw.Draw(canvas)
        x0 = im.width + 15
        y = 12
        dd.text((x0, y), '%s · %s · 쪽 %d · src %s · 그림 %d' % (k, r[F['CODE']], p, e.get('src'), len(e.get('fig') or [])), fill=(30, 60, 160), font=font)
        y += 30
        line = ''
        for ch in str(e.get('t') or ''):
            if dd.textlength(line + ch, font=font) > tw:
                dd.text((x0, y), line, fill=(0, 0, 0), font=font)
                y += 24
                line = ch
                if y > canvas.height - 30:
                    break
            else:
                line += ch
        if line and y <= canvas.height - 30:
            dd.text((x0, y), line, fill=(0, 0, 0), font=font)
        fn = '%02d_%s_%s_p%03d.png' % (n, k, r[F['CODE']], p)
        canvas.save(os.path.join(CHECK, fn))
        made.append(fn)
    T(G, '표본 20(장마다 고르게 · 시드 20261001) 발문 글 · 그림 자리(빨간 상자) ↔ 원본 쪽 그림 — %s' % CHECK, len(made) == 20, {'파일': made})
    N(G, '표본 — 사용자·채팅 눈 검수', '글이 쪽 발문과 같은가 · 그림 상자가 발문 그림을 감싸는가 · 〈보기〉·선택지·머리 줄이 안 섞였나')
    return len(made) == 20


# ── B3 · B4 · B6 앱 ───────────────────────────────────────────────────────────────────────────
PVREADY = "() => typeof PV !== 'undefined' && !!PV && Object.keys(PV).length > 0"
ROWS = r"""(sel) => [...document.querySelectorAll(sel)].map(it => {
  const gc = it.querySelector('[data-ggcnt]');   /* 바탕(physprev 앞) 첫 화면 줄은 data-pv 가 없다 — 근거 칩의 data-ggcnt = GGU(r) 로 잇는다 */
  const pv = it.dataset.pv || (it.dataset.no ? 'P' + String(it.dataset.no).padStart(3, '0') : '') || (gc ? gc.dataset.ggcnt : '');
  const t = it.querySelector('.prev, .q'), fg = it.querySelector('.pvfig'), R = e => e.getBoundingClientRect();
  const cs = t ? getComputedStyle(t) : null, imgs = fg ? [...fg.querySelectorAll('img')] : [];
  return {k: pv, txt: t ? t.textContent : null, pvc: t ? t.classList.contains('pv') : false,
    clamp: cs ? (cs.webkitLineClamp || cs.getPropertyValue('-webkit-line-clamp') || 'none') : null,
    cut: t ? t.scrollHeight > t.clientHeight + 1 : null, fig: !!fg, drawn: fg ? !!fg.dataset.pvd : false,
    imgs: imgs.map(i => ({h: Math.round(R(i).height * 10) / 10, w: Math.round(R(i).width * 10) / 10})), rw: Math.round(R(it).width),
    over: it.scrollWidth > it.clientWidth + 1, top: Math.round(R(it).top), bot: Math.round(R(it).bottom)}; })"""


def ws(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def check_rows(rows, PV, DATA, vh):
    """한 화면 줄들 — 틀린 것 셈"""
    byk = {uid(r): r for r in DATA}
    bad = {'빈 줄': [], '글 ≠ t': [], '잘림': [], '〈보기〉·선택지': [], '그림 높이 > 44': [], '그림 폭 > 60%': [], '그림 없는데 칸': [], '그림 칸 없음': [], '가로 넘침': []}
    n = drawn_vis = 0
    for x in rows:
        e = PV.get(x['k'])
        if not e:
            continue
        n += 1
        if e.get('src') != 'none':
            if not ws(x['txt']):
                bad['빈 줄'].append(x['k'])
            if ws(x['txt']) != ws(e.get('t')):
                bad['글 ≠ t'].append(x['k'])
            if x['cut'] or (x['clamp'] not in ('none', '', None) and x['pvc']):
                bad['잘림'].append(x['k'])
            if leak(x['txt'] or ''):
                bad['〈보기〉·선택지'].append(x['k'])
        hasfig = e.get('fig') == 'img' or bool(e.get('fig'))
        if x['fig'] and not hasfig:
            bad['그림 없는데 칸'].append(x['k'])
        for i in x['imgs']:
            if i['h'] > 44:
                bad['그림 높이 > 44'].append(x['k'])
        if x['imgs'] and sum(i['w'] for i in x['imgs']) > 0.6 * x['rw'] + 8:
            bad['그림 폭 > 60%'].append(x['k'])
        if x['over']:
            bad['가로 넘침'].append(x['k'])
        if x['drawn'] and x['imgs'] and x['top'] < vh:
            drawn_vis += 1
    return n, {k: v for k, v in bad.items() if v}, drawn_vis


def lazy_state(p):
    return p.ev(r"""() => { const vh = innerHeight, out = {below_drawn: 0, below: 0, vis: 0, vis_drawn: 0};
      document.querySelectorAll('#list .item .pvfig').forEach(f => { const r = f.getBoundingClientRect();
        if (r.top >= vh) { out.below++; if (f.dataset.pvd) out.below_drawn++; } else if (r.bottom > 0) { out.vis++; if (f.dataset.pvd) out.vis_drawn++; } });
      return out; }""")


def scroll_all(p, sel_box):
    """그 상자를 끝까지 내려가며(화면 하나씩) 그림이 그려지게"""
    p.ev(r"""async (sel) => { const se = sel ? document.querySelector(sel) : document.scrollingElement; if (!se) return;
      for (let y = 0; y <= se.scrollHeight; y += Math.max(200, (sel ? se.clientHeight : innerHeight) - 60)) { se.scrollTop = y; await new Promise(r => setTimeout(r, 160)); }
      await new Promise(r => setTimeout(r, 600)); se.scrollTop = 0; }""", sel_box)
    p.wait(800)


FD_JS = """(()=>{window.__fd=null;window.__pv=null;const mo=new MutationObserver(()=>{if(window.__fd===null&&document.querySelector('#list .item'))window.__fd=performance.now();
      if(window.__pv===null&&document.querySelector('#list .item .prev.pv'))window.__pv=performance.now();if(window.__fd!==null&&window.__pv!==null)mo.disconnect()});
      document.addEventListener('DOMContentLoaded',()=>{if(window.__fd===null&&document.querySelector('#list .item'))window.__fd=performance.now();const l=document.getElementById('list');if(l)mo.observe(l,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['class']})})})();"""


def first_draw_ms(br, src, base_src, n=5):
    """PC 첫 화면 처음 그리기 — 새 판·바탕 문맥을 하나씩 열어 시험지를 받아 둔 뒤 번갈아 다시 열기 n 번씩
       · 첫 .item 이 #list 에 든 performance.now()(fd) · 새 판은 첫 .prev.pv(미리보기 갈아 끼움)도(pv)"""
    pn = JG.fresh(br, 'b3t_new', src, 'phys', JG.PC, remote=Rem())
    pb = JG.fresh(br, 'b3t_base', base_src, 'phys', JG.PC, remote=Rem())
    tn, tb, tv = [], [], []
    try:
        for p in (pn, pb):
            p.ctx.add_init_script(FD_JS)
        for i in range(n):
            for p, out in ((pn, tn), (pb, tb)):
                p.pg.reload(wait_until='load')
                p.pg.wait_for_function("() => window.__fd !== null && window.__fd !== undefined", timeout=90000)
                p.wait(1500)
                out.append(round(p.ev("() => window.__fd"), 1))
                if p is pn:
                    v = p.ev("() => window.__pv")
                    tv.append(round(v, 1) if v is not None else None)
    finally:
        pn.close()
        pb.close()
    return tn, tb, tv


def b3(br, eng, PV, DATA, src, base_src):
    G = 'B3'
    ok = True
    for dn, dev in ((('폰390', JG.PHONE), ('iPad820', JG.PAD), ('PC1440', JG.PC)) if not QC.SMOKE else (('폰390', JG.PHONE),)):   # smoke — 폰 390 하나
        if eng == 'webkit' and dev == JG.PC:
            continue
        for who, s in ((('NEW', src), ('BASE', base_src)) if QC.GATE else (('NEW', src),)):   # regress — 바탕(B3-헛 재료) 띄움 0
            QC.launch('new' if who == 'NEW' else 'base')
            p = JG.fresh(br, '%s_b3_%s_%s' % (eng, dn, who), s, 'phys', dev, eng=eng, remote=Rem())
            try:
                if who == 'NEW':
                    try:
                        p.pg.wait_for_function(PVREADY, timeout=30000)
                    except Exception:
                        pass
                p.wait(900)
                vh = p.ev("() => innerHeight")
                if who == 'NEW':   # 화면 안 그림이 하나라도 그려질 때까지(시험지 PDF 첫 읽기가 몇 초 걸린다 · 20초까지) — 그 뒤에 화면 밖 그림 수를 잰다
                    try:
                        p.pg.wait_for_function("""() => { const vh = innerHeight; const f = [...document.querySelectorAll('#list .item .pvfig')].filter(x => { const r = x.getBoundingClientRect(); return r.bottom > 0 && r.top < vh; });
                          return !f.length || f.some(x => x.dataset.pvd); }""", timeout=20000)
                    except Exception:
                        pass
                    p.wait(600)
                lz = lazy_state(p)
                rows0 = p.ev(ROWS, '#list .item')
                scroll_all(p, None)
                rows = p.ev(ROWS, '#list .item')
                n, bad, dv = check_rows(rows, PV, DATA, vh)
                p.ev("() => jnOpen('1.1')")
                p.wait(900) if QC.GATE else _rg_wait(p, 900, _RG_JNW, 'B3.jnw')
                jrows0 = p.ev(ROWS, '#jnw .jnrow')
                scroll_all(p, '#jnw .panel')
                jrows = p.ev(ROWS, '#jnw .jnrow')
                jn, jbad, jdv = check_rows(jrows, PV, DATA, vh)
                errs = p.errs[:] + (p.ev("() => __H.errs()") or [])
            finally:
                p.close()
            good = n > 0 and not bad and jn > 0 and not jbad and not errs
            figs = sum(1 for x in rows if x['fig'])
            if who == 'NEW':
                lazy_ok = lz['below_drawn'] == 0 and (lz['vis'] == 0 or lz['vis_drawn'] > 0)
                ok = ok and good and lazy_ok
                T(G, '%s %s 첫 화면 · 📋 1.1 — 빈 줄 0 · 글 = t 전부 · 잘림 0 · 〈보기〉·선택지 0 · 그림 ≤ 44 · ≤ 60%% · 그림 없는 문항 칸 0 · 넘침 0' % (eng, dn), good,
                  {'첫 화면 줄': n, '틀림': bad, '📋 줄': jn, '📋 틀림': jbad, '그림 칸': figs, '그려진 그림(화면 안)': dv, '오류': errs[:3]})
                if QC.want('B3.lazy'):   # smoke 칸 아님
                    T(G, '%s %s 그림은 보일 때만 — 처음 화면 밖 그림 0 · 화면 안 그림은 그려짐' % (eng, dn), lazy_ok, lz)
            else:
                nb = len(bad.get('글 ≠ t', []))
                T(G + '-헛', '%s %s 바탕 = 미리보기 없음(헛잣대 — 표본 줄 있음 · 글 ≠ t 인 줄 있음 · 그림 칸 0)' % (eng, dn), n > 0 and nb > 0 and figs == 0,
                  {'첫 화면 줄': n, '글 ≠ t': nb, '틀림 수': {k: len(v) for k, v in bad.items()}, '그림 칸': figs, '📋 줄': jn})
    return ok


def b3t(br, src, base_src):
    G = 'B3'
    if QC.GATE:
        QC.launch('new'); QC.launch('base')
        tn, tb, tv = first_draw_ms(br, src, base_src)
        mn, mb = statistics.median(tn[1:]), statistics.median(tb[1:])
    else:   # regress — 새 판 문맥만(다시 열기 다섯 번 · 첫 번 데움 뺌) · 바탕 가운데 값 = 기준 스냅샷(앞 인도판 같은 칸의 새 판 가운데 값 · 다른 때 잰 값 — 결정 거리)
        tn, tv = _rg_first_draw_ms(br, src)
        mn = statistics.median(tn[1:])
        mb = QC.base('B3.first/mn', mn)
        tb = ['기준 스냅샷 %s · %s' % (mb, QC.base_note('B3.first/mn'))]
    ok = 0.8 * mb <= mn <= 1.2 * mb
    T(G, 'PC 첫 화면 처음 그리기 시간 = 바탕 ±20%(번갈아 다시 열기 다섯 번씩 · 첫 번 데움 빼고 넷의 가운데 값)', ok,
      {'새 판 ms': tn, '바탕 ms': tb, '비': round(mn / mb, 3) if mb else None})
    N(G, '새 판 미리보기 갈아 끼운 때(첫 .prev.pv · ms)', {'pv': tv, '처음 그리기 뒤(가운데)': round(statistics.median([v - f for v, f in zip(tv[1:], tn[1:]) if v is not None]), 1) if any(v is not None for v in tv[1:]) else None})
    return ok


def pick_words(PV, DATA):
    """ABBYY 에만 있는 말 — 쪽 16 「자동차의 속력」 + BODY 가 빈 문항 t 에서 BODY 전부에 없는 8~12자 조각 둘(열쇠 차례 첫 것)"""
    allbody = '\n'.join(str(r[F['BODY']]) for r in DATA)
    out = [('자동차의 속력', 'P007')]
    for r in DATA:
        k = uid(r)
        e = PV.get(k) or {}
        if k == 'P007' or str(r[F['BODY']]).strip() or e.get('src') != 'abbyy':
            continue
        t = str(e.get('t') or '')
        m = re.search(r'[가-힣]{2,5} [가-힣]{2,6}', t[10:])
        if not m:
            continue
        w = m.group(0)
        if w in allbody or sum(1 for v in PV.values() if w in str(v.get('t') or '')) != 1:
            continue
        out.append((w, k))
        if len(out) == 3:
            break
    return out


def b4(br, eng, PV, DATA, src, base_src):
    G = 'B4'
    words = pick_words(PV, DATA)
    ok = True
    res = {}
    for who, s in ((('NEW', src), ('BASE', base_src)) if QC.GATE else (('NEW', src),)):   # regress — 「바탕은 그 문항 없음」(헛잣대) 몫 띄움 0 · 판정의 바탕 조건은 빈 값이라 NEW 조건만 남는다
        QC.launch('new' if who == 'NEW' else 'base')
        p = JG.fresh(br, '%s_b4_%s' % (eng, who), s, 'phys', JG.PC, eng=eng, remote=Rem())
        try:
            if who == 'NEW':
                try:
                    p.pg.wait_for_function(PVREADY, timeout=30000)
                except Exception:
                    pass
            for w, k in words:
                no = int(k[1:])
                r = p.ev("""([w, no]) => { const q = document.getElementById('q'); if (typeof GGMODE !== 'undefined' && GGMODE !== 'q') try { ggSearchMode('q') } catch (e) {}
                  q.value = w; esSearch(); const box = document.getElementById('esres');
                  const row = box ? box.querySelector('[data-esq="' + no + '"]') : null;
                  return {n: (typeof ES_NOS !== 'undefined') ? ES_NOS.length : -1, hit: (typeof ES_NOS !== 'undefined') && ES_NOS.indexOf(no) >= 0,
                          mark: row ? row.querySelectorAll('mark').length : 0, snip: row ? (row.querySelector('.qq') || {}).textContent || '' : ''}; }""", [w, no])
                res.setdefault(w, {})[who] = r
        finally:
            p.close()
    for w, k in words:
        n_, b_ = res[w].get('NEW') or {}, res[w].get('BASE') or {}
        good = bool(n_.get('hit')) and n_.get('mark', 0) >= 1 and not b_.get('hit')
        ok = ok and good
        T(G, '%s 「%s」 → 물리 검색 결과에 %s(조각 mark) · 바탕은 그 문항 없음(헛잣대)' % (eng, w, k), good,
          {'새 판': {x: n_.get(x) for x in ('n', 'hit', 'mark')}, '조각': (n_.get('snip') or '')[:80], '바탕': {x: b_.get(x) for x in ('n', 'hit')}})
    return ok


def b6(br, eng, src, base_src):
    G = 'B6'
    ok = True
    for dn, dev in (('폰390', JG.PHONE), ('iPad820', JG.PAD), ('PC1440', JG.PC)):
        got = {}
        for who, s in ((('NEW', src), ('BASE', base_src)) if QC.GATE else (('NEW', src),)):   # regress — 바탕 훑기 대신 기준 스냅샷(아래)
            QC.launch('new' if who == 'NEW' else 'base')
            p = JG.fresh(br, '%s_b6_%s_%s' % (eng, dn, who), s, 'phys', dev, eng=eng, remote=Rem())
            try:
                if who == 'NEW':
                    try:
                        p.pg.wait_for_function(PVREADY, timeout=30000)
                    except Exception:
                        pass
                p.wait(1200)
                touch = dev != JG.PC
                sw = lambda sel: p.ev("a => __H.sweep(a[0], a[1])", [sel, touch])
                o = {'첫 화면 목록': sw('#list')}
                if QC.GATE:   # 📋 정리 창 훑기 = 합침→physphone B7(같은 __H.sweep #jnw · 같은 기기 셋) — regress 끔
                    p.ev("() => jnOpen('1.1')")
                    p.wait(1200)
                    o['📋 정리 창'] = sw('#jnw')
                got[who] = (o, p.errs[:])
            finally:
                p.close()
        if QC.REGRESS:   # regress — 「새로 생긴 흠」 = 새 판 훑기 − 기준 스냅샷(앞 인도판 같은 칸 훑기)
            got['BASE'] = ({scr: QC.base(_rg_cid('B6', eng, dn, scr), sorted(set(v))) for scr, v in got['NEW'][0].items()}, [])
        for scr in got['NEW'][0]:
            nn = sorted(set(got['NEW'][0][scr]) - set(got['BASE'][0].get(scr, [])))
            gone = sorted(set(got['BASE'][0].get(scr, [])) - set(got['NEW'][0][scr]))
            good = not nn
            ok = ok and good
            T(G, '%s %s %s 새로 생긴 흠 0' % (eng, dn, scr), good, {'새로': nn[:8], '없어짐': gone[:6], '남은(바탕에도)': len(set(got['NEW'][0][scr]) & set(got['BASE'][0].get(scr, [])))})
        if got['NEW'][1]:
            ok = False
            T(G, '%s %s JS 오류' % (eng, dn), False, got['NEW'][1][:3])
    return ok


def b5(PV, src, base_src):
    G = 'B5'
    long_t = [str(v.get('t')) for v in PV.values() if len(str(v.get('t') or '')) >= 12]
    if QC.REGRESS:   # regress — 「바탕 앱에 이미 있던 글」 = 기준 스냅샷(앞 인도판 앱에 든 t 의 md5 목록 · 글은 안 남김) · 바탕(d3762af) 안 풂
        import hashlib
        _h = lambda t: hashlib.md5(t.encode('utf-8')).hexdigest()
        _bs = set(QC.base('B5.inapp', sorted(_h(t) for t in long_t if t in src)))
        base_src = ''.join('\n' + t for t in long_t if _h(t) in _bs)   # 판정 줄 · 값 줄이 읽는 「바탕에 있던 글」 꼴(아래 줄 무변)
    inapp = [t[:30] for t in long_t if t in src and t not in base_src]   # 바탕 앱에 이미 있던 글(옛 BODY = 옛 PDF 글자층)은 이 판이 넣은 것이 아니다
    T(G, '이 판이 앱에 넣은 미리보기 글(t ≥ 12자 · 바탕 앱에 없던 것) 0 — 미리보기 재료는 studyplandata(비공개)에만', not inapp,
      {'t 수': len(long_t), '이 판이 넣은 것': inapp[:3], '바탕에도 있던 것(옛 BODY)': sum(1 for t in long_t if t in base_src)})
    ok = not inapp
    scan = os.path.join(NR, '_d11_scan.py') if NR else None
    if not QC.GATE:   # regress — _d11_scan(하위 파이썬)은 g_push 가 push 마다 스테이징 뒤 잰다(CLAUDE.md 5 ⓓ) · 관문만
        return ok
    if scan and os.path.isfile(scan) and os.path.isfile(NEWF):
        QC.sub('python:scan')
        r = subprocess.run([sys.executable, scan, NEWF], capture_output=True, text=True, encoding='utf-8', errors='replace')
        good = r.returncode == 0
        ok = ok and good
        T(G, '앱 파일 _d11_scan 걸림 0(메일 · 휴대전화 · 토큰 꼴 · 워터마크 — 값은 안 찍음)', good, {'rc': r.returncode, '끝줄': (r.stdout.strip().splitlines() or [''])[-1][:160]})
    else:
        N(G, '_d11_scan', 'N: 필요(또는 --new 가 git 판) — 건넘')
    return ok


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    if QC.GATE:
        QC.sub('git:show-app')
        src, base_src = src_of(NEWF), src_of(BASEF)
    else:   # regress — 바탕(d3762af) 앱 풀기 0
        src, base_src = src_of(NEWF), None
    DATA = data_of(src)
    if not os.path.isfile(PREVF):
        raise SystemExit('미리보기.json 없음: %s' % PREVF)
    PV = json.load(open(PREVF, encoding='utf-8'))
    print('관문 _task_jagwa_physprev · 앱 = %s · 바탕 = %s · 미리보기 = %s(%d칸)' % (NEWF, BASEF, PREVF, len(PV)), flush=True)
    got, tm = {}, {}

    def step(g, fn):
        t1 = time.time()
        print('── %s' % g, flush=True)
        try:
            got[g] = bool(fn())
        except Exception as e:
            got[g] = False
            T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300] if str(e) else repr(e))
        tm[g] = tm.get(g, 0) + time.time() - t1
        print('   (%s %.0f초)' % (g, time.time() - t1), flush=True)

    if want('B1') and not QC.SMOKE:   # smoke — 데이터 칸 건넘
        step('B1', lambda: b1(PV, DATA))
    if want('B2') and QC.GATE:   # B2 표본 PNG(원본 PDF 렌더 · 눈 검수) = 관문만
        step('B2', lambda: b2(PV, DATA))
    if want('B5') and not QC.SMOKE:
        step('B5', lambda: b5(PV, src, base_src))
    with sync_playwright() as pw:
        for eng in (ENGS if not QC.SMOKE else [e for e in ENGS if e == 'chromium'][:1]):   # smoke — chromium 한 판
            try:
                br = getattr(pw, eng).launch()
            except Exception as e:
                N('WK', '%s 안 잼' % eng, str(e).splitlines()[0][:160])
                continue
            try:
                if want('B3'):
                    step('B3', lambda: b3(br, eng, PV, DATA, src, base_src))
                    if eng == 'chromium' and not QC.SMOKE:
                        step('B3', lambda: b3t(br, src, base_src))
                if want('B4') and not QC.SMOKE:
                    step('B4', lambda: b4(br, eng, PV, DATA, src, base_src))
                if want('B6') and eng == 'chromium' and not QC.SMOKE:
                    step('B6', lambda: b6(br, eng, src, base_src))
            finally:
                br.close()
    lines = []
    print('\n══ 요약 (%.0f초)' % (time.time() - t0))
    for g in [x for x in ('B1', 'B2', 'B3', 'B4', 'B5', 'B6') if x in got]:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        s = '  %-3s %s (%d 칸 중 FAIL %d · %.0f초)' % (g, 'PASS' if got[g] else 'FAIL', len(cells), nf, tm.get(g, 0))
        print(s)
        lines.append(s)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        f.write('==== %s · physprev · 앱 %s · 바탕 %s · 미리보기 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(str(NEWF)), BASEF, os.path.basename(PREVF), ','.join(ENGS)))
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
