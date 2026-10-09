# -*- coding: utf-8 -*-
r"""_task_ewm_list_add1 §B-1 · B-3 관문 — 조판기 1차객 첫 화면 「총 N문제」 → 수만 · 단원 줄 그 수 검정(파랑 → 검정) · 한 줄 판 그대로

  python _harness_ewm_list_add1.py [--jo <jo/index.html 파일 | 커밋>] [--root <genie 자리 · 기본 --jo 파일의 위 폴더 · 없으면 _roots.genie()>]
        [--base <커밋 · 기본 a1fbc79>] [--res <결과 파일>] [--shots <그림 폴더>] [--strict-h] [--selftest] [--dump-js <파일>]
  예 (워크트리 ewm_list = 새 판 bff7852 · 바탕 a1fbc79):
        python _harness_ewm_list_add1.py --jo <genie>/.claude/worktrees/ewm_list/jo/index.html --base a1fbc79 --res <결과 파일>
  (전수표 argv 꼴 = ewm_list 와 같게 `--jo {app} --res {res}` · --root 를 안 주면 --jo 파일의 위 폴더(jo 폴더의 위)를 genie 자리로 본다)

  NEW  = --jo 파일(없으면 <root>/jo/index.html · 예 워크트리 ewm_list bff7852 = add1 패치 판)
  BASE = git show <base>:jo/index.html — a1fbc79 = cloud/ewm_list(53cdcf6)를 합친 판 = add1 **전** = 헛잣대 바탕
         두 판을 같은 기기 · 같은 차례로 늘 같이 돌려 헛잣대(바탕 FAIL 이어야 하는 칸)와 무변 칸(바탕과 같은 값)을 한 번에 센다
  시험 기록 · 가짜 원격 · 서버 · 폭 바꾸기 = _harness_ewm_list.py(E)의 것을 그대로 불러 쓴다(진짜 기록은 열지 않는다 · 하네스가 지어낸 기록)
  데이터 = <root>/jo/data(읽기만) · 세 법(특허법 · 상표법 · 디자인보호법) × 폭 1440 · 834(서랍 열림 · 접음) · 390 첫 화면

  관문(B-1) — 매 칸은 폭(·상태)마다, 세 법을 한꺼번에 본다:
    B1a 단원 줄 .mbur>.l>.tot 글자 = 숫자만(^\d+$ · 장 머리 아래 단원 · 편 한 줄 · 깊은 머리 · (미수록)·(변형) 줄) · 회차 줄 = 「N문항 · M지문」(무변)
    B1b 단원 줄 · 회차 줄 .tot 계산색 = rgb(26, 26, 26)(--ink)
    B1c 첫 화면 어느 .tot 에도 「총」 「문제」 글자 0 · 첫 화면 글 전체에 「총 N문제」 꼴 0
    B1d 장 머리(.mbch>.hh .tot) · 카드 머리(.mbsj>.hd h2 .tot — 편 · 미분류 · 변리사 기출) 글자도 숫자만
    B1e 장 머리 · 카드 머리 .tot 계산색 = 바탕(회색 무변 — 시안 v3 · A-2)               ← 바탕과 같은 값(무변 칸)
    B1f .tot 의 수 = 바탕의 「총 N문제」 의 N(줄마다 · 일곱 자리 다 같은 수)                   ← 바탕과 같은 값(무변 칸)
    B1g 줄 높이 — 새 판 줄이 바탕보다 1px 넘게 높지 않다(한 줄 판 그대로 · 두 줄 되는 줄 0) · --strict-h 면 지시서 글자 그대로 ±1px 모든 줄
    B1h 390 가로 넘침 0(나머지 폭은 값만 INFO)
    B1i 「61x1 63x2」(.ewmn) 글자 목록 = 바탕(add1 이 안 건드림)                               ← 바탕과 같은 값(무변 칸)
    B1s 소스 자리 수 — 첫 화면 일곱 자리 「총 ' + … + '문제」 = 0(바탕 7) · .mbur>.l .tot 색 var(--ink)(바탕 var(--exc)) · A-2 안 바꾼 자리(qltot · 기출뷰 머리 · OMR)는 그대로
  관문(B-3) — 헛잣대: 바탕(a1fbc79)에서 B1a · B1b · B1c · B1d 가 FAIL 이어야 한다(셋 + 장 · 카드 = 바탕이 통과하면 잣대가 헛 것)
    B0  새 판 페이지 오류 0(바탕에도 같은 글로 나는 오류는 값만)
  엔진 = Chromium(터치 칸 아님 · 834 · 390 = 모바일 뷰포트 + 마우스) · 결과 = 화면 PASS/FAIL 줄 · --res(기본 = 임시 폴더) · 그림 = --shots(기본 = 임시 폴더)
  --selftest = 브라우저 없이 판정 함수만 가짜 값으로 시험(종료코드 0 = 다 맞음) · --dump-js = 쪽 안 JS(A1JS)를 파일로 내보냄(node --check 용)
  ⚠ 줄 높이(B1g)는 바탕 줄 수 = 새 판 줄 수 · 같은 차례 · 같은 이름일 때만 맞댄다 — 다르면 FAIL(칸이 안 맞는 것)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_fix1 A-4(2026-10-09) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · import 때 sys.argv 에서 --mode · --snap-in · --snap-out 을 뗀다(아래 E import · ARG 보다 먼저 · E 의 QC 와 몸 한 벌) · 새 갈래는 모두 QJ.GATE / QJ.REGRESS / QJ.SMOKE 안
# ── 모드(_task_qa_fix1 A-4 · 꼴 = 10/4 _task_qa_slim · 뿌리 _harness_ewm_list 의 qa_slim2 꼴과 같은 길) ──
#   gate(인자 없음) = 이 판 앞과 같음 — 바탕 a1fbc79 를 git show 로 풀어 폭마다 새 판 · 바탕 두 쪽을 같은 차례로(헛잣대 B3 · 「= 바탕」 칸)
#   regress = 새 판만 띄움(바탕 git show 0 · 바탕 쪽 띄움 0 · 그림 안 찍음) · 헛잣대(B1a~B1d 의 바탕 쪽 · B3) 안 돎 ·
#             「= 바탕」 칸(B1e 색 · B1f 수 · B1g 줄 높이 · B1i 61x1 · 넘침 값)의 바탕 자리 = 기준 스냅샷 'B1-ref@<폭 상태>'(앞 인도판 새 판 재기 · tots · rows · ewmn · fit · over · tx 만) ·
#             B1s 는 새 판 조건(일곱 자리 0 · ink 1 · exc 0 · qltot 1 · 기출뷰 머리 1) + A-2 자리 셈 = 기준 'B1s/A-2' · B0 「바탕에도 나는 오류」 = 기준 'B0/msgs'(E._rg_msg 꼴)
#   smoke   = regress 가운데 1440 한 폭 · B1s · B1a · B1b · B1c · B0 다섯 칸(쪽 하나 · 세 법)
#   셈(§B-4) = 쪽 띄움은 E.Pg 가 이미 셈(QC.launch) · 바탕 풀기 QJ.sub('git:show-app') — regress · smoke 에서 base · git:show-app = 0
import json, os, re, subprocess, sys, time, traceback   # noqa: E402
import _harness_ewm_list as E   # noqa: E402  — 서버 · 가짜 원격 · 시험 기록 · 쪽 만들기(Pg) · 결과 줄 꼴(T · TB · N)을 그대로 쓴다(import 만으로는 아무것도 안 돈다)

ARG = E.ARG
JO_ARG = ARG('--jo')   # 새 판 = jo/index.html 파일 또는 커밋(E 와 같은 --jo 꼴 · 전수표 argv 가 {app} 를 준다)


def _root_of(jo):
    """--jo 가 .../jo/index.html 이면 그 위 폴더 = genie 자리"""
    if jo and os.path.isfile(jo):
        d = os.path.dirname(os.path.abspath(jo))
        if os.path.basename(d).lower() == 'jo':
            return os.path.dirname(d)
    return None


ROOT = ARG('--root') or _root_of(JO_ARG) or _roots.genie()
BASE = ARG('--base', 'a1fbc79')   # E.BASE 와 같은 값(같은 --base 를 둘 다 읽는다)
OUTF = ARG('--res', os.path.join(E.TMPD, '_harness_ewm_list_add1_result.txt'))
STRICT_H = '--strict-h' in sys.argv
LAWS = E.LAWS   # ('특허법', '상표법', '디자인보호법')
INK = 'rgb(26, 26, 26)'
DIGITS = re.compile(r'\d+')
ROUND = re.compile(r'\d+문항 · \d+지문')
STATES = {1440: [('', False)], 834: [('서랍 열림', False), ('서랍 접음', True)], 390: [('', False)]}   # 폭 → (이름, 서랍 접음)
STEP = []


# ════════════════════════ 쪽 안 JS — 첫 화면 .tot · 줄 높이 · 넘침 ════════════════════════
A1JS = r"""(function(){ if (window.__A1) return;
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
const noTot = h => { if (!h) return ''; const c = h.cloneNode(true); c.querySelectorAll('.tot, .ewmn').forEach(t => t.remove()); return txt(c); };
window.__A1 = {
  /* 첫 화면(#slot .mbdash) — 줄 · 머리 · 카드 .tot 전수(차례대로) · 줄 높이 · 「61x1」 · 한 줄로 맞춘 줄 · 가로 넘침 */
  measure(){
    const d = document.querySelector('#slot .mbdash'); if (!d) return null;
    const tots = [...d.querySelectorAll('.tot')].map(e => { let k = 'other', nm = '';
      if (e.matches('.mbur > .l > .tot')){ k = e.closest('.mbur').hasAttribute('data-giy') ? 'round' : 'unit'; nm = txt(e.parentElement.querySelector(':scope > .nm')); }
      else if (e.matches('.mbch > .hh > .tot')){ k = 'chap'; nm = txt(e.parentElement.querySelector(':scope > .nm')); }
      else if (e.matches('.mbsj > .hd > h2 > .tot')){ k = 'card'; nm = noTot(e.parentElement); }
      const s = getComputedStyle(e);
      return { k: k, nm: nm.slice(0, 40), t: txt(e), c: s.color, fs: s.fontSize, fw: s.fontWeight, v: vis(e) ? 1 : 0 }; });
    const rows = [...d.querySelectorAll('.mbur, .mbch > .hh, .mbsj > .hd')].filter(vis).map(r => {
      const k = r.matches('.mbur') ? (r.hasAttribute('data-giy') ? 'y' : 'u') : (r.matches('.mbch > .hh') ? 'h' : 'c');
      const nm = k === 'c' ? noTot(r.querySelector('h2')) : txt(r.querySelector(':scope > .nm') || r.querySelector(':scope > .l > .nm'));
      return { k: k, nm: nm.slice(0, 40), h: +r.getBoundingClientRect().height.toFixed(1), e: r.querySelector('.ewmn') ? 1 : 0, f: r.classList.contains('ewmfit') ? 1 : 0 }; });
    const all = txt(d).match(/총 \d+문제/g) || [];
    const de = document.documentElement;
    return { tots: tots, rows: rows, ewmn: [...d.querySelectorAll('.ewmn')].map(txt), tx: { n: all.length, s: all.slice(0, 3) },
             fit: [...d.querySelectorAll('.mbur.ewmfit')].map(r => txt(r.querySelector('.nm')).slice(0, 20)), over: { sw: de.scrollWidth, iw: innerWidth } };
  },
  top(){ const e = document.querySelector('#slot .mbdash .mbur > .l > .tot'); if (e) try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} return !!e; }
};
})();"""


# ════════════════════════ 판정 — 순수 함수(브라우저 없이 --selftest 로 시험) ════════════════════════
def tots(v, *kinds):
    """v = {법: 첫 화면 재기} → 그 종류(unit 단원 줄 · round 회차 줄 · chap 장 머리 · card 카드 머리 · other)의 .tot 목록(법 차례 · 줄 차례)"""
    return [r for law in sorted(v or {}) for r in ((v[law] or {}).get('tots') or []) if r.get('k') in kinds]


def j_digits(v):
    """B1a — 단원 줄 .tot = 숫자만 · 회차 줄 = 「N문항 · M지문」 · 단원 줄 1개 이상"""
    u, y = tots(v, 'unit'), tots(v, 'round')
    return bool(u) and all(DIGITS.fullmatch(r['t']) for r in u) and all(ROUND.fullmatch(r['t']) for r in y)


def j_ink(v):
    """B1b — 단원 줄 · 회차 줄 .tot 계산색 = rgb(26, 26, 26)"""
    xs = tots(v, 'unit', 'round')
    return bool(xs) and all(r['c'] == INK for r in xs)


def j_nochar(v):
    """B1c — 첫 화면 어느 .tot 에도 「총」 「문제」 0 · 글 전체에 「총 N문제」 꼴 0"""
    xs = tots(v, 'unit', 'chap', 'card', 'round', 'other')
    return bool(xs) and all(('총' not in r['t']) and ('문제' not in r['t']) for r in xs) and all(((m or {}).get('tx') or {}).get('n', 1) == 0 for m in (v or {}).values())


def j_head_digits(v):
    """B1d — 장 머리 · 카드 머리 .tot 도 숫자만(장 머리 1개 이상 · 카드 머리 1개 이상)"""
    ch, cd = tots(v, 'chap'), tots(v, 'card')
    return bool(ch) and bool(cd) and all(DIGITS.fullmatch(r['t']) for r in ch + cd)


def nums(r):
    """.tot 글에서 수만 — 옛 「총 554문제」 와 새 「554」 가 같은 수를 낸다 · 회차 줄 「20문항 · 98지문」 = (20, 98)"""
    return tuple(int(x) for x in re.findall(r'\d+', r.get('t') or ''))


def key_list(v, *kinds):
    return [(law, r['k'], r['nm'], nums(r)) for law in sorted(v or {}) for r in ((v[law] or {}).get('tots') or []) if r['k'] in kinds]


def j_nums_same(vn, vb):
    """B1f — 새 판 .tot 의 수 = 바탕 .tot 의 수(법 · 종류 · 이름 · 차례까지) — 일곱 자리 다"""
    a, b = key_list(vn, 'unit', 'chap', 'card', 'round', 'other'), key_list(vb, 'unit', 'chap', 'card', 'round', 'other')
    return bool(a) and a == b


def j_color_same(vn, vb):
    """B1e — 장 머리 · 카드 머리 .tot 계산색 = 바탕(회색 무변)"""
    f = lambda v: [(law, r['k'], r['nm'], r['c']) for law in sorted(v or {}) for r in ((v[law] or {}).get('tots') or []) if r['k'] in ('chap', 'card')]
    a, b = f(vn), f(vb)
    return bool(a) and a == b


def h_cmp(rn, rb):
    """줄 높이 맞댐 — 같은 차례 · 같은 이름의 줄끼리. 앞은 새 판 줄 목록 · 뒤는 바탕 줄 목록(재기 rows)"""
    rn, rb = rn or [], rb or []
    same = len(rn) == len(rb) and all(x['k'] == y['k'] and x['nm'] == y['nm'] for x, y in zip(rn, rb))
    up, down, dmax = [], [], 0.0
    if same:
        for x, y in zip(rn, rb):
            d = round(x['h'] - y['h'], 1)
            dmax = max(dmax, abs(d))
            if d > 1:
                up.append([x['nm'][:18], y['h'], x['h'], x['e']])
            elif d < -1:
                down.append([x['nm'][:18], y['h'], x['h'], x['e']])
    return {'줄': len(rn), '바탕 줄': len(rb), '같은 차례': same, '1 넘게 높아진 줄': len(up), '높아진 보기(이름 · 바탕 · 새 판 · .ewmn)': up[:4],
            '1 넘게 낮아진 줄': len(down), '낮아진 보기(이름 · 바탕 · 새 판 · .ewmn)': down[:4], '최대 차': dmax}


def h_ok(c, strict=False):
    """기본 = 새 판 줄이 바탕보다 1px 넘게 높은 줄 0(한 줄 판 그대로 — 글자가 짧아져 한 줄이 된 줄은 허용) · strict = 모든 줄 ±1px(지시서 글자 그대로)"""
    return bool(c['줄']) and c['같은 차례'] and c['1 넘게 높아진 줄'] == 0 and (not strict or c['1 넘게 낮아진 줄'] == 0)


def h_all(vn, vb):
    """법마다 줄 높이 맞댐 → 한 칸으로(줄 수 합 · 어긋난 법 목록)"""
    out = {law: h_cmp((vn.get(law) or {}).get('rows'), (vb.get(law) or {}).get('rows')) for law in LAWS if law in vn}
    return out


def h_all_ok(c, strict=False):
    # 옛 줄: return bool(c) and all(h_ok(x, strict) for x in c.values())
    # ★ 10/5 첫 실행 뒤 — 디자인보호법은 첫 화면 줄이 바탕 · 새 판 둘 다 0 이라 h_ok 의 「줄 > 0」 에 늘 걸렸다 → 둘 다 0 인 법은 건너뜀 · 전체 줄 > 0 은 그대로
    xs = [x for x in c.values() if x['줄'] or x['바탕 줄']]
    return bool(xs) and all(h_ok(x, strict) for x in xs)


def h_show(c):
    return {law: {k: v for k, v in x.items() if k in ('줄', '바탕 줄', '같은 차례', '1 넘게 높아진 줄', '1 넘게 낮아진 줄', '최대 차')} for law, x in c.items()} | \
           {'보기': {law: (x['높아진 보기(이름 · 바탕 · 새 판 · .ewmn)'] or x['낮아진 보기(이름 · 바탕 · 새 판 · .ewmn)']) for law, x in c.items()
                    if x['높아진 보기(이름 · 바탕 · 새 판 · .ewmn)'] or x['낮아진 보기(이름 · 바탕 · 새 판 · .ewmn)']}}


def j_ewmn_same(vn, vb):
    f = lambda v: [(law, (v[law] or {}).get('ewmn')) for law in sorted(v or {})]
    a, b = f(vn), f(vb)
    return a == b and any(x[1] for x in a)


def j_over(v, w):
    """B1h — 가로 넘침 0(scrollWidth ≤ innerWidth)"""
    xs = [m['over'] for m in (v or {}).values() if m]
    return bool(xs) and all(o['sw'] <= o['iw'] for o in xs)


def src_census(sn, sb):
    """B1s — 소스 자리 수(브라우저 없이) — 새 판 · 바탕 글에서 센다"""
    site = re.compile(r"(?:'tot', |\.textContent = )'총 ' \+")
    ink = ".mbur>.l .tot{font-size:11px;font-weight:600;color:var(--ink);"
    exc = ".mbur>.l .tot{font-size:11px;font-weight:600;color:var(--exc);"
    ql = "el('span','qltot','총 '+total+'문제')"
    ev = "번 / 총 ' + list.length + '문제'"
    omr = "' / 총 ' + "
    c = lambda s: {'일곱 자리': len(site.findall(s)), 'tot ink': s.count(ink), 'tot exc': s.count(exc), 'qltot': s.count(ql), '기출뷰 머리': s.count(ev), 'OMR 「/ 총」': s.count(omr)}
    n, b = c(sn), c(sb)
    ok = n['일곱 자리'] == 0 and b['일곱 자리'] == 7 and n['tot ink'] == 1 and n['tot exc'] == 0 and b['tot ink'] == 0 and b['tot exc'] == 1 \
        and all(n[k] == b[k] for k in ('qltot', '기출뷰 머리', 'OMR 「/ 총」')) and n['qltot'] == 1 and n['기출뷰 머리'] == 1
    return ok, {'새 판': n, '바탕': b}


if QJ.REGRESS:   # regress 기준 스냅샷 꼴(_task_qa_fix1 A-4) — gate 에서는 안 지음
    def _ref(v):
        """재기 → 기준 스냅샷 꼴 — 「= 바탕」 칸(B1e · B1f · B1g · B1i · 넘침 값)이 읽는 칸만 · .tot · 줄은 짧은 배열(스냅샷 크기)"""
        out = {}
        for law in sorted(v or {}):
            m = v[law]
            out[law] = None if not m else {'tots': [[r.get('k'), r.get('nm'), r.get('t'), r.get('c')] for r in (m.get('tots') or [])],
                                           'rows': [[r.get('k'), r.get('nm'), r.get('h'), r.get('e')] for r in (m.get('rows') or [])],
                                           'ewmn': m.get('ewmn'), 'fit': m.get('fit'), 'over': m.get('over'), 'tx': m.get('tx')}
        return out

    def _unref(b):
        """기준 스냅샷 꼴 → 재기 꼴(판정 함수 j_color_same · j_nums_same · h_all · j_ewmn_same · 넘침 값을 그대로 쓴다) · 세 법 자리를 늘 채움"""
        out = {}
        for law in LAWS:
            m = (b or {}).get(law)
            out[law] = None if not m else {'tots': [{'k': x[0], 'nm': x[1], 't': x[2], 'c': x[3]} for x in (m.get('tots') or [])],
                                           'rows': [{'k': x[0], 'nm': x[1], 'h': x[2], 'e': x[3]} for x in (m.get('rows') or [])],
                                           'ewmn': m.get('ewmn'), 'fit': m.get('fit'), 'over': m.get('over') or {'sw': None, 'iw': None}, 'tx': m.get('tx')}
        return out


# ════════════════════════ 재기 ════════════════════════
def git_show(root, rev, rel):
    r = subprocess.run(['git', '-C', root, '-c', 'core.quotepath=false', 'show', rev + ':' + rel], capture_output=True)
    return r.stdout.decode('utf-8') if r.returncode == 0 and r.stdout else None


def go(p, w, law, fold):
    o = {'law': law, 'tab': 'jimun', 'jimunTab': 'ox', 'mok': None, 'oxQ': '', 'jtFold': (w <= 480) or fold, 'jtCh': {}, 'mbCh': {}, 'omr': False}
    p.ev("o => __EL.go(o)", o)
    p.ev("() => __EL.mln()")
    p.ev("o => __EL.go(o)", o)
    p.wait(300)


def measure(p, w, law, fold):
    """한 쪽 · 한 법의 첫 화면 재기 · 834 서랍 접음 = jtPaint 만(render 없음 · ResizeObserver 다음 틀에 다시 잼 — E.scan_jo 와 같은 길)"""
    go(p, w, law, False)
    if fold:
        p.ev("() => { S.jtFold = true; jtPaint(); }")
        p.wait(500)
    m = p.ev("() => __A1.measure()")
    if fold:
        p.ev("() => { S.jtFold = false; jtPaint(); }")
        p.wait(300)
    return m


def run_width(br, w, sn, sb):
    # 옛 줄: pn, pb = E.Pg(br, 'jo', 'NEW_%d' % w, sn, w), E.Pg(br, 'jo', 'BASE_%d' % w, sb, w)
    pn, pb = E.Pg(br, 'jo', 'NEW_%d' % w, sn, w), (E.Pg(br, 'jo', 'BASE_%d' % w, sb, w) if QJ.GATE else None)   # regress · smoke — 바탕(a1fbc79) 쪽 안 띄움
    # 옛 줄: pages = {'NEW': pn, 'BASE': pb}
    pages = {'NEW': pn, 'BASE': pb} if QJ.GATE else {'NEW': pn}
    try:
        for p in pages.values():
            E.N('B0', '조판기 %s %d 기록 받기 EWM.st' % (p.tag.split('_')[0], w), p.ewm_ok())
            p.ev(A1JS)
        for sname, fold in STATES[w]:
            M = {'NEW': {}, 'BASE': {}}
            for law in LAWS:
                for tag, p in pages.items():
                    M[tag][law] = measure(p, w, law, fold)
            tag_ = '%d%s' % (w, (' ' + sname) if sname else '')
            vn, vb = M['NEW'], M['BASE']
            if QJ.REGRESS:   # regress · smoke — 바탕 쪽 재기 없음: 헛잣대 칸(B1a~B1d · TB)엔 바탕 None(새 판 조건만 · YARD 0)
                vb = None
            cnt = lambda v: {k: len(tots(v, k)) for k in ('unit', 'round', 'chap', 'card', 'other')}
            E.N('B1', '조판기 %s 첫 화면 .tot 수(종류별 · 세 법 합)' % tag_, {'새 판': cnt(vn), '바탕': cnt(vb)})
            g = 'B1'
            sh = lambda v: {'unit': [r['t'] for r in tots(v, 'unit')][:6], 'round': [r['t'] for r in tots(v, 'round')][:3], '단원 줄': len(tots(v, 'unit')), '회차 줄': len(tots(v, 'round'))}
            E.TB(g, '조판기 %s 단원 줄 .mbur>.l>.tot 글자 = 숫자만(^\\d+$) · 회차 줄 = 「N문항 · M지문」' % tag_, j_digits, vn, vb, show=sh)
            E.TB(g, '조판기 %s 단원 줄 · 회차 줄 .tot 계산색 = rgb(26, 26, 26)' % tag_, j_ink, vn, vb,
                 show=lambda v: {'색': sorted({r['c'] for r in tots(v, 'unit', 'round')}), '줄': len(tots(v, 'unit', 'round'))})
            E.TB(g, '조판기 %s 첫 화면 .tot 어디에도 「총」 「문제」 글자 0 · 「총 N문제」 꼴 0' % tag_, j_nochar, vn, vb,
                 show=lambda v: {'.tot 중 총·문제': sum(1 for r in tots(v, 'unit', 'chap', 'card', 'round', 'other') if '총' in r['t'] or '문제' in r['t']),
                                 '글 전체 「총 N문제」': {law: (m or {}).get('tx') for law, m in v.items()}})
            if QJ.SMOKE:   # smoke — 이 상태는 B1a · B1b · B1c 까지(B1d · 「= 바탕」 칸 · 넘침은 smoke 밖)
                continue
            E.TB(g, '조판기 %s 장 머리 · 카드 머리(편 · 미분류 · 변리사 기출) .tot 글자 = 숫자만' % tag_, j_head_digits, vn, vb,
                 show=lambda v: {'장 머리': [r['t'] for r in tots(v, 'chap')][:4], '카드 머리': [r['t'] for r in tots(v, 'card')][:4]})
            if QJ.REGRESS:   # 「= 바탕」 칸(B1e 색 · B1f 수 · B1g 줄 높이 · B1i 61x1 · 넘침 값)부터 바탕 자리 = 기준 스냅샷(앞 인도판 새 판 재기 · 없으면 첫 기록)
                vb = _unref(QJ.base('B1-ref@%s' % tag_, _ref(vn)))
            E.T('B1', '조판기 %s 장 머리 · 카드 머리 .tot 계산색 = 바탕(회색 무변)' % tag_, j_color_same(vn, vb),
                {'새 판': sorted({r['c'] for r in tots(vn, 'chap', 'card')}), '바탕': sorted({r['c'] for r in tots(vb, 'chap', 'card')})})
            a, b = key_list(vn, 'unit', 'chap', 'card', 'round', 'other'), key_list(vb, 'unit', 'chap', 'card', 'round', 'other')
            diff = [[x, y] for x, y in zip(a, b) if x != y]
            E.T('B1', '조판기 %s .tot 의 수 = 바탕 「총 N문제」 의 N(법 · 종류 · 이름 · 차례 같음 · 일곱 자리 다)' % tag_, j_nums_same(vn, vb),
                {'새 판 칸': len(a), '바탕 칸': len(b), '다른 칸': len(diff), '보기': diff[:4]})
            c = h_all(vn, vb)
            E.T('B1', '조판기 %s 줄 높이 — %s' % (tag_, '바탕과 ±1px(모든 줄 · --strict-h)' if STRICT_H else '바탕보다 1px 넘게 높은 줄 0(한 줄 판 그대로)'), h_all_ok(c, STRICT_H), h_show(c))
            E.N('B1', '조판기 %s 한 줄로 맞춘 줄(.ewmfit — 글자가 짧아져 바탕과 다를 수 있다)' % tag_,
                {law: [len((vn[law] or {}).get('fit') or []), len((vb[law] or {}).get('fit') or [])] for law in LAWS})
            E.T('B1', '조판기 %s 「61x1 63x2」(.ewmn) 글자 목록 = 바탕(무변)' % tag_, j_ewmn_same(vn, vb),
                {law: [len((vn[law] or {}).get('ewmn') or []), len((vb[law] or {}).get('ewmn') or [])] for law in LAWS})
            ov = {law: [m['over']['sw'], m['over']['iw']] for law, m in vn.items() if m}
            ovb = {law: [m['over']['sw'], m['over']['iw']] for law, m in vb.items() if m}
            if w == 390:
                E.T('B1', '조판기 390 가로 넘침 0(세 법 · scrollWidth ≤ innerWidth · 바탕 %s)' % ovb, j_over(vn, w), {'새 판 [sw, iw]': ov, '바탕 [sw, iw]': ovb})
            else:
                E.N('B1', '조판기 %s 가로 넘침 값(지시서는 390 만 판정)' % tag_, {'새 판 [sw, iw]': ov, '바탕 [sw, iw]': ovb})
        # 그림(눈으로 보는 용 · 판정 아님) — 특허법 첫 화면
        if QJ.REGRESS:   # regress · smoke — 그림 안 찍음(판정 아님 · 시간)
            return
        for tag, p in pages.items():
            go(p, w, '특허법', False)
            p.ev("() => __A1.top()")
            E.N('그림', '조판기 %s %d 특허법 첫 화면' % (tag, w), os.path.basename(p.shot('a1_dash')))
    finally:
        for p in pages.values():
            p.close()


def summary(t0):
    y_bad = [y for y in E.YARD if y[2]]
    # 옛 줄: E.T('B3', '헛잣대 — 바탕(%s)에서 단원 줄 숫자만 · 계산색 · 「총」「문제」 0 · 장 · 카드 머리 숫자만 이 모두 FAIL(%d 칸)' % (BASE, len(E.YARD)),
    # 옛 줄:     len(E.YARD) > 0 and not y_bad, {'헛잣대 칸': len(E.YARD), '바탕이 통과한 칸': [y[1] for y in y_bad]})
    if QJ.GATE:
        E.T('B3', '헛잣대 — 바탕(%s)에서 단원 줄 숫자만 · 계산색 · 「총」「문제」 0 · 장 · 카드 머리 숫자만 이 모두 FAIL(%d 칸)' % (BASE, len(E.YARD)),
            len(E.YARD) > 0 and not y_bad, {'헛잣대 칸': len(E.YARD), '바탕이 통과한 칸': [y[1] for y in y_bad]})
    else:   # regress · smoke — 헛잣대(바탕을 띄워야 함)는 gate 몫
        E.N('B3', '헛잣대 — 안 돎(바탕 %s 안 띄움 · gate 몫)' % BASE, QJ.MODE)
    n_pass = sum(1 for r in E.RES if r[2] is True)
    n_fail = sum(1 for r in E.RES if r[2] is False)
    lines = ['', '=' * 100, '_harness_ewm_list_add1 — PASS %d · FAIL %d · INFO %d · %d초' % (n_pass, n_fail, sum(1 for r in E.RES if r[2] is None), round(time.time() - t0)),
             '헛잣대(바탕 %s · 같은 차례 · FAIL 이어야 함): %d 칸 중 바탕이 통과한 칸 %d' % (BASE, len(E.YARD), len(y_bad))]
    lines += ['  바탕 통과(헛잣대 실패): %s · %s' % (g, nm) for g, nm, _ in y_bad]
    if QJ.REGRESS:
        lines += ['모드 = %s — 바탕 %s 안 띄움 · 헛잣대 없음(위 0 칸은 그 뜻) · 「= 바탕」 칸 = 기준 스냅샷' % (QJ.MODE, BASE)]
    lines += ['줄 높이 판정 = %s' % ('모든 줄 ±1px(--strict-h)' if STRICT_H else '새 판 줄이 바탕보다 1px 넘게 높은 줄 0')]
    lines += ['단계별 초: ' + ' · '.join('%s %d' % s for s in STEP)]
    lines += ['FAIL: %s · %s' % (r[0], r[1]) for r in E.RES if r[2] is False]
    print('\n'.join(lines), flush=True)
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for g, nm, ok, d in E.RES:
            f.write('%s | %s · %s | %s\n' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), g, nm, E._s(d)))
        f.write('\n'.join(lines) + '\n')
    print('결과 파일: %s · 그림: %s' % (OUTF, E.SHOTS), flush=True)
    return 0 if not n_fail else 1


def main():
    t0 = time.time()
    os.makedirs(E.TMPD, exist_ok=True)
    if os.path.isdir(os.path.join(ROOT, 'jo', 'data')):
        E.JODATA = os.path.join(ROOT, 'jo', 'data')   # 데이터도 새 판 자리 것(두 판 같은 데이터 · 없으면 E 의 기본 = _roots.genie('jo','data'))
    if JO_ARG and not os.path.isfile(JO_ARG):   # --jo 가 커밋이면 git 에서(E.app_src 와 같은 길)
        npath, sn = JO_ARG + ':jo/index.html', git_show(ROOT, JO_ARG, 'jo/index.html')
    else:
        npath = JO_ARG or os.path.join(ROOT, 'jo', 'index.html')
        sn = open(npath, 'rb').read().decode('utf-8') if os.path.isfile(npath) else None
    # 옛 줄: sb = git_show(ROOT, BASE, 'jo/index.html')
    if QJ.GATE:
        QJ.sub('git:show-app')   # 셈 — 바탕 앱 풀기(regress · smoke 는 0)
    sb = git_show(ROOT, BASE, 'jo/index.html') if QJ.GATE else None   # regress · smoke — 바탕(a1fbc79) 안 풂(git show 0)
    # 옛 줄: if not sn or not sb:
    if not sn or (QJ.GATE and not sb):
        print('NG | 소스를 못 읽음 — 새 판 %s(%s) · 바탕 %s(%s) · 위치 %s' % (npath, bool(sn), BASE, bool(sb), ROOT), flush=True)
        return 2
    # 옛 줄: print('INFO | 새 판 %s md5(LF) %s · %s B · 바탕 %s md5(LF) %s · %s B' % (npath, E.md5lf(sn), len(sn.encode('utf-8')), BASE, E.md5lf(sb), len(sb.encode('utf-8'))), flush=True)
    if QJ.GATE:
        print('INFO | 새 판 %s md5(LF) %s · %s B · 바탕 %s md5(LF) %s · %s B' % (npath, E.md5lf(sn), len(sn.encode('utf-8')), BASE, E.md5lf(sb), len(sb.encode('utf-8'))), flush=True)
    else:
        print('INFO | 새 판 %s md5(LF) %s · %s B · 바탕 %s 안 풂(%s — 헛잣대 없음 · 「= 바탕」 칸 = 기준 스냅샷)' % (npath, E.md5lf(sn), len(sn.encode('utf-8')), BASE, QJ.MODE), flush=True)
    # 옛 줄: ok, d = src_census(sn, sb)
    # 옛 줄: E.T('B1s', '소스 자리 수 — 첫 화면 「총 N문제」 글을 짓던 일곱 자리 0(바탕 7) · .mbur>.l .tot 색 var(--ink)(바탕 var(--exc)) · A-2 자리(qltot · 기출뷰 머리 · OMR) 무변', ok, d)
    if QJ.GATE:
        ok, d = src_census(sn, sb)
        E.T('B1s', '소스 자리 수 — 첫 화면 「총 N문제」 글을 짓던 일곱 자리 0(바탕 7) · .mbur>.l .tot 색 var(--ink)(바탕 var(--exc)) · A-2 자리(qltot · 기출뷰 머리 · OMR) 무변', ok, d)
    else:   # regress · smoke — 새 판 조건(일곱 자리 0 · tot ink 1 · exc 0 · qltot 1 · 기출뷰 머리 1) 그대로 · 「바탕 7 · 바탕 exc」 는 헛잣대라 뺌 · A-2 자리 무변 = 기준 스냅샷(앞 인도판 새 판 셈)
        n2 = src_census(sn, sn)[1]['새 판']
        a2 = {k: n2[k] for k in ('qltot', '기출뷰 머리', 'OMR 「/ 총」')}
        b2 = QJ.base('B1s/A-2', a2)
        E.T('B1s', '소스 자리 수 — 첫 화면 「총 N문제」 글을 짓던 일곱 자리 0(바탕 7) · .mbur>.l .tot 색 var(--ink)(바탕 var(--exc)) · A-2 자리(qltot · 기출뷰 머리 · OMR) 무변',
            n2['일곱 자리'] == 0 and n2['tot ink'] == 1 and n2['tot exc'] == 0 and n2['qltot'] == 1 and n2['기출뷰 머리'] == 1 and QJ.norm(a2) == b2,
            {'새 판': n2, '기준(A-2 자리)': b2, '기준 출처': QJ.base_note('B1s/A-2')})
    E.N('기록', '지어낸 시험 기록(하네스 실행 중 · 파일 없음)', {'틀림 줄': ['%s %d-%d' % (x['s'], x['r'], x['i']) for x in E.WR]})
    with E.sync_playwright() as pw:
        br = pw.chromium.launch()
        for w in E.WIDTHS:
            if QJ.SMOKE and w != 1440:   # smoke — 1440 한 폭만(B1s · B1a · B1b · B1c · B0)
                continue
            t1 = time.time()
            try:
                run_width(br, w, sn, sb)
            except Exception:
                E.T('B1', '조판기 %d 실행 오류' % w, False, traceback.format_exc()[-1500:])
            STEP.append(('폭 %d' % w, round(time.time() - t1)))
        br.close()
    base_msgs = {re.sub(r' @\d*$', '', m) for k, v in E.ERRS.items() if ' BASE' in k for m in v}
    if QJ.REGRESS:   # regress · smoke — 바탕 쪽 안 띄움: 「바탕에도 나는 오류」 = 기준 스냅샷(앞 인도판 새 판 오류 글 · @줄 · 포트 뺀 꼴 — 뿌리 _harness_ewm_list B0 와 같은 길 E._rg_msg)
        base_msgs = set(QJ.base('B0/msgs', sorted({E._rg_msg(m) for k, v in E.ERRS.items() if ' NEW' in k for m in v})))
    for k, v in E.ERRS.items():
        if ' NEW' in k:
            # 옛 줄: own = [m for m in v if re.sub(r' @\d*$', '', m) not in base_msgs]
            own = [m for m in v if (re.sub(r' @\d*$', '', m) if QJ.GATE else E._rg_msg(m)) not in base_msgs]
            E.T('B0', '%s 페이지 오류 0(바탕에도 같은 글로 나는 오류는 값만 · %d)' % (k, len(v) - len(own)), not own, {'새 판만': own[:5], '바탕과 같음': sorted({m for m in v if m not in own})[:3]})
        else:
            E.N('B0', '%s 페이지 오류' % k, v[:5])
    return summary(t0)


# ════════════════════════ --selftest — 판정 함수를 가짜 값으로 ════════════════════════
def _tot(k, t, nm='x', c=INK):
    return {'k': k, 'nm': nm, 't': t, 'c': c, 'fs': '11px', 'fw': '600', 'v': 1}


def _row(k, nm, h, e=0, f=0):
    return {'k': k, 'nm': nm, 'h': h, 'e': e, 'f': f}


def selftest():
    GRAY = 'rgb(154, 149, 139)'
    BLUE = 'rgb(47, 111, 208)'
    new = {'특허법': {'tots': [_tot('card', '68', '1 특허제도', GRAY), _tot('chap', '12', 'ⅰ', GRAY), _tot('unit', '554', 'a'), _tot('unit', '0', 'b'), _tot('round', '20문항 · 98지문', '2009년')],
                    'rows': [_row('u', 'a', 33), _row('u', 'b', 33, 1, 1)], 'ewmn': ['63x2'], 'tx': {'n': 0, 's': []}, 'over': {'sw': 390, 'iw': 390}}}
    old = {'특허법': {'tots': [_tot('card', '총 68문제', '1 특허제도', GRAY), _tot('chap', '총 12문제', 'ⅰ', GRAY), _tot('unit', '총 554문제', 'a', BLUE), _tot('unit', '총 0문제', 'b', BLUE),
                            _tot('round', '20문항 · 98지문', '2009년', BLUE)],
                    'rows': [_row('u', 'a', 33), _row('u', 'b', 50, 1, 0)], 'ewmn': ['63x2'], 'tx': {'n': 4, 's': ['총 68문제']}, 'over': {'sw': 390, 'iw': 390}}}
    bad = []

    def chk(name, got, want):
        if got != want:
            bad.append((name, got, want))
        print('%s | selftest · %s | got %s · want %s' % ('PASS' if got == want else 'FAIL', name, got, want))
    # 새 판 = 모두 참 · 바탕 = 헛잣대 칸 모두 거짓
    chk('새 판 j_digits', j_digits(new), True)
    chk('바탕 j_digits(헛잣대)', j_digits(old), False)
    chk('새 판 j_ink', j_ink(new), True)
    chk('바탕 j_ink(헛잣대)', j_ink(old), False)
    chk('새 판 j_nochar', j_nochar(new), True)
    chk('바탕 j_nochar(헛잣대)', j_nochar(old), False)
    chk('새 판 j_head_digits', j_head_digits(new), True)
    chk('바탕 j_head_digits(헛잣대)', j_head_digits(old), False)
    chk('j_nums_same 새 = 바탕(수만 같고 글자 다름)', j_nums_same(new, old), True)
    chk('j_color_same 회색 무변', j_color_same(new, old), True)
    # 나쁜 새 판 — 하나씩 어긋나면 해당 칸만 거짓
    n2 = json.loads(json.dumps(new)); n2['특허법']['tots'][2]['t'] = '554문제'
    chk('j_digits — 「554문제」 섞임', j_digits(n2), False)
    chk('j_nochar — 「문제」 섞임', j_nochar(n2), False)
    n3 = json.loads(json.dumps(new)); n3['특허법']['tots'][2]['c'] = BLUE
    chk('j_ink — 파랑 남음', j_ink(n3), False)
    n4 = json.loads(json.dumps(new)); n4['특허법']['tots'][2]['t'] = '555'
    chk('j_nums_same — 수가 다름', j_nums_same(n4, old), False)
    n5 = json.loads(json.dumps(new)); n5['특허법']['tx'] = {'n': 1, 's': ['총 5문제']}
    chk('j_nochar — 글 전체 「총 N문제」 남음', j_nochar(n5), False)
    n6 = json.loads(json.dumps(new)); n6['특허법']['tots'][0]['t'] = '총 68'
    chk('j_head_digits — 카드 머리 「총 68」', j_head_digits(n6), False)
    chk('빈 값 j_digits(표본 0건 = 거짓)', j_digits({}), False)
    chk('빈 값 j_ink', j_ink({'특허법': {'tots': []}}), False)
    chk('빈 값 j_nochar', j_nochar({}), False)
    chk('빈 값 j_head_digits', j_head_digits({'특허법': {'tots': [_tot('unit', '3')]}}), False)
    # nums
    chk('nums 옛', nums({'t': '총 554문제'}), (554,))
    chk('nums 새', nums({'t': '554'}), (554,))
    chk('nums 회차', nums({'t': '20문항 · 98지문'}), (20, 98))
    # 줄 높이
    rn, rb = [_row('u', 'a', 33), _row('u', 'b', 33)], [_row('u', 'a', 33), _row('u', 'b', 33)]
    chk('h 같음', h_ok(h_cmp(rn, rb)), True)
    rn2 = [_row('u', 'a', 33), _row('u', 'b', 50)]
    chk('h 1 넘게 높아짐', h_ok(h_cmp(rn2, rb)), False)
    rb2 = [_row('u', 'a', 33), _row('u', 'b', 50)]
    chk('h 낮아짐(기본 = 허용)', h_ok(h_cmp(rn, rb2)), True)
    chk('h 낮아짐(--strict-h = 거짓)', h_ok(h_cmp(rn, rb2), True), False)
    chk('h 1px 이내', h_ok(h_cmp([_row('u', 'a', 33.8)], [_row('u', 'a', 33)]), True), True)
    chk('h 이름 다름 = 거짓', h_ok(h_cmp([_row('u', 'a', 33)], [_row('u', 'z', 33)])), False)
    chk('h 줄 수 다름 = 거짓', h_ok(h_cmp(rn, rb[:1])), False)
    chk('h 빈 = 거짓', h_ok(h_cmp([], [])), False)
    chk('h_all_ok 두 법 하나 틀림', h_all_ok({'특허법': h_cmp(rn, rb), '상표법': h_cmp(rn2, rb)}), False)
    # 넘침 · ewmn
    chk('over 0', j_over(new, 390), True)
    n7 = json.loads(json.dumps(new)); n7['특허법']['over'] = {'sw': 420, 'iw': 390}
    chk('over 넘침', j_over(n7, 390), False)
    chk('ewmn 같음', j_ewmn_same(new, old), True)
    n8 = json.loads(json.dumps(new)); n8['특허법']['ewmn'] = []
    chk('ewmn 사라짐', j_ewmn_same(n8, old), False)
    # 소스 자리(가짜 글 — 일곱 자리 · A-2 자리 셋 · tot 색)
    tail = "el('span','qltot','총 '+total+'문제') 번 / 총 ' + list.length + '문제' ' / 총 ' + z"
    s7 = ("el('span', 'tot', '총 ' + a + '문제') " * 4) + ("x.textContent = '총 ' + b + '문제' " * 3) + ".mbur>.l .tot{font-size:11px;font-weight:600;color:var(--exc);l} " + tail
    s0 = ("el('span', 'tot', String(a)) " * 4) + ("x.textContent = String(b) " * 3) + ".mbur>.l .tot{font-size:11px;font-weight:600;color:var(--ink);l} " + tail
    chk('소스 census 새 = 0 · 바탕 = 7', src_census(s0, s7)[0], True)
    chk('소스 census 새 = 바탕(안 고침) = 거짓', src_census(s7, s7)[0], False)
    chk('소스 census 일곱 중 하나 남음 = 거짓', src_census(s0 + " el('span', 'tot', '총 ' + q + '문제')", s7)[0], False)
    chk('소스 census A-2 자리(qltot)까지 고침 = 거짓', src_census(s0.replace("el('span','qltot','총 '+total+'문제')", "el('span','qltot',String(total))"), s7)[0], False)
    chk('소스 census 색 안 바꿈 = 거짓', src_census(s0.replace('var(--ink)', 'var(--exc)'), s7)[0], False)
    print('selftest %s — 어긋남 %d' % ('OK' if not bad else 'NG', len(bad)))
    return 0 if not bad else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    if '--dump-js' in sys.argv:
        open(ARG('--dump-js'), 'w', encoding='utf-8', newline='\n').write(A1JS + '\n')
        print('A1JS →', ARG('--dump-js'))
        sys.exit(0)
    sys.exit(main())
