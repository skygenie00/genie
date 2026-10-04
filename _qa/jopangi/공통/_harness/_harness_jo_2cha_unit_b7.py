# -*- coding: utf-8 -*-
"""_task_jo_2cha_unit 보탬 탐침 — D 목록 밖 두 가지를 잰다(2026-09-23 · v4).
   ① B-7 단원별에서도 회차 select · 1단 필터 · 2단 목록(c2Mark) · 연도 단추가 먹는가
   ② C-7·A-3 「노트 없음」 — 손값 · ⚙ 자동값 양쪽 · 줄 칩 · 머리 · ✎ 창(설문 칩 · 주단원 라디오 · 자동 후보)
   쓰기 : python _harness_jo_2cha_unit_b7.py > _harness_jo_2cha_unit_b7_result.txt
   _harness_jo_2cha_unit.py 의 서버·페이지 틀(P)을 그대로 빌려 쓴다(시드·網 막기 같음).
   ★ yard8(10/4 · ⑧ _task_jo_2cha_minso_board 합친 뒤 옛 잣대 고침 · 칸 이름은 그대로 — 고르는 길 · 누를 자리 · 읽는 때만 바꿈 · 옛 줄은 「옛(yard8 전)」 주석):
     ⑧ A-2-1·A-2-3(사용자 10/3 05:35·05:39) — 회차 select(.ysel)는 없고 켜진 「단원별」 0.5초 길게 → 회차 고르기 메뉴(.c2fmenu) → 첫 칸에서 죽어(예외) 뒤 칸이 다 사라졌다
     ⑧ A-2-2(사용자 10/3 05:20) — 연도 단추(.ysort)는 정렬 화살표(.c2sortar) · 같은 값(S.yearSort)
     ⑧ A-10-1·A-10-2(사용자 10/3 09:07) — 단원 칩은 평소 가림 → 칩을 읽는 칸은 먼저 편다(h.SHOW_CHIPS) · A-10-3 · 정한 것 3 — ✎ 단원 창은 「단원 N」 0.5초 길게(h.P.hold)
     옛 판(⑧ 전)에서도 같은 코드가 돈다(.ysel 이 있으면 select · 길게 누름도 click 이라 ✎ 단추가 같은 창을 연다)."""
import io, json, os, sys, importlib.util
from collections import Counter
HP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_harness_jo_2cha_unit.py')   # env_lanes_fix(9/29) — 같은 폴더(옛: N: 고정 자리)
spec = importlib.util.spec_from_file_location('h2u', HP)
h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4): --mode 는 h(2cha_unit)를 불러올 때 이미 읽혔다(같은 모듈 · 인자 읽기보다 먼저) · gate(인자 없음) = 이 판 앞과 같다
if QJ.SMOKE:   # smoke 칸 없음(보탬 탐침 — 2차 단원별 B-7 · C-7 · A-3) — 앱을 띄우기 전에 한 줄 찍고 끝
    print('INFO | smoke 칸 없음')
    sys.exit(0)
from playwright.sync_api import sync_playwright

new = open(os.path.join(h.GENIE, h.REL), 'rb').read().decode('utf-8')
os.makedirs(h.WORK, exist_ok=True)
D = json.load(open(os.path.join(h.JOD, 'data', h.UNIT_FILE), encoding='utf-8'))['문제']
R63 = sorted(k for k in D if k.startswith('26-63-'))
MAIN63 = Counter(D[k]['주'] for k in R63)

AT = """async ([sel, txt]) => { const e = [...document.querySelectorAll(sel)].find(x => !txt || x.innerText.includes(txt)); if (!e) return null;
  e.scrollIntoView({block:'center'}); await new Promise(r => setTimeout(r, 250));
  const b = e.getBoundingClientRect(), cx = b.left + b.width / 2, cy = b.top + b.height / 2, top = document.elementFromPoint(cx, cy);
  return {on: !!top && (top === e || e.contains(top)), cx, cy}; }"""
