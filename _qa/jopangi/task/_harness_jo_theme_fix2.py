# -*- coding: utf-8 -*-
r"""_task_jo_theme_fix2 §C-1 관문(로컬 · 새 데이터) — 합친 앱(§B 클라우드) + minbeoppdf 새 테마 재료(§A)

  python _harness_jo_theme_fix2.py [--new <앱>] [--base <앱 | genie git 판 = eacc28e>] [--old-theme <minbeoppdf 판 = e9e7e8e3>] [--res <결과>] [--shots <폴더>] [--eng chromium,webkit]

  재료 = 덧판 「새」: MBPDF_ROOT 의 theme/patent_hr8(테마.json.gz + img/) 그대로 링크(읽기만) · 그 밖은 _harness_jo_theme 의 full 덧판(합성 8판 · 빈 pdf)
         덧판 「옛」(헛잣대 재료): minbeoppdf git <--old-theme> 의 테마.json.gz(테마 70 · 그림 0 · 거리 묶음)
  관문(새 앱 + 새 재료 = PASS 여야) — 헛잣대 줄: 옛 재료 + 새 앱(재료 칸) · 새 재료 + 바탕 앱(그림 칸) 에서 그 칸이 FAIL 이면 PASS(안 물면 INFO 「헛잣대 안 삶」)
   C1 서랍 「테마 N」 = 재료 테마 수(95)
   C2 테마 줄 이름 — t03 {주체능력} · t06 {기일기간} · t71 {분변분재 기간}
   C3 {분변분재 기간}(t71) 창 = .thfig SVG 하나 · text · path 수 = 재료 · 창 폭 맞춤 · 화면 밖 0(PC · 폰 390)
   C4 구역 SVG 글 속 조 링크(.wmlk) 누름 → 조문 팝업(jo|<법>|<조>) — t71 실제 글엔 조 꼴이 없어 링크 든 첫 구역 테마로
   C5 {기일기간}(t06) 창 글에 「[분할출원]」 0
   C6 {권범심·자유실시기술 항변}(t72) 창 = 구역 SVG — 펜 획(path) ≥ 2 + 표 그림(image) 뜸
   C7 {침해형사조치}(t52) 창 = 박스 글 줄(.thl) ≥ 1 + 벌칙 표 그림 뜸
   C8 {청구범위해석}(t29) 창에 「국제예비심사」 0
   C9 거름 점 「기간」(초록) — 「테마 N」 · 테마 줄 = 재료 bk[2](39)
   C10 구역 SVG 테마 전부(PC) · 그림 든 테마(폰) — 그림 다 뜸(blob · Image.decode) · 그림 자리 화소가 비지 않음 · 형광펜 섞기(mix-blend-mode multiply) 수 = 재료 · 창 폭 · 화면 밖 0
       (WebKit 은 iPad 834 로 그림 뜸 · 풀림 · 폭 — blob: 은 route 에서 풀어 줌)
   C11 그림 확인(규칙 60 · 게이트 아님) — --shots <폴더> 를 주면 t72 · t74 · t73 · t52 · t37 · t71 창 그림(PC) + 원본 쪽(주석1 PDF · 빨간 테 = 구역) 나란히
       → <폴더>\_shot_theme_fix2_<id>_합침.png
  도구 = 같은 폴더 _harness_jo_theme(덧판 · 서버 · __TM · 가짜 원격) → _harness_jo_revfix0929b(SEED · __RB · 기기 · 결과 줄)
  D11 — 이 파일에 정리omr 글 0(테마 id · 지시서가 적은 이름·낱말만) · 실제 글은 돌 때 재료에서 읽기만 · 그림은 --shots 자리(N:)에만
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import gzip, hashlib, io, json, os, re, shutil, subprocess, sys, time   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('jo', 'index.html'))
BASE = ARG('--base', 'eacc28e')          # fix2 바탕(main · 구역 SVG 의 image 를 지우는 소독기)
OLDT = ARG('--old-theme', 'e9e7e8e3')    # 헛잣대 재료 — minbeoppdf §A 착수 바탕(테마 70 · 그림 0 · 거리 묶음)
OUTF = ARG('--res', os.path.join(HERE, '_harness_jo_theme_fix2_result.txt'))
SHOTS = ARG('--shots')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
MBREAL = ARG('--mbpdf', _roots.mbpdf())
_argv = sys.argv
sys.argv = [sys.argv[0], '--new', NEW, '--mbpdf', MBREAL]
sys.path.insert(0, HERE)
import _harness_jo_theme as TH   # noqa: E402 — 가져올 때 덧판 full · none 을 짓는다(끝에 TH.TMP 를 지움)
sys.argv = _argv
H = TH.H
T, N, RES = H.T, H.N, H.RES
PC2, PHONE, PAD = H.PC2, H.PHONE, H.PAD
NAMES = {'t03': '{주체능력}', 't06': '{기일기간}', 't71': '{분변분재 기간}'}
NO_TXT = {'t06': '[분할출원]', 't29': '국제예비심사'}
SHOT_IDS = ['t72', 't74', 't73', 't52', 't37', 't71']
BK_KIGAN = '#059669'
OVERS = {}


# ════════════════════════ 재료 · 덧판 ════════════════════════
def load(raw):
    D = json.loads(gzip.decompress(raw).decode('utf-8'))

    def svg_of(t):
        return [D['boxes'][b]['svg'] for b in t.get('boxes') or [] if (D['boxes'].get(b) or {}).get('svg')]
    want = {'n': len(D['themes']), 'names': {t['id']: t['n'] for t in D['themes']}, 'kigan': sorted(t['id'] for t in D['themes'] if t.get('bk') and t['bk'][2]),
            'svg_ids': [t['id'] for t in D['themes'] if svg_of(t)],
            'img': {t['id']: sum(s.count('<image') for s in svg_of(t)) for t in D['themes'] if svg_of(t)},
            'blend': sum(s.count('mix-blend-mode') for t in D['themes'] for s in svg_of(t)),
            'svgcnt': {t['id']: [sum(len(re.findall(r'<text\b', s)) for s in svg_of(t)), sum(len(re.findall(r'<path\b', s)) for s in svg_of(t))] for t in D['themes'] if svg_of(t)},
            'region': {t['id']: t.get('region') for t in D['themes']}}
    want['img_ids'] = [k for k, v in want['img'].items() if v]
    return D, want


def overlay(name, raw=None):
    """raw 없음 = 새 재료(클론 theme/patent_hr8 폴더째 링크 · img/ 포함) · raw = 그 테마.json.gz 바이트만"""
    d = os.path.join(TH.TMP, 'mbp_c1' + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'theme'))
    for x in os.listdir(TH.OVER['full']):
        if x != 'theme':
            TH._ln(os.path.join(TH.OVER['full'], x), os.path.join(d, x))
    if raw is None:
        TH._ln(os.path.join(MBREAL, 'theme', 'patent_hr8'), os.path.join(d, 'theme', 'patent_hr8'))
    else:
        os.makedirs(os.path.join(d, 'theme', 'patent_hr8'))
        open(os.path.join(d, 'theme', 'patent_hr8', '테마.json.gz'), 'wb').write(raw)
    OVERS[name] = d
    return d


def page(br, cfg, tag, src, dev):
    """cfg = 덧판 이름 — 서버는 tag 마다 처음 지을 때 TH.OVER['real'] 을 잡는다(그 앞에 갈아 끼움)"""
    TH.OVER['real'] = OVERS[cfg]
    p = TH.page(br, 'real:' + cfg + ':' + tag, src, dev)
    # Playwright WebKit 은 blob: 주소도 ctx.route 에 태운다 — 「127.0.0.1 밖 끊기」가 앱이 만든 그림 blob 을 Load failed 로 만든다(10/2 잼 · Chromium 은 안 태움)
    p.ctx.unroute_all()
    p.ctx.route(lambda u: not (u.startswith('http://127.0.0.1') or u.startswith('blob:') or u.startswith('data:')), lambda r: r.abort())
    TH.jo(p)
    p.ev("async () => { for (let i = 0; i < 300 && !(typeof TM === 'object' && TM.d && TM.d.themes && TM.d.themes.length); i++) await __TM.wait(50); }")
    return p


# ════════════════════════ 재기 ════════════════════════
DRAWER = r"""async () => { const tg = () => document.querySelector('.jtbar .tmtg'); if (!tg()) return null;
  const out = { tmtg: __TM.txt(tg()), dot: __TM.dot() };
  tg().click(); await __TM.wait(350);
  out.rows = __TM.rows().map(r => [r.id, r.t]);
  tg().click(); await __TM.wait(350);
  return out; }"""
WIN = r"""async (id) => { closeAllPops(true); if (!(TM.d && TM.d.themes || []).some(t => t.id === id)) return null; tmWin(id, null);
  const w = await __RB.until(() => __TM.pop('theme|' + id), 5000); if (!w) return null;
  const XL = 'http://www.w3.org/1999/xlink', href = n => n.getAttribute('href') || n.getAttributeNS(XL, 'href') || '';
  const imgs = () => [...w.querySelectorAll('.thfig image')];
  await __RB.until(() => imgs().every(n => /^(blob:|data:)/.test(href(n))), 8000);
  await __TM.wait(150);
  const R = e => { const q = e.getBoundingClientRect(); return [q.left, q.top, q.right, q.bottom].map(v => Math.round(v * 10) / 10); };
  const body = w.querySelector(':scope > .pb') || w;
  const figs = [...w.querySelectorAll('.thfig')].map(f => { const s = f.querySelector('svg');
    return { text: s ? s.querySelectorAll('text').length : 0, path: s ? s.querySelectorAll('path').length : 0,
      links: s ? [...s.querySelectorAll('.wmlk')].map(a => [a.textContent, a.dataset.law || '', a.dataset.k || '']) : [],
      img: imgs().filter(n => f.contains(n)).map(n => ({ p: n.getAttribute('data-tmimg') || '', h: href(n).slice(0, 5) })),
      blend: s ? [...s.querySelectorAll('*')].filter(n => getComputedStyle(n).mixBlendMode === 'multiply').length : 0,
      svg: s ? R(s) : null }; });
  const dec = [];
  for (const n of imgs()){ const h = href(n), pth = n.getAttribute('data-tmimg') || h.slice(0, 16);
    if (!/^(blob:|data:)/.test(h)){ dec.push([pth, 0, 0, '받지 못함']); continue; }
    try { const im = new Image(); im.src = h; await im.decode(); dec.push([pth, im.naturalWidth, im.naturalHeight, '']); } catch (e) { dec.push([pth, 0, 0, String(e).slice(0, 60)]); } }
  return { win: R(w), body: R(body), vw: innerWidth, vh: innerHeight, txt: __TM.txt(w), thl: w.querySelectorAll('.thl').length, figs, dec }; }"""
IMG_AT = r"""([id, i]) => { const w = __TM.pop('theme|' + id); const n = w ? [...w.querySelectorAll('.thfig image')][i] : null; if (!n) return null;
  n.scrollIntoView({ block: 'center', inline: 'nearest' }); const q = n.getBoundingClientRect(); return [q.left, q.top, q.width, q.height, innerWidth, innerHeight]; }"""


def ink(p, tid, i):
    """그림 자리 화소 — 흰 바탕(최소 채널 ≥ 225) 아닌 몫(0~1) · 그림이 없으면 None"""
    from PIL import Image
    r = p.ev(IMG_AT, [tid, i])
    if not r:
        return None
    p.wait(120)
    r = p.ev(IMG_AT, [tid, i])
    x0, y0, x1, y1 = max(0, r[0]), max(0, r[1]), min(r[4], r[0] + r[2]), min(r[5], r[1] + r[3])
    if x1 - x0 < 2 or y1 - y0 < 2:
        return 0.0
    im = Image.open(io.BytesIO(p.pg.screenshot(clip={'x': x0, 'y': y0, 'width': x1 - x0, 'height': y1 - y0}))).convert('RGB')
    px = list(im.getdata())
    return round(sum(1 for c in px if min(c) < 225) / max(1, len(px)), 4)


def fits(w):
    """창 폭 맞춤(그림 svg 가 창 몸통 안) · 화면 밖 0(뷰포트 가로 안)"""
    bad = []
    for f in w['figs']:
        s = f['svg']
        if not s:
            continue
        if s[0] < w['body'][0] - 1 or s[2] > w['body'][2] + 1:
            bad.append(['창 밖', s, w['body']])
        if s[0] < -0.5 or s[2] > w['vw'] + 0.5:
            bad.append(['화면 밖', s, w['vw']])
    return bad


def wsum(w):
    if not w:
        return None
    figs = []
    for f in w['figs']:
        g = {k: (v if k != 'links' else len(v)) for k, v in f.items() if k != 'img'}
        g['img'] = len(f['img'])
        g['blob'] = sum(1 for x in f['img'] if x['h'] in ('blob:', 'data:'))
        figs.append(g)
    return {'thl': w['thl'], 'figs': figs, 'dec 실패': [d for d in w['dec'] if not d[1]], '창': w['win'], 'vw': w['vw']}


def measure(br, cfg, src, want, tag, full=True):
    """한 짝(덧판 · 앱)에서 C1~C10 재료를 잰다 — full=False 면 그림 칸(C6 · C7 · C10)만"""
    M = {'errs': []}
    p = page(br, cfg, tag + 'pc', src, PC2)
    M['ntm'] = p.ev("() => (TM.d && TM.d.themes || []).length")
    if full:
        M['drawer'] = p.ev(DRAWER)
        for _ in range(3):
            p.press(TH.at(p, '.jtbar .tmdot'), 450)
        M['kigan'] = p.ev(DRAWER)
        p.press(TH.at(p, '.jtbar .tmdot'), 450)
        M['t71'] = p.ev(WIN, 't71')
        for tid in ('t06', 't29'):
            M[tid] = p.ev(WIN, tid)
    for tid in ('t72', 't52'):
        M[tid] = p.ev(WIN, tid)
    M['pcwin'] = {}
    M['ink'] = {}
    for tid in want['svg_ids']:
        w = p.ev(WIN, tid)
        M['pcwin'][tid] = w
        if w and tid in want['img_ids']:
            n = sum(len(f['img']) for f in w['figs'])
            M['ink'][tid] = [ink(p, tid, i) for i in range(n)]
    if full:   # C4 — 구역 SVG 글 속 조 링크 → 조문 팝업 · t71 실제 글엔 조 꼴이 없다(10/2 잼 · 지시서 「52조」 는 합성 시험 재료 글) → 링크가 있는 첫 구역 테마로 잰다
        has = [t for t in want['svg_ids'] if (M['pcwin'].get(t) or {}).get('figs') and sum(len(f['links']) for f in M['pcwin'][t]['figs'])]
        lk = {'t71 링크': sum(len(f['links']) for f in (M['t71'] or {}).get('figs', [])) if M['t71'] else None, '링크 든 구역 테마': len(has), '표본': has[0] if has else None}
        if has:
            tid = has[0]
            p.ev(WIN, tid)
            a = p.ev("id => { const e = __TM.pop('theme|' + id).querySelector('.thfig .wmlk'); e.scrollIntoView({block: 'center'}); return __RB.hitOn(e); }", tid)
            d = p.ev("id => { const e = __TM.pop('theme|' + id).querySelector('.thfig .wmlk'); return [e.textContent, e.dataset.law || TM_LAW, e.dataset.k]; }", tid)
            lk['링크'] = d
            p.press(a, 700)
            lk['pop'] = p.ev("key => !!POPS.find(x => x._pk === key)", 'jo|%s|%s' % (d[1], d[2]))
            lk['pops'] = p.ev("() => POPS.map(x => x._pk).slice(-3)")
        M['link'] = lk
    M['errs'] += p.errs[:3]
    p.close()
    q = page(br, cfg, tag + 'ph', src, PHONE)
    M['phwin'] = {tid: q.ev(WIN, tid) for tid in ['t71'] + want['img_ids']}
    M['errs'] += q.errs[:3]
    q.close()
    return M


# ════════════════════════ 판정 ════════════════════════
def judge(M, want):
    """칸마다 (참 · 잰 값) — 새 짝에선 관문 · 헛잣대 짝에선 FAIL 이어야 물린 것"""
    J = {}
    d = M.get('drawer') or {}
    J['C1'] = (d.get('tmtg') == '테마 %d' % want['n'] and want['n'] == 95 and len(d.get('rows') or []) == want['n'], {'머리': d.get('tmtg'), '테마 줄': len(d.get('rows') or []), '재료': want['n']})
    rows = dict(d.get('rows') or [])
    J['C2'] = (all(rows.get(k) == v for k, v in NAMES.items()), {k: rows.get(k) for k in NAMES})
    t71 = M.get('t71')
    want71 = want['svgcnt'].get('t71')
    if t71 and len(t71['figs']) == 1 and want71:
        f = t71['figs'][0]
        ph = (M.get('phwin') or {}).get('t71')
        bad = fits(t71) + (fits(ph) if ph else [['폰 창 없음']])
        J['C3'] = ([f['text'], f['path']] == want71 and not bad, {'text·path': [f['text'], f['path']], '재료': want71, '지시서 text': 25, '폭·화면 밖': bad, 'PC': wsum(t71), '폰': wsum(ph)})
    else:
        J['C3'] = (False, {'창': wsum(t71), '재료 t71': want71})
    lk = M.get('link')
    J['C4'] = (bool(lk and lk.get('표본') and lk.get('pop')), lk)
    for c, tid in (('C5', 't06'), ('C8', 't29')):
        w = M.get(tid)
        J[c] = (bool(w) and NO_TXT[tid] not in w['txt'] and bool(w['thl'] > 0 or w['figs']), {'창': bool(w), '글에 있음': (NO_TXT[tid] in w['txt']) if w else None, '줄': w['thl'] if w else None})
    w72 = M.get('t72')
    if w72:
        im = [x for f in w72['figs'] for x in f['img']]
        g = len(w72['figs']) >= 1 and sum(f['path'] for f in w72['figs']) >= 2 and im and all(x['h'] == 'blob:' for x in im) and not [x for x in w72['dec'] if not x[1]]
        J['C6'] = (bool(g), {'path': sum(f['path'] for f in w72['figs']), '그림': len(im), 'blob': sum(1 for x in im if x['h'] == 'blob:'), '풀림': w72['dec']})
    else:
        J['C6'] = (False, {'창': None})
    w52 = M.get('t52')
    if w52:
        im = [x for f in w52['figs'] for x in f['img']]
        g = w52['thl'] >= 1 and im and all(x['h'] == 'blob:' for x in im) and not [x for x in w52['dec'] if not x[1]]
        J['C7'] = (bool(g), {'박스 글 줄': w52['thl'], '그림': len(im), 'blob': sum(1 for x in im if x['h'] == 'blob:'), '풀림': w52['dec']})
    else:
        J['C7'] = (False, {'창': None})
    k = M.get('kigan') or {}
    kr = [r[0] for r in (k.get('rows') or [])]
    J['C9'] = ((k.get('dot') or {}).get('bg') == BK_KIGAN and k.get('tmtg') == '테마 %d' % len(want['kigan']) and sorted(kr) == want['kigan'] and len(kr) == 39,
               {'점': (k.get('dot') or {}).get('bg'), '머리': k.get('tmtg'), '테마 줄': len(kr), '재료 bk[2]': len(want['kigan']), '다른 것': sorted(set(kr) ^ set(want['kigan']))[:8]})
    pw, inks = M.get('pcwin') or {}, M.get('ink') or {}
    imgs = [x for w in pw.values() if w for f in w['figs'] for x in f['img']]
    decbad = [x for w in pw.values() if w for x in w['dec'] if not x[1]]
    blend = sum(f['blend'] for w in pw.values() if w for f in w['figs'])
    fitbad = {tid: fits(w) for tid, w in pw.items() if w and fits(w)}
    fitbad.update({'폰 ' + tid: fits(w) for tid, w in (M.get('phwin') or {}).items() if w and tid in want['img_ids'] and fits(w)})
    phimg = [x for tid, w in (M.get('phwin') or {}).items() if w and tid in want['img_ids'] for f in w['figs'] for x in f['img']]
    blank = {tid: v for tid, v in inks.items() if not v or any((x is None or x < 0.005) for x in v)}
    nwant = sum(want['img'].values())
    vals = [x for v in inks.values() for x in v if x is not None]
    g10 = (len(imgs) == nwant and nwant == 34 and all(x['h'] == 'blob:' for x in imgs) and not decbad and blend == want['blend'] and not fitbad and not blank
           and len(phimg) == nwant and all(x['h'] == 'blob:' for x in phimg) and all(pw.get(t) for t in want['svg_ids']))
    J['C10'] = (bool(g10), {'구역 테마': '%d/%d' % (sum(1 for t in want['svg_ids'] if pw.get(t)), len(want['svg_ids'])), '그림': len(imgs), '재료 그림': nwant, 'blob': sum(1 for x in imgs if x['h'] == 'blob:'),
                            '풀림 실패': decbad[:4], '섞기': blend, '재료 섞기': want['blend'], '폭·화면 밖': fitbad, '빈 그림 자리(<0.5%)': blank, '화소 몫 최소': min(vals) if vals else None,
                            '폰 그림': len(phimg), '폰 blob': sum(1 for x in phimg if x['h'] == 'blob:')})
    return J


DESC = {'C1': '서랍 「테마 N」 = 재료 테마 수 95 · 테마 줄 95', 'C2': '테마 줄 이름 — t03 {주체능력} · t06 {기일기간} · t71 {분변분재 기간}',
        'C3': '{분변분재 기간}(t71) 창 = 구역 SVG 하나 · text·path = 재료(24 · 24 — 지시서 25 는 E 결과 「t71 text 24」 참고) · 창 폭 · 화면 밖 0(PC · 폰 390)',
        'C4': '구역 SVG 글 속 조 링크 누름 → 조문 팝업(jo|법|조) — t71 실제 글엔 조 꼴 0 이라 링크 든 첫 구역 테마로 잼', 'C5': '{기일기간}(t06) 창 글에 「[분할출원]」 0', 'C6': '{권범심·자유실시기술 항변}(t72) 창 = 펜 획 ≥ 2 + 표 그림 뜸(blob · 풀림)',
        'C7': '{침해형사조치}(t52) 창 = 박스 글 줄 ≥ 1 + 벌칙 표 그림 뜸', 'C8': '{청구범위해석}(t29) 창에 「국제예비심사」 0',
        'C9': '거름 점 기간(초록 #059669) — 「테마 39」 · 테마 줄 39 = 재료 bk[2]',
        'C10': '구역 SVG 테마 전부(PC) · 그림 든 테마(폰 390) — 그림 34 다 뜸(blob · Image.decode) · 그림 자리 화소 ≥ 0.5% · 형광펜 섞기 수 = 재료(17) · 창 폭 · 화면 밖 0'}
YARD_OF = {'C1': 'data', 'C2': 'data', 'C3': 'data', 'C4': 'data', 'C5': 'data', 'C8': 'data', 'C9': 'data', 'C6': 'app', 'C7': 'app', 'C10': 'app'}


# ════════════════════════ 그림 확인(C11 · 게이트 아님) ════════════════════════
def shots(br, src, want, out_dir):
    from PIL import Image, ImageDraw, ImageFont
    nroot = _roots.need_n('정리omr 주석1 PDF(그림 확인 · 원본 쪽)')
    pdf = os.path.join(nroot, 'jopangi', '정리omr', '26특허해례정리omr주석1.pdf')
    try:
        import fitz
        doc = fitz.open(pdf)
    except Exception as e:
        doc = None
        N('C11', '원본 쪽 못 엶', str(e)[:200])
    try:
        font = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 22)
        small = ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', 17)
    except Exception:
        font = small = ImageFont.load_default()
    p = page(br, 'new', 'shot', src, (1440, 1800))
    made = []
    for tid in SHOT_IDS:
        w = p.ev(WIN, tid)
        if not w:
            N('C11', '%s 창 없음' % tid)
            continue
        p.ev("id => { document.querySelectorAll('[data-shot]').forEach(x => x.removeAttribute('data-shot')); const w = __TM.pop('theme|' + id); w.setAttribute('data-shot', 'w'); const f = w.querySelector('.thfig'); if (f) f.setAttribute('data-shot', 'f'); const b = w.querySelector(':scope > .pb'); if (b) b.scrollTop = 0; }", tid)
        p.wait(300)
        panels = []
        rg = want['region'].get(tid)
        if doc and rg:
            pg = doc[rg['p'] - 1]
            W, Hh = pg.rect.width, pg.rect.height
            x0, y0, x1, y1 = rg['r'][0] * W, rg['r'][1] * Hh, rg['r'][2] * W, rg['r'][3] * Hh
            m = 0.03 * W
            clip = fitz.Rect(max(0, x0 - m), max(0, y0 - m), min(W, x1 + m), min(Hh, y1 + m))
            pix = pg.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip)
            im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
            dr = ImageDraw.Draw(im)
            dr.rectangle([(x0 - clip.x0) * 3, (y0 - clip.y0) * 3, (x1 - clip.x0) * 3, (y1 - clip.y0) * 3], outline=(220, 0, 0), width=4)
            panels.append(('원본 쪽(주석1 PDF %d쪽 · 빨간 테 = 구역)' % rg['p'], im))
        panels.append(('합친 앱 테마 창(PC 1440 · 연 그대로)', Image.open(io.BytesIO(p.pg.locator('[data-shot="w"]').screenshot())).convert('RGB')))
        if p.ev("() => !!document.querySelector('[data-shot=\"f\"]')"):
            panels.append(('창 안 구역 SVG 전체(.thfig · 그림 = 앱이 받은 webp)', Image.open(io.BytesIO(p.pg.locator('[data-shot="f"]').screenshot())).convert('RGB')))
        sc = [(lb, im if im.height <= 900 else im.resize((int(im.width * 900 / im.height), 900))) for lb, im in panels]
        mh = max(im.height for _, im in sc)
        Wt = sum(im.width for _, im in sc) + 30 * (len(sc) + 1)
        canvas = Image.new('RGB', (max(Wt, 900), mh + 110), (255, 255, 255))
        dr = ImageDraw.Draw(canvas)
        dr.text((20, 12), '%s · %s — jo_theme_fix2 합친 판(§A 데이터 + §B 앱)' % (tid, want['names'].get(tid, '')), fill=(0, 0, 0), font=font)
        x = 30
        for lb, im in sc:
            dr.text((x, 52), lb, fill=(90, 90, 90), font=small)
            canvas.paste(im, (x, 84))
            dr.rectangle([x - 1, 83, x + im.width, 84 + im.height], outline=(200, 200, 200))
            x += im.width + 30
        fn = os.path.join(out_dir, '_shot_theme_fix2_%s_합침.png' % tid)
        canvas.save(fn)
        made.append([os.path.basename(fn), canvas.size])
    p.close()
    N('C11', '그림 확인(규칙 60 · 게이트 아님) — 원본 쪽 + 합친 앱 창 나란히', made)


# ════════════════════════ 돌림 ════════════════════════
def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    raw_new = open(os.path.join(MBREAL, 'theme', 'patent_hr8', '테마.json.gz'), 'rb').read()
    raw_old = subprocess.run(['git', '-C', MBREAL, 'show', OLDT + ':theme/patent_hr8/테마.json.gz'], capture_output=True).stdout
    D, want = load(raw_new)
    want_old = load(raw_old)[1] if raw_old else None
    imgdir = os.path.join(MBREAL, 'theme', 'patent_hr8', 'img')
    N('C0', '재료', {'새': {'자리': MBREAL, 'md5': hashlib.md5(raw_new).hexdigest()[:8], '테마': want['n'], '구역 SVG 테마': len(want['svg_ids']), '그림 든 테마': len(want['img_ids']),
                          '그림': sum(want['img'].values()), '섞기': want['blend'], '기간': len(want['kigan']), 't71 text·path': want['svgcnt'].get('t71'),
                          'img 파일': len(os.listdir(imgdir)) if os.path.isdir(imgdir) else 0},
                    '옛(헛잣대)': {'판': OLDT, 'md5': hashlib.md5(raw_old).hexdigest()[:8] if raw_old else None, '테마': want_old['n'] if want_old else None},
                    '앱': NEW, '바탕 앱(헛잣대)': BASE})
    overlay('new')
    if raw_old:
        overlay('old', raw_old)
    src = H.app_src(NEW)
    base_src = H.app_src(BASE)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        print('── 새 앱 + 새 재료', flush=True)
        M = measure(br, 'new', src, want, 'n')
        J = judge(M, want)
        for c in sorted(J, key=lambda x: int(x[1:])):
            T(c, DESC[c], J[c][0], J[c][1])
        if M['errs']:
            T('C0', 'JS 오류 0(새 짝)', False, M['errs'])
        print('── 헛잣대 — 옛 재료(%s) + 새 앱 · 새 재료 + 바탕 앱(%s)' % (OLDT, BASE), flush=True)
        YD = judge(measure(br, 'old', src, want, 'yd'), want) if raw_old else {}
        YA = judge(measure(br, 'new', base_src, want, 'ya', full=False), want)
        for c in sorted(J, key=lambda x: int(x[1:])):
            yj = (YD if YARD_OF[c] == 'data' else YA).get(c)
            which = '옛 재료 %s' % OLDT if YARD_OF[c] == 'data' else '바탕 앱 %s' % BASE
            if yj is None:
                N('Y' + c[1:], '%s 헛잣대(%s) — 못 잼' % (c, which))
            elif not yj[0]:
                T('Y' + c[1:], '%s 헛잣대(%s) = FAIL(물림)' % (c, which), True, yj[1])
            else:
                N('Y' + c[1:], '%s 헛잣대(%s) 안 삶 — 바탕도 PASS' % (c, which), yj[1])
        if SHOTS:
            print('── 그림 확인(C11)', flush=True)
            shots(br, src, want, SHOTS)
        br.close()
        if 'webkit' in ENGS:
            wk = TH.webkit_try(pw)
            if wk:
                print('── WebKit iPad 834 — 그림 뜸 · 풀림(INFO)', flush=True)
                p = page(wk, 'new', 'wk', src, PAD)
                got = {tid: p.ev(WIN, tid) for tid in want['img_ids']}
                im = [x for w in got.values() if w for f in w['figs'] for x in f['img']]
                dec = [x for w in got.values() if w for x in w['dec']]
                fb = {t: fits(w) for t, w in got.items() if w and fits(w)}
                nwant = sum(want['img'].values())
                T('C10', 'WebKit iPad 834 그림 든 테마 — 그림 %d 다 뜸(blob · Image.decode) · 창 폭 · 화면 밖 0' % nwant,
                  len(im) == nwant and all(x['h'] == 'blob:' for x in im) and len(dec) == nwant and all(x[1] for x in dec) and not fb and not p.errs,
                  {'그림': len(im), 'blob': sum(1 for x in im if x['h'] == 'blob:'), '풀림 ok': sum(1 for x in dec if x[1]), '풀림 실패': [x for x in dec if not x[1]][:4], '폭·화면 밖': fb, 'JS 오류': p.errs[:3]})
                p.close()
                wk.close()
            else:
                N('C10-wk', 'WebKit 없음 — 안 잼')
    nf = sum(1 for r in RES if r[2] is False)
    npass = sum(1 for r in RES if r[2] is True)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
    print('\n══ PASS %d · FAIL %d (%.0f초) · 결과 → %s' % (npass, nf, time.time() - t0, OUTF))
    return nf


if __name__ == '__main__':
    rc = 1
    try:
        rc = 1 if main() else 0
    finally:
        shutil.rmtree(TH.TMP, ignore_errors=True)
    sys.exit(rc)