ROWS = """() => [...document.querySelectorAll('#slot .main .c2row')].map(r => ({ck: r.dataset.ck || '', ckx: r.dataset.ckx || '',
  code: (r.querySelector('.c2code') || {}).innerText || '', dim: r.classList.contains('dim'), sel: r.classList.contains('sel'),
  on: (() => { const b = r.getBoundingClientRect(); return b.bottom > 0 && b.top < innerHeight; })()}))"""
# ★ yard8 — ⑧ 뒤 회차 고르기 메뉴 항목(앱 c2FMenu 9424 · 항목 「전체 N」 · 「YY-회」) — 열린 메뉴 안에서만 찾고 메뉴 안만 굴린다
YEAR_ITEM = """([t])=>{const m=document.querySelector('.c2fmenu');if(!m)return null;const e=[...m.querySelectorAll('.it')].find(x=>String(x.innerText||'').trim().indexOf(t)===0);if(!e)return null;
  try{e.scrollIntoView({block:'nearest'})}catch(_){}const b=e.getBoundingClientRect(),cx=b.left+b.width/2,cy=b.top+b.height/2,top=document.elementFromPoint(cx,cy);
  return {on:!!top&&(top===e||e.contains(top)),cx:cx,cy:cy}}"""


def pick_year(p, val, label):
    """회차 고르기 — 옛(yard8 전) = select.ysel 에서 값을 고름 · 새 = ★ ⑧ A-2-1·A-2-3 · 사용자 10/3 05:35·05:39 — .ysel 은 없고 켜진 「단원별」 단추를 0.5초 길게 누르면 메뉴(.c2fmenu) → 항목(「전체 N」 · 「YY-회」)
    val = select 값(연도 · 비면 전체) · label = 메뉴 항목 앞글자(「26-63」 · 「전체」)"""
    if p.ev("()=>!!document.querySelector('#slot .main .ysel')"):   # 옛 판(⑧ 전)
        p.pg.select_option('#slot .main .ysel', val); p.pg.wait_for_timeout(900)
        return True
    at = p.ev(AT, ['#ordSeg button.on', ''])
    ok = p.hold(at, 400)
    it = p.ev(YEAR_ITEM, [label]) if ok else None
    p.pg.wait_for_timeout(120)   # scrollIntoView 가 낸 스크롤 알림이 누름 뒤에 와서 메뉴를 닫지 않게(⑧ 하네스 click 과 같은 까닭)
    return bool(it) and p.click(it, 900)


L = []
T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c else ' | ' + json.dumps(i, ensure_ascii=False)[:700]))

with sync_playwright() as pw:
    for eng in ('chromium', 'webkit'):
        br = getattr(pw, eng).launch()
        QJ.launch('new')
        p = h.P(br, eng, 'NEW', new, 1440, 900)
        E = '[%s] ' % eng
        try:
            # ① 회차 select — 63회만
            p.board('민사소송법', '기출', 'unit')
            u0 = p.ev('__HU.unitRead()')
            # 옛(yard8 전): p.pg.select_option('#slot .main .ysel', '2026'); p.pg.wait_for_timeout(900)
            pick_year(p, '2026', '26-63')   # ★ ⑧ A-2-1·A-2-3 · 사용자 10/3 05:35·05:39 — select → 켜진 「단원별」 길게 누름 메뉴 「26-63」(옛 판은 select 그대로)
            u1 = p.ev('__HU.unitRead()')
            heads = {x['unit']: x['rows'] for x in u1['heads'] if not x['none']}
            want_b = sorted({n.split('.')[0] for n in MAIN63})
            T(E + 'B-7 회차 select 63회 → 줄 = 63회 문제(%d) · 머리 = 그 문제들의 주단원(%d) · 머리마다 줄 수 = 문제 N · 0 인 머리 없음 · 편 띠 = 그 편만(%s)'
              % (len(R63), len(MAIN63), ','.join(want_b)),
              sorted(r['code'] for r in u1['rows']) == R63 and heads == dict(MAIN63) and all(v > 0 for v in heads.values())
              and sorted(b['no'] for b in u1['bands']) == want_b and len(u0['rows']) == 76,
              [sorted(r['code'] for r in u1['rows']), heads, dict(MAIN63), [b['no'] for b in u1['bands']], len(u0['rows'])])
            # 옛(yard8 전): p.pg.select_option('#slot .main .ysel', ''); p.pg.wait_for_timeout(900)
            pick_year(p, '', '전체')   # ★ ⑧ A-2-3 · 사용자 10/3 05:35·05:39 — 메뉴 「전체 N」
            T(E + 'B-7 회차 select 「전체」 → 다시 76줄 · 머리 40', len(p.ev('__HU.unitRead()')['rows']) == 76 and len([x for x in p.ev('__HU.unitRead()')['heads'] if not x['none']]) == 40)
            # ② 1단 필터 「채점됨」 — 흐림 집합 = 회차별과 같음 · 수 = 필터 글자
            at = p.ev(AT, ['#slot .tree .fitem', '채점됨']); ok = p.click(at, 900)
            nshow = p.ev("() => { const r = [...document.querySelectorAll('#slot .tree .fitem')].find(x => x.innerText.includes('채점됨')); return r ? +r.querySelector('em').innerText : -1; }")
            uu = [r for r in p.ev(ROWS) if r['ck']]
            p.ev("async()=>{S.c2ord='round';await render();}"); p.pg.wait_for_timeout(700)
            rr = [r for r in p.ev(ROWS) if r['ck']]
            lit_u = sorted(r['ck'] for r in uu if not r['dim']); lit_r = sorted(r['ck'] for r in rr if not r['dim'])
            T(E + 'B-7 1단 필터 「채점됨」 → 단원별 안 흐린 줄 = 회차별 안 흐린 줄 = %d · 나머지 흐림' % nshow,
              ok and nshow > 0 and lit_u == lit_r and len(lit_u) == nshow and len(uu) == 76 and sum(r['dim'] for r in uu) == 76 - nshow,
              [ok, nshow, len(lit_u), len(lit_r), sum(r['dim'] for r in uu)])
            at = p.ev(AT, ['#slot .tree .fitem', '채점됨']); p.click(at, 700)   # 필터 끔
            # ③ 2단 목록 → c2Mark — 단원별 보드의 그 줄(주 줄)이 sel · 화면 안
            p.ev("async()=>{S.c2ord='unit';await render();}"); p.pg.wait_for_timeout(700)
            ck = h.CK251
            at = p.ev("async (ck) => { const e = [...document.querySelectorAll('#slot .prow[data-ck]')].find(x => x.dataset.ck === ck); if (!e) return null;"
                      " e.scrollIntoView({block:'center'}); await new Promise(r => setTimeout(r, 250)); const b = e.getBoundingClientRect();"
                      " const cx = b.left + Math.min(40, b.width / 2), cy = b.top + b.height / 2, top = document.elementFromPoint(cx, cy);"
                      " return {on: !!top && (top === e || e.contains(top)), cx, cy}; }", ck)
            ok = p.click(at, 1500)
            rs = p.ev(ROWS)
            sel = [r for r in rs if r['sel']]
            T(E + 'B-7 2단 목록 행 누름 → 단원별 보드의 주 줄 하나만 sel · 화면 안(c2Mark)',
              ok and len(sel) == 1 and sel[0]['ck'] == ck and sel[0]['on'], [ok, at, sel])
            # ④ 연도 단추 — 머리 안 줄 차례가 뒤집힌다(내림 ↔ 오름) · 머리 차례는 목차 그대로
            def order():
                u = p.ev('__HU.unitRead()')
                return [x['unit'] for x in u['heads']], [(r['head'], r['code']) for r in u['rows']]
            h0, r0 = order()
            # 옛(yard8 전): at = p.ev(AT, ['#slot .main .ysort', '']); ok = p.click(at, 900)
            ysort = '#slot .main .c2sortar' if p.ev("()=>!!document.querySelector('#slot .main .c2sortar')") else '#slot .main .ysort'   # ★ ⑧ A-2-1·A-2-2 · 사용자 10/3 05:08·05:20 — 「연도·회차 ↓」 단추(.ysort) → 정렬 화살표 ↓↑(.c2sortar · 같은 S.yearSort) — 옛 판은 .ysort
            at = p.ev(AT, [ysort, '']); ok = p.click(at, 900)
            h1, r1 = order()
            ys = p.ev('S.yearSort')
            def key(c):
                return [int(v) for v in c.split('-')[1:]]
            def in_head(rows):
                g = {}
                for hd, c in rows:
                    g.setdefault(hd, []).append(c)
                return g
            g0, g1 = in_head(r0), in_head(r1)
            multi = [k for k in g0 if len({key(c)[0] for c in g0[k]}) > 1]
            flip = all([key(c)[0] for c in g1[k]] == sorted(key(c)[0] for c in g1[k]) and [key(c)[0] for c in g0[k]] == sorted((key(c)[0] for c in g0[k]), reverse=True) for k in multi)
            T(E + 'B-7 연도 단추 → 머리 안 회차 차례가 내림 → 오름(여러 회차가 든 머리 %d) · 머리 차례 그대로 · 줄 집합 그대로' % len(multi),
              ok and ys == 'asc' and h0 == h1 and flip and sorted(r0) == sorted(r1) and len(multi) > 0, [ok, ys, h0 == h1, flip, len(multi)])
            p.click(p.ev(AT, [ysort, '']), 700)   # ★ ⑧ A-2-2 — 옛 '#slot .main .ysort' → ysort(위)
            # ⑤ C-7 — 손값 칸의 노트 이름이 note_민소.json 에 없으면 빨간 점선 + 「노트 없음」 툴팁 · 칸은 지우지 않는다
            FAKE = '9.9.9. 없는노트(하네스)'
            hv = {'main': FAKE, 's': {'(1)': [FAKE, h.U411]}, 't': 1790000000000, 'by': '꼬까PC'}
            p.ev("([k,v])=>{const o=JSON.parse(localStorage.getItem('jopangi.c2unit')||'{}');o[k]=v;localStorage.setItem('jopangi.c2unit',JSON.stringify(o));}", ['민소|25-62-1', hv])
            p.ev("async()=>{S.c2ord='round';await render();}"); p.pg.wait_for_timeout(700)
            p.ev(h.SHOW_CHIPS)   # ★ ⑧ A-10-1 · 사용자 10/3 09:07 — 단원 칩은 평소 가림 → 칩을 읽기 전에 편다(옛 판은 늘 보임 — 같은 값)
            CH = """(fake) => { const r = [...document.querySelectorAll('#slot .main .c2row')].find(x => x.dataset.ck === 'card|기출|민기출 25-62-1'); if (!r) return null;
              const cs = [...r.querySelectorAll('.c2r3 .c2uc')].map(c => { const s = getComputedStyle(c); return {unit: c.dataset.unit, cls: c.className, title: c.title,
                bs: s.borderTopStyle, bc: s.borderTopColor}; }); return cs; }"""
            rc = p.ev(CH, FAKE)
            p.ev("async()=>{S.c2ord='unit';await render();}"); p.pg.wait_for_timeout(700)
            hd = p.ev("(fake) => { const e = [...document.querySelectorAll('#slot .c2uh')].find(x => x.dataset.unit === fake); if (!e) return null;"
                      " return {cls: e.className, title: e.title, nm: (e.querySelector('.nm') || {}).innerText, color: getComputedStyle(e.querySelector('.nm')).color,"
                      " rows: (() => { let n = 0, x = e.nextElementSibling; while (x && x.classList.contains('c2row')) { n++; x = x.nextElementSibling; } return n; })()}; }", FAKE)
            # 옛(yard8 전): at = p.ev("([c,x])=>__HU.rowAt(c,x)", [h.CK251, 'edit']); ok = p.click(at, 900)
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", [h.CK251, 'edit']); ok = p.hold(at, 900)   # ★ ⑧ A-10-3 · 정한 것 3 · 사용자 말 없음(시안 09:08 답 4) — ✎ 단추 톡 → 「단원 N」 0.5초 길게
            wc = p.ev("(fake) => [...document.querySelectorAll('.pop.c2uw .c2w-row .c2uc')].filter(c => c.dataset.n === fake).map(c => ({cls: c.className, title: c.title, bs: getComputedStyle(c).borderTopStyle}))", FAKE)
            wr_ = p.ev("(fake) => [...document.querySelectorAll('.pop.c2uw .c2w-rad')].filter(c => c.dataset.n === fake).map(c => ({cls: c.className, title: c.title, bs: getComputedStyle(c).borderTopStyle}))", FAKE)
            p.ev('__HU.closePops()')
            kept = p.ev("(k)=>{const o=JSON.parse(localStorage.getItem('jopangi.c2unit')||'{}');return o[k]||null;}", '민소|25-62-1')
            chip = [c for c in (rc or []) if c['unit'] == FAKE]
            T(E + 'C-7 노트 없는 손값 — 회차별 줄 칩 = 빨간 점선(.nonote · dashed) + 툴팁 「노트 없음」',
              len(chip) == 1 and 'nonote' in chip[0]['cls'] and chip[0]['bs'] == 'dashed' and '노트 없음' in chip[0]['title']
              and all('nonote' not in c['cls'] for c in rc if c['unit'] != FAKE), rc)
            T(E + 'C-7 노트 없는 손값 — 단원별 머리 .nonote(빨간 글자) · 그 아래 줄 1 · 툴팁 「노트 없음」',
              hd is not None and 'nonote' in hd['cls'] and '노트 없음' in hd['title'] and hd['rows'] == 1, hd)
            T(E + 'C-7 노트 없는 손값 — ✎ 창 설문 칩 .nonote(dashed · 툴팁) · 창을 열고 닫아도 칸이 그대로(지우지 않는다)',
              ok and len(wc) == 1 and 'nonote' in wc[0]['cls'] and wc[0]['bs'] == 'dashed' and '노트 없음' in wc[0]['title'] and kept == hv, [ok, wc, kept])
            T(E + 'C-7 노트 없는 손값 — ✎ 창 주단원 라디오도 .nonote(dashed · 툴팁)',
              len(wr_) == 1 and 'nonote' in wr_[0]['cls'] and wr_[0]['bs'] == 'dashed' and '노트 없음' in wr_[0]['title'], wr_)
            errs = [x for x in (p.ev('window.__ERR') or []) + p.errs if not h.NOISE(x)]
            T(E + 'B-7 JS 오류 0', not errs, errs[:5])
            p.close()
            # ⑥ A-3/C-7 — ⚙ 자동값에 노트 없는 단원이 섞였을 때(볼트 이름이 바뀐 경우) — 손값 없음 · 사본 먹임(?alt=1)
            FAKE2 = '4.9.9. 없는노트(⚙ 사본)'
            alt = json.load(open(os.path.join(h.JOD, 'data', h.UNIT_FILE), encoding='utf-8'))
            alt['문제']['25-62-1'] = {'주': h.U411, '설문': [{'no': '(1)', '단원': [{'n': h.U411, 's': '책'}, {'n': FAKE2, 's': '볼트'}]}]}
            json.dump(alt, io.open(os.path.join(h.WORK, '2cha_단원_민소.alt.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
            QJ.launch('new')
            p = h.P(br, eng, 'NEW', new, 1440, 900, q='tok=1&alt=1')
            p.board('민사소송법', '기출', 'unit')
            p.ev(h.SHOW_CHIPS)   # ★ ⑧ A-10-1 · 사용자 10/3 09:07 — 단원 칩은 평소 가림 → 걸친 칩을 읽기 전에 편다
            oc = p.ev("(fake) => { const r = [...document.querySelectorAll('#slot .main .c2row')].find(x => x.dataset.ck === 'card|기출|민기출 25-62-1'); if (!r) return null;"
                      " return [...r.querySelectorAll('.c2r3 .c2uc')].map(c => ({unit: c.dataset.unit, cls: c.className, title: c.title, bs: getComputedStyle(c).borderTopStyle})); }", FAKE2)
            # 옛(yard8 전): at = p.ev("([c,x])=>__HU.rowAt(c,x)", [h.CK251, 'edit']); ok = p.click(at, 900)
            at = p.ev("([c,x])=>__HU.rowAt(c,x)", [h.CK251, 'edit']); ok = p.hold(at, 900)   # ★ ⑧ A-10-3 · 정한 것 3 · 사용자 말 없음(시안 09:08 답 4) — ✎ 단추 톡 → 「단원 N」 0.5초 길게
            rad = p.ev("(fake) => [...document.querySelectorAll('.pop.c2uw .c2w-rad')].map(c => ({n: c.dataset.n, cls: c.className, bs: getComputedStyle(c).borderTopStyle, title: c.title}))", FAKE2)
            at = p.ev("async () => { const b = document.querySelector('.pop.c2uw .c2w-row .c2w-add'); if (!b) return null; const r = b.getBoundingClientRect();"
                      " const cx = r.left + r.width / 2, cy = r.top + r.height / 2, t = document.elementFromPoint(cx, cy); return {on: !!t && (t === b || b.contains(t)), cx, cy}; }")
            ok2 = p.click(at, 700)
            its = p.ev("(fake) => [...document.querySelectorAll('.pop.c2uw .c2w-list .c2w-it')].filter(x => x.dataset.n === fake).map(x => ({cls: x.className, title: x.title,"
                       " after: getComputedStyle(x, '::after').content, color: getComputedStyle(x).color}))", FAKE2)
            okall = p.ev("() => [...document.querySelectorAll('.pop.c2uw .c2w-list .c2w-it')].filter(x => x.classList.contains('nonote')).length")
            p.ev('__HU.closePops()')
            och = [c for c in (oc or []) if c['unit'] == FAKE2]
            T(E + 'A-3/C-7 ⚙ 자동값의 노트 없는 단원 — 단원별 줄 걸친 칩 .nonote(dashed · 툴팁)',
              len(och) == 1 and 'nonote' in och[0]['cls'] and och[0]['bs'] == 'dashed' and '노트 없음' in och[0]['title'], oc)
            fr = [x for x in (rad or []) if x['n'] == FAKE2]; gr = [x for x in (rad or []) if x['n'] != FAKE2]
            T(E + 'A-3/C-7 ✎ 창 주단원 라디오 — 노트 없는 것만 .nonote(dashed · 툴팁) · 나머지 solid',
              ok and len(fr) == 1 and 'nonote' in fr[0]['cls'] and fr[0]['bs'] == 'dashed' and '노트 없음' in fr[0]['title']
              and gr and all('nonote' not in x['cls'] and x['bs'] == 'solid' for x in gr), rad)
            T(E + 'A-3/C-7 ＋ 단원 고르개 자동 후보 — 노트 없는 것만 .nonote(빨간 글자 · 꼬리 「· 노트 없음」 · 툴팁) · 목차 전부에는 없음(1건)',
              ok2 and len(its) == 1 and 'auto' in its[0]['cls'] and 'nonote' in its[0]['cls'] and '노트 없음' in its[0]['after'] and '노트 없음' in its[0]['title']
              and its[0]['color'] == 'rgb(185, 28, 28)' and okall == 1, [ok2, its, okall])
            errs = [x for x in (p.ev('window.__ERR') or []) + p.errs if not h.NOISE(x)]
            T(E + 'A-3/C-7 JS 오류 0', not errs, errs[:5])
        except Exception as e:
            T(E + '예외', False, str(e)[:400])
        finally:
            p.close(); br.close()
    for srv, _ in h.SERVERS.values():
        srv.shutdown()
print('\n'.join(L))
print('합계 PASS %d · FAIL %d' % (sum(x.startswith('PASS') for x in L), sum(x.startswith('FAIL') for x in L)))
