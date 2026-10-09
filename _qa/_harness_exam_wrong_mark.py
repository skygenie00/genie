# -*- coding: utf-8 -*-
r"""_task_exam_wrong_mark §C 관문 — 실제 1차 시험(61·63회)에서 틀린 문제 「<회>-<번>-X」 · 조판기 · 민법OX · 자과

  python _harness_exam_wrong_mark.py [--jo <앱|판>] [--mb <앱|판>] [--jg <앱|판>] [--base afd6339] [--apps jo,mb,jg] [--fx <시험 기록>]
        [--eng chromium,webkit] [--only C1,C2-jo,..] [--res <결과(기본 = 임시 폴더)>] [--yardstick]
        [--vendor <cdnjs 사본(/ajax/libs/ 뒤 꼴)>] [--exam <시험지 폴더>] [--tw <Tailwind CSS 사본>]

  시험 기록 = _qa/jopangi/task/_fx_exam_mark/exam_꼬까.json(지어낸 값 · 세 앱 같은 한 벌 · 진짜 기록도 한 파일) — 가짜 원격이 studyplandata exam/꼬까.json 자리에 준다.
    ⚠ 진짜 기록(SPD exam/꼬까.json)은 이 하네스가 열지 않는다 — 가짜 원격이 그 자리를 시험 기록 · 404 둘로만 대답한다.
  관문(§C):
    C1 표시 수 — 앱마다 틀림 줄이 짝지은 지문(문제) 수를 하네스가 데이터에서 따로 세어 앱 표(ewmMap · ewmIdx · ewmOf)와 맞대고
       화면(기출뷰 해마다 · 쪽 전부 / 자과 문제 창)의 표시 수와 맞댐 · ok true · 화학 · 지운 회차 · 2차 · 점수만 회차 = 0
    C2 펼침 글 · 꼴 — 「내 답 · 정답 · 평균 정답률」 셋만(앞 회·번 · 뒤 출처·메모 없음) · 접힘 11px 800 #dc2626 글자만(바탕·테두리 없음) ·
       펼침 줄 = 조판기 H7 .qsub 계산값(10.5px · #8a867d · margin 2px 0 4px · padding-left 4px) · 밑줄 표본 6(+ 정답 둘 ④⑤) · 다시 누르면 접힘
    C3 자리 전수 표 — 자리마다 표본 1 → 표시 있음 · 누름 칸 겹침 0(표시 ↔ 이웃 칩 상자 겹침 0 · 서로 가운데 누름이 제 것) · 진짜 누름(PC 마우스 ·
       폰 390 · iPad 834 손가락)으로 펼침 · 다시 누르면 접힘
    C4 기록 못 받음(토큰 없음 · 404) = 표시 0 · 오류 0 · 기록이 늦게 와도(5초) 첫 화면이 먼저(바탕과 첫 화면 시각 맞댐) · 오면 펴 둔 화면에 저절로 붙음
    C5 회귀(규칙 57) = 이 하네스 밖(세 앱 건드린 화면 하네스를 바탕 afd6339 먼저) — 결과는 인도 글
  헛잣대 = --yardstick : 세 앱 자리에 바탕(afd6339) + 같은 시험 기록 → C1~C3 칸마다 FAIL 해야 통과 · C4 = 바탕엔 표시가 없어 가를 수 없음(해당 없음)
  도구 = 조판기 _qa/jopangi/task/_harness_jo_sp_view4(+ revfix0929b 서버 · SEED · 기기) · 자과 _qa/jagwa/moolri/_harness_jagwa_physphone(가짜 원격 · 기기 · 손가락)
    조판기 시험 데이터 = sp_view4 덧판(jo/data + _fx_sp_view4) 위에 상표 단원 하나(2.3 · 61회 22번 책 줄 = 리담에 없음 · 63회 24번 같은 uid 책 줄 · 63회 30번 문항째 카드 — 지어낸 글)
  자리 = _roots(GENIE_ROOT · SPD_ROOT) — 민법 문항 = SPD minbeop/문항마스터.json · 자과 생물·지학 = SPD(읽기만 · 쪽 안에서만 · 결과엔 ID 만)
  클라우드 = cdn 막힘 → --vendor(cdnjs 사본) · --tw(민법 Tailwind — 앱이 쓰는 클래스를 Tailwind v3 로 미리 구운 CSS · 없으면 cdn.tailwindcss.com 그대로)
  WebKit = 터치 칸(C3 폰 · iPad)만 · 이 컴퓨터에 WebKit 이 없으면 「안 잼」

  ★ JG2 (uid_unify_add1 · 2026-10-04) — 자과 서랍 줄 · 첫 화면 목록 카드 · 목차 「지금 목록」 줄의 「<회>-<번>-X」(클래스 .ewmt · 글자만 · 누름 없음)
    위 C1~C4 는 그대로 — 더한 칸 JG2-B1 ~ JG2-B5 · 이 칸만 = --only JG2(JG2-B1 처럼 하나만도) · 앱만 = --apps jg --eng chromium
      python _harness_exam_wrong_mark.py --apps jg --eng chromium --only JG2 --jg <새 판 jagwa/index.html> [--jgbase 4754b1d] [--real <진짜 exam/꼬까.json 사본>]
    B1 지어낸 기록 · 세 자리(서랍 줄 · 목록 카드 · 문제를 연 뒤 지금 목록 줄) · 거르개 줄 0 · 자리 · 꼴 · 헛잣대(바탕에서 셋 다 0)
    B2 받기 늦음 — 응답을 잡아 둔 채 서랍 · 목록을 굴려 두고 풀어 줌(세 자리에 나타남 · 쪽 · 서랍 스크롤 자리 그대로) · 문제를 연 채 풀어 줌(지금 목록 줄) · 2초 늦춤 첫 화면 시각 바탕 ±10%
    B3 토큰 없음 · 404 = 표시 0 · 오류 0 · 알림 0 / B4 폭 1440 · 834 · 390(서랍 줄 높이 무변 · 카드 가로 넘침 0 · 표시 글자 위를 눌러도 그 문제가 열림) / B5 진짜 기록(--real · 읽기만 · 수만 적음)
    헛잣대 = --jgbase(기본 4754b1d = uid_unify ④ 앞 바탕 · ④ 가 서면 그 커밋으로) — --yardstick 이면 JG2 칸이 바탕을 새 판 자리에 놓고 저마다 FAIL 해야(B3 = 해당 없음)
    진짜 기록 먹이는 길 = 가짜 원격(XRemoteReal)이 api.github.com/…/contents/exam/꼬까.json 자리에 --real 파일 바이트를 줌(기본 SPD_ROOT\exam\꼬까.json · 읽기만 — SPD 클론에 쓰지도 · fetch · pull 도 안 함)
    ⚠ 목차 「지금 목록」(#trq)은 앱에서 #tree 의 hide 가 영영 안 벗겨져(죽은 길) 사용자 눈엔 안 보인다 — 줄 글자(DOM)로만 잰다 · 물리는 앱이 문제를 열어도 안 채움(B2 「문제를 연 채」 에서 잼)
  ★ JG2 add1 검수 고침(2026-10-04 · 본 세션이 가름 — 앱 결함이 아니라 잣대 쪽 · 칸 이름은 그대로 · 옛 줄은 주석으로 남김)
    B2 「첫 화면 시각」(10/5 · 사용자 「1,2 둘다 고쳐」) — 매 회 새 판을 먼저 열던 차례(새 판만 ≈300 ms 손해)를 몸풀기 두 쪽 + ABBA 6 회(판마다 여섯 · 채팅 10/5 11:0x)로 · 판정식 · 라벨 그대로
    B1 「표시 자리 · 꼴」 목록 카드 — 제목 칸(.sub)이 있는 줄 = 옛 잣대 그대로(표시 바로 뒤가 ★ 또는 .sub) · 제목 칸이 없는 줄(uid_unify §G-1 이 기출 uid 줄의 .sub 를 안 그린다 · 생물 · 지학) = 기출 칩(kindTag .tag.tg) 바로 뒤 · .meta 안
    B2 「늦게 오면」 — 크롬 = 쪽 스크롤 같음 또는 기준 카드 이동 ≤ 1px(크롬의 스크롤 고정이 위쪽 높이 변화를 scrollTop 으로 갚아 화면은 제자리 · 값 칸에 둘 다) · 값 칸에 위쪽 높이 변화 재기(참고 · 판정 아님)
      · WebKit 칸 = --jg2eng chromium,webkit(기본 chromium = 지금처럼 크롬만 · webkit 만 쓰면 그 칸만) — 스크롤 고정이 없어 scrollTop 같음이 증거가 못 되므로 기준 카드 이동 ≤ 1px 만으로 판정
    B3 「토큰 없음」 생물 · 지학 — 문항은 비공개 저장소에서 토큰으로 받아 IndexedDB 에 두는 과목이라 처음부터 토큰이 없으면 물리에 머문다 → 토큰 있게 한 번 열어 받아 둔 뒤 토큰만 지우고 다시 연다(조판기·민법 C4-mb 와 같은 길) · 물리 = 옛 길(처음부터 토큰 없음)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) 실행 모드: --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같다) · 새 갈래는 모두 `if QJ.REGRESS:` / `if QJ.GATE:` 안 · regress 는 조판기(jo) 실행에만
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import hashlib, io, json, os, re, statistics, subprocess, sys, tempfile, threading, time, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


BASE = ARG('--base', 'afd6339')
YARD = '--yardstick' in sys.argv
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
APPS = [x for x in (ARG('--apps', 'jo,mb,jg') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(tempfile.gettempdir(), 'h_ewm', '_harness_exam_wrong_mark_result.txt'))   # 기본 = 임시 폴더(_qa 에 결과를 쓰지 않는다)
FX = ARG('--fx', os.path.join(HERE, 'jopangi', 'task', '_fx_exam_mark', 'exam_꼬까.json'))
VEND = ARG('--vendor')
EXAM = ARG('--exam', _roots.genie('gichul', 'pdf'))
TWCSS = ARG('--tw')
SPD = _roots.spd()
TMP = os.path.join(tempfile.gettempdir(), 'h_ewm', 'p%d' % os.getpid())
os.makedirs(TMP, exist_ok=True)
REL = {'jo': 'jo/index.html', 'mb': 'minbeop/index.html', 'jg': 'jagwa/index.html'}
NEWA = {'jo': ARG('--jo', _roots.genie('jo', 'index.html')), 'mb': ARG('--mb', _roots.genie('minbeop', 'index.html')),
        'jg': ARG('--jg', _roots.genie('jagwa', 'index.html'))}
PHONE, PAD, PC = (390, 844), (834, 1194), (1440, 900)
DEVS = (('폰390', PHONE), ('iPad834', PAD), ('PC1440', PC))
NAME = {'jo': '조판기', 'mb': '민법OX', 'jg': '자과'}

# ── 도구 하네스 둘 — 저마다 제 인자를 sys.argv 에서 읽는다(돌릴 때만 갈아 끼우고 되돌림) ──
_argv = sys.argv[:]
if 'jo' in APPS:   # ★ _task_qa_slim2(10/8 · 본 세션 결정) — 조판기 도구(sp_view4 → revfix0929b · jo 데이터 읽기)는 --apps 에 jo 가 있을 때만 연다 · jo 가 있으면 옛 길 그대로(jo 사슬 gate 무변) · 민법 · 자과 사슬(--apps mb · jg)은 jo 도구를 안 쓴다(그 사슬 입력에서 jo 파일이 빠진다)
    sys.path.insert(0, os.path.join(HERE, 'jopangi', 'task'))
    sys.argv = [_argv[0]] + (['--vendor', os.path.join(VEND, 'pdf.js', '3.11.174')] if VEND else []) + ['--exam', EXAM]
    import _harness_jo_sp_view4 as SV   # noqa: E402
sys.path.insert(0, os.path.join(HERE, 'jagwa', 'moolri'))
JG.conf(SPD_PP=SPD, **({'VENDOR_PP': VEND} if VEND else {}))   # 옛 PP import 때 가린 argv(--vendor VEND · --spd SPD)와 같은 값을 JG 에 넘김
sys.argv = _argv
if 'jo' in APPS:   # jo 도구를 열었을 때만(위)
    H = SV.H


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(app, x):
    """앱 글 — 파일이면 그 파일 · 아니면 genie git 판의 그 앱"""
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':' + REL[app])
    if not b:
        raise SystemExit('앱을 못 읽었다: %s %s' % (app, x))
    return b.decode('utf-8')


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


RES = []


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, d[:700]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str)
    print('INFO | %s · %s | %s' % (g, name, d[:1200]), flush=True)


# ════════════════════════ 시험 기록(지어낸 값) · 거르기 — 앱과 따로 하네스가 센다 ════════════════════════
EXJ = json.load(io.open(FX, encoding='utf-8'))
EXB = open(FX, 'rb').read()


def ex_rows(j):
    """틀림 줄(cha 1 · mode q · del 아님 · ok === false · 화학 뺌) · 뺀 줄(까닭)"""
    keep, drop = [], []
    for it in (j or {}).get('items') or []:
        m = re.match(r'\d+', str(it.get('id') or ''))
        r = int(it.get('no') or 0) or (int(m.group(0)) if m else 0)
        why = '2차' if it.get('cha') != 1 else ('점수만' if it.get('mode') != 'q' else ('지운 회차' if it.get('del') else ''))
        for x in it.get('q') or []:
            w = why or ('맞힘' if x.get('ok') is not False else ('화학' if str(x.get('s')) == '화학' else ''))
            row = {'r': r, 's': str(x.get('s')), 'i': int(x.get('i')), 'my': str(x.get('my', '')), 'ans': str(x.get('ans', '')), 'rate': x.get('rate')}
            if w:
                row['why'] = w
                drop.append(row)
            else:
                keep.append(row)
    return keep, drop


WR, WX = ex_rows(EXJ)
CIR = '①②③④⑤⑥⑦⑧⑨'


def circ(v):
    a = [t for t in re.split(r'[,\s]+', str(v or '')) if t]
    return ''.join(CIR[int(t) - 1] if re.fullmatch(r'[1-9]', t) else t for t in a) if a else '—'


def ratef(v):
    try:
        return '%.1f%%' % float(v)
    except Exception:
        return '—'


def line_of(x):
    return '내 답 %s · 정답 %s · 평균 정답률 %s' % (circ(x['my']), circ(x['ans']), ratef(x['rate']))


def lab_of(x):
    return '%d-%d-X' % (x['r'], x['i'])


def row_of(s, r, i):
    return next((x for x in WR if x['s'] == s and x['r'] == r and x['i'] == i), None)


MARK_CSS = {'fs': '11px', 'fw': '800', 'c': 'rgb(220, 38, 38)', 'bg': 'rgba(0, 0, 0, 0)', 'bw': '0px 0px 0px 0px', 'sh': 'none'}
QSUB = {'fs': '10.5px', 'c': 'rgb(138, 134, 125)', 'm': '2px 0px 4px 0px', 'pl': '4px'}   # 조판기 H7 .qsub(869줄) — 조판기 칸에서 계산값으로 다시 잰다


def css_ok(got, want):
    return bool(got) and all(str(got.get(k)) == str(v) for k, v in want.items())


# ── 쪽 첫머리(앱 스크립트보다 먼저) — 첫 화면 시각 · 시험 기록 늦추기(쪽 안 fetch · 다른 요청은 안 막음) · 오류 · 알림 셈 ──
PROBE = r"""<script>/* exam_wrong_mark 하네스 */(function(){ var D = __D__, READY = __R__;
 var H = window.__ewmH = { t1: 0, tEx: 0, nEx: 0, alerts: 0, errs: [] };
 window.addEventListener('error', function(e){ H.errs.push(String(e.message || '').slice(0, 160)); });
 window.addEventListener('unhandledrejection', function(e){ H.errs.push('reject: ' + String((e.reason && e.reason.message) || e.reason).slice(0, 160)); });
 var of = window.fetch;
 window.fetch = function(u, o){ var s = String((u && u.url) || u), d = s; try{ d = decodeURIComponent(s); }catch(e){}
   if (/exam\/꼬까\.json/.test(d)){ H.nEx++; var go = function(){ return of.call(window, u, o).then(function(r){ H.tEx = performance.now(); return r; }, function(e){ H.tEx = performance.now(); throw e; }); };
     return D ? new Promise(function(res){ setTimeout(res, D); }).then(go) : go(); }
   return of.apply(window, arguments); };
 var iv = setInterval(function(){ try{ if (!H.t1 && READY()){ H.t1 = performance.now(); clearInterval(iv); } }catch(e){} }, 20);
 window.alert = function(){ H.alerts++; };
})();</script>"""
READY = {'jo': "function(){ return !!document.querySelector('#slot .main, #slot .mbdash'); }",
         'mb': "function(){ return typeof quizData !== 'undefined' && quizData.length > 0 && !!document.querySelector('#dashboard-container > *'); }",
         'jg': "function(){ return typeof DATA !== 'undefined' && DATA.length > 0 && document.querySelectorAll('#list .item').length > 0; }"}


def with_probe(app, src, delay=0):
    b = src.index('<body')
    bb = src.index('>', b) + 1
    return src[:bb] + PROBE.replace('__D__', str(int(delay))).replace('__R__', READY[app]) + src[bb:]


# ── 쪽 도구(세 앱 공통 · 표시 · 이웃 · 펼침 줄) ──
EW = r"""() => { if (window.__EW) return 1;
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const R = e => { const r = e.getBoundingClientRect(); return { l: r.left, t: r.top, r: r.right, b: r.bottom, w: r.width, h: r.height, cx: r.left + r.width / 2, cy: r.top + r.height / 2 }; };
const on = (e, x, y) => { const a = document.elementFromPoint(x, y); return !!a && (a === e || e.contains(a)); };
const ov = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const KS = '[data-uzk],[data-jnrow],[id^="qb-"],[id^="jp-"],[id^="q-box-"],.qp2,#view,.oxwin';
const kOf = e => { const k = e.closest(KS); return k ? (k.dataset.uzk || k.dataset.jnrow || (k.id ? k.id.replace(/^(qb-|jp-|q-box-|oxwin-)/, '') : '') || k.className) : ''; };
window.__EW = {
  txt: txt, R: R, vis: vis,
  marks: sel => [...document.querySelectorAll((sel || '') + ' .ewmx')].filter(e => !e.classList.contains('cfhc') && vis(e)),
  list: sel => __EW.marks(sel).map(e => ({ t: txt(e), ewm: e.dataset.ewm || '', k: kOf(e) })),
  copies: sel => [...document.querySelectorAll((sel || '') + ' .ewmx.cfhc')].filter(vis).map(txt),
  cssOf: e => { if (!e) return null; const s = getComputedStyle(e); return { fs: s.fontSize, fw: s.fontWeight, c: s.color, bg: s.backgroundColor, bw: [s.borderTopWidth, s.borderRightWidth, s.borderBottomWidth, s.borderLeftWidth].join(' '), sh: s.boxShadow,
      m: [s.marginTop, s.marginRight, s.marginBottom, s.marginLeft].join(' '), pl: s.paddingLeft, td: s.textDecorationLine }; },
  hitOf: e => { if (!e) return null; try { e.scrollIntoView({ block: 'center', inline: 'nearest' }); } catch (x) {} const r = R(e); return Object.assign(r, { on: on(e, r.cx, r.cy) && r.cx > 0 && r.cy > 0 && r.cx < innerWidth && r.cy < innerHeight, t: txt(e) }); },
  /* 이웃 — 표시 바로 앞(출제연도 칩 · 앞 표시)·뒤 요소 + 같은 줄의 누를 것(머리 단추) · 상자 겹침 넓이 · 서로 가운데 누름이 제 것인지 */
  nbr: (e, extra) => { const me = R(e); const xs = [e.previousElementSibling, e.nextElementSibling].concat(extra ? [...document.querySelectorAll(extra)] : []);
    return [...new Set(xs)].filter(x => x && x !== e && !x.contains(e) && vis(x)).map(x => { const r = R(x); return { cls: String(x.className || x.id || x.tagName).slice(0, 40), t: txt(x).slice(0, 16),
      ov: Math.round(ov(me, r) * 10) / 10, own: on(x, r.cx, r.cy), meOwn: on(e, me.cx, me.cy),
      at: on(x, r.cx, r.cy) ? '' : (a => a ? String(a.className || a.tagName).slice(0, 30) : 'null')(document.elementFromPoint(r.cx, r.cy)) }; }); },
  lines: sel => [...document.querySelectorAll((sel || '') + ' .ewml')].filter(vis).map(l => ({ t: txt(l), u: [...l.querySelectorAll('u, .u')].map(txt),
      prev: l.previousElementSibling ? String(l.previousElementSibling.className || l.previousElementSibling.id || l.previousElementSibling.tagName).slice(0, 40) : String((l.parentElement || {}).id || ''),
      css: __EW.cssOf(l) })),
  find: (sel, ewm, k) => __EW.marks(sel).find(e => (!ewm || e.dataset.ewm === ewm) && (!k || kOf(e) === k)) || null,
  pick: (sel, ewm, k) => { const e = __EW.find(sel, ewm, k); if (!e) return null; document.querySelectorAll('.ewmx[data-ewpick]').forEach(x => x.removeAttribute('data-ewpick')); e.setAttribute('data-ewpick', '1'); return __EW.hitOf(e); },
  picked: () => document.querySelector('.ewmx[data-ewpick]'),
  /* 굴림이 멎을 때까지(앱 「↪ 이동」 = 부드러운 굴림) — 고른 표시 자리가 0.1초 셋 잇달아 같으면 그 자리 */
  settle: async () => { const e = __EW.picked(); if (!e) return null; let last = '', same = 0;
    for (let i = 0; i < 60 && same < 3; i++){ await new Promise(r => setTimeout(r, 100)); const r = e.getBoundingClientRect(), k = Math.round(r.left) + ',' + Math.round(r.top); if (k === last) same++; else { same = 0; last = k; } }
    return __EW.hitOf(e); }
};
return 1; }"""


def ew(p):
    p.ev(EW)


def press_at(p, at, wait=500):
    if not at or not at.get('on'):
        return False
    (p.tap if p.touch else p.click)(at['cx'], at['cy'], wait)
    return True


def nb_ok(nb):
    return bool(nb) and all(x['ov'] <= 0.5 and x['own'] and x['meOwn'] for x in nb)


def until(p, js, ms=15000, step=200, arg=None):
    t0 = time.time()
    v = None
    while time.time() - t0 < ms / 1000.0:
        try:
            v = p.ev(js, arg) if arg is not None else p.ev(js)
        except Exception:
            v = None
        if v:
            return v
        p.wait(step)
    return v


EWM_ST = "() => typeof EWM === 'undefined' ? '정의 없음' : EWM.st"


def ewm_wait(p, ms=15000):
    t0 = time.time()
    st = None
    while time.time() - t0 < ms / 1000.0:
        st = p.ev(EWM_ST)
        if st in ('ok', 'fail', 'none', '정의 없음'):
            return st
        p.wait(200)
    return st


# ════════════════════════ 조판기 — 시험 데이터 덧판 · 기대값 ════════════════════════
LAWS = ('특허법', '상표법', '디자인보호법')
LAWN = {'특허': '특허법', '상표': '상표법', '디보': '디자인보호법'}
SHORT = {'특허법': '특허', '상표법': '상표', '디자인보호법': '디보'}
JO_LAWL = {'T': '특허법', 'S': '상표법', 'D': '디자인보호법'}
JO_UNIT = 'S008'


def jo_parse_uid(u):
    """앱 jxeParseUid 의 두 꼴(선지 지문 · 객관식 문항 열쇠) — 해(회 + 1963) · 번"""
    u = str(u or '')
    m = re.match(r'^([TSD])(\d{2})(\d{2})(\d{2})([1-7ㄱ-ㅅ가-사])(?:[hr]\d?)?$', u) or re.match(r'^([TSD])(\d{2})(\d{2})(\d{2})$', u)
    return (JO_LAWL[m.group(1)], 1963 + int(m.group(3)), int(m.group(4))) if m else None


def _jo_book_rows():
    """책 줄(덧판) — 상표 뷰객 시험 + 이 관문 단원(2.3) · 지어낸 글"""
    fj = json.loads(json.dumps(SV.FXJ, ensure_ascii=False))
    fm = json.loads(json.dumps(SV.FXM, ensure_ascii=False))
    q24 = next(q for q in SV.JMS['문제'] if str(q.get('연도')) == '2026' and str(q.get('시험문번')) == '24')
    add, ids = [], []
    for n in range(1, 6):   # 상표 61회 22번 — 리담에 없음 · 책 지문만(uid = 시험 꼴 · 태그 「24 변리」)
        r = {'id': 'V4-C3-S2-%d' % n, 'uid': 'S246122%d' % n, 't': '시험 선지 E22-%d — (지어낸 글) 시험 부등록 사유 문장 %d' % (n, n),
             'sol': '시험 해설 E22-%d — 지어낸 글.' % n, '쪽': '140', 'pdf쪽': '150', '태그': '24 변리', '연도들': ['2024'], '책번호': 'C3-S2',
             'ox': 'X' if n == 3 else 'O', '유제': False, '배지': '기출', '순': 60 + n, '판': 'V4', '단원': JO_UNIT, '문항': 'V4-C3-S2', '선지': n,
             '사례': '시험 발문 E22 — 다음 중 옳지 않은 것은?(지어낸 글)'}
        add.append(r)
    for n, z in enumerate(q24.get('지문') or [], 1):   # 상표 63회 24번 — 리담과 같은 uid 책 줄(병합)
        r = {'id': 'V4-C3-S3-%d' % n, 'uid': z['uid'], 't': '시험 선지 E24-%d — (지어낸 글) 시험 상표 문장 %d' % (n, n),
             'sol': '시험 해설 E24-%d — 지어낸 글.' % n, '쪽': '141', 'pdf쪽': '151', '태그': '26 변리', '연도들': ['2026'], '책번호': 'C3-S3',
             'ox': str(z.get('ox') or 'O'), '유제': False, '배지': '기출', '순': 70 + n, '판': 'V4', '단원': JO_UNIT, '문항': 'V4-C3-S3', '선지': n,
             '사례': '시험 발문 E24 — 다음 중 옳지 않은 것은?(지어낸 글)', '병합': 'Y',
             '리담': {'연도': '2026', '문항': str(q24.get('문번')), '선지': str(n), 'ox': str(z.get('ox') or 'O')}}
        add.append(r)
    obj = {'id': 'V4-C3-S9', 'uid': 'S266330', 't': '시험 문항째 카드 E30 — 다음 중 옳은 것은?(지어낸 글)\n① 시험 선지 하나\n② 시험 선지 둘\n③ 시험 선지 셋\n④ 시험 선지 넷\n⑤ 시험 선지 다섯',
           'sol': '시험 해설 E30 — 지어낸 글.', '쪽': '142', 'pdf쪽': '152', '태그': '26 변리', '연도들': ['2026'], '책번호': 'C3-S9', '답': '①',
           '종류': '옳은', '판': 'V4', '유형태그': [], '단원': JO_UNIT}
    fj['지문'] += add
    fj.setdefault('객관식', []).append(obj)
    fj['건수'] = len(fj['지문'])
    yi = fj.setdefault('연도색인', {})
    yi.setdefault('2024', []).extend([r['id'] for r in add if r['연도들'] == ['2024']])
    yi.setdefault('2026', []).extend([r['id'] for r in add if r['연도들'] == ['2026']])
    ids = [r['id'] for r in add] + [obj['id']]
    at = next(i for i, n in enumerate(fm['마디']) if n['id'] == 'S007') + 1
    fm['마디'].insert(at, {'id': JO_UNIT, 'no': '2.3', '제목': '시험 단원 — 틀린 문제 표시', '깊이': 2, '장': False, '출처': 'OMR',
                          '지문': ids, '리담': ['2026-63-4'], '조': [], '소제목': []})
    return fj, fm, at


if 'jo' in APPS:   # 조판기 시험 덧판 — jo 도구가 있을 때만(위)
    JO_FJ, JO_FM, JO_UNIT_IX = _jo_book_rows()


def jo_overlay():
    d = os.path.join(TMP, 'jo_data')
    if os.path.isdir(d):
        return d
    os.makedirs(d)
    for x in os.listdir(SV.DATA0):
        if x in SV.FX_FILES:
            continue
        SV._ln(os.path.join(SV.DATA0, x), os.path.join(d, x))
    io.open(os.path.join(d, SV.FX_FILES[0]), 'w', encoding='utf-8').write(json.dumps(JO_FJ, ensure_ascii=False))
    io.open(os.path.join(d, SV.FX_FILES[1]), 'w', encoding='utf-8').write(json.dumps(JO_FM, ensure_ascii=False))
    return d


def jo_expect():
    """법마다 {열쇠: ['회-번', …]} · 리담 열쇠(기출뷰에 서는 지문) — 앱 규칙(리담 시험문번 · 책 줄 uid 꼴 · 문항째)을 하네스가 따로"""
    exp = {law: {} for law in LAWS}
    lid = {law: {} for law in LAWS}
    book = {'특허법': json.load(open(os.path.join(SV.DATA0, 'jimun_7pan.json'), encoding='utf-8')), '상표법': JO_FJ, '디자인보호법': {'지문': [], '객관식': []}}
    for law in LAWS:
        jm = json.load(open(os.path.join(SV.DATA0, 'jimun_%s.json' % SHORT[law]), encoding='utf-8'))
        for x in WR:
            if LAWN.get(x['s']) != law:
                continue
            y, ri = x['r'] + 1963, '%d-%d' % (x['r'], x['i'])
            for q in jm['문제']:
                if str(q.get('연도')) == str(y) and str(q.get('시험문번')) == str(x['i']):
                    for z in q.get('지문') or []:
                        k = z.get('uid') or ('L:%s:%s' % (q['id'], z.get('n')))
                        exp[law].setdefault(k, [])
                        if ri not in exp[law][k]:
                            exp[law][k].append(ri)
                        lid[law][k] = y
            for z in (book[law].get('지문') or []) + (book[law].get('객관식') or []):
                pu = jo_parse_uid(z.get('uid'))
                if pu and pu[0] == law and pu[1] == y and pu[2] == x['i']:
                    k = z.get('uid') or ('P7:' + z['id'])
                    exp[law].setdefault(k, [])
                    if ri not in exp[law][k]:
                        exp[law][k].append(ri)
    return exp, lid


EXAM_MODE = {'m': 'ok'}
if 'jo' in APPS:   # 조판기 가짜 원격 갈아 끼우기 — jo 도구가 있을 때만(위)
    _jo_clear0 = SV.REMOTE.clear


def _jo_clear():
    _jo_clear0()
    if EXAM_MODE['m'] == 'ok':
        with SV.REMOTE.lock:
            SV.REMOTE.files['exam/꼬까.json'] = EXB   # 가짜 원격 — 시험 기록(지어낸 값) · 404 면 안 넣는다


if 'jo' in APPS:   # 조판기 가짜 원격 갈아 끼우기 — jo 도구가 있을 때만(위)
    SV.REMOTE.clear = _jo_clear
NO_TOKEN = {'tt.cfg': json.dumps({'person': '꼬까'})}
_TAGN = [0]


def ntag(pre):
    _TAGN[0] += 1
    return '%s%d' % (pre, _TAGN[0])


def jo_open(br, src, dev=PC, ls=None, delay=0, mode='ok'):
    QJ.launch('new')
    EXAM_MODE['m'] = mode
    tag = ntag('ewj')
    SV.DATA_FOR[tag] = jo_overlay()
    p = SV.open_pg(br, with_probe('jo', src, delay), dev, tag, ls)
    ew(p)
    return p


JO_EXV = r"""async ([law, y]) => { const w = ms => new Promise(r => setTimeout(r, ms)); try{ closeAllPops(); }catch(e){}
  S.law = law; S.tab = 'jimun'; S.exvPg = S.exvPg || {}; S.exvPg[PLAW() + ':' + y] = 0; mbGiGo(y);
  for (let i = 0; i < 150 && !document.querySelector('#slot .exv-q'); i++) await w(100);
  for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await w(100);
  const n = (typeof MBHEAD !== 'undefined' && MBHEAD && MBHEAD.list) ? MBHEAD.list.length : 0, nPg = Math.max(1, Math.ceil(n / 5)), pk = PLAW() + ':' + y, out = [];
  for (let pg = 0; pg < nPg; pg++){ S.exvPg[pk] = pg; await render(); for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await w(100); await w(200);
    { const ms = __EW.marks('#slot'), ls = __EW.list('#slot'); ls.forEach((m, j) => { const h = ms[j] && ms[j].closest('.exv-head'); if (h){ m.h = 1; m.no = (h.closest('.exv-q') || { dataset: {} }).dataset.exno || ''; } }); out.push(...ls); } }   /* ★ ewm_list J6(10/5) — 문항 머리 표시(.exv-head)는 h · 그 문항 번호 no(옛 줄: out.push(...__EW.list('#slot'))) */
  S.exvPg[pk] = 0; await render(); await w(200);
  const nos = ((typeof MBHEAD !== 'undefined' && MBHEAD && MBHEAD.list) || []).map(q => { try{ return String(giNo(q)); }catch(e){ return ''; } });   /* ★ ewm_list J6(10/5) — 그 해 기출뷰에 선 문항 번호 */
  return { n: n, nPg: nPg, marks: out, nos: nos, boxes: document.querySelectorAll('#slot .uzexb').length }; }"""
JO_EXV_GO = r"""async ([law, y, k]) => { const w = ms => new Promise(r => setTimeout(r, ms)); try{ closeAllPops(); }catch(e){}
  S.law = law; S.tab = 'jimun'; S.exvPg = S.exvPg || {}; mbGiGo(y);
  for (let i = 0; i < 150 && !document.querySelector('#slot .exv-q'); i++) await w(100);
  for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await w(100);
  const list = (typeof MBHEAD !== 'undefined' && MBHEAD && MBHEAD.list) || []; const pk = PLAW() + ':' + y;
  const ix = list.findIndex(q => (q.지문 || []).some(z => oxKeyLid(q, z) === k)); S.exvPg[pk] = ix >= 0 ? Math.floor(ix / 5) : 0; await render();
  for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await w(100); await w(300);
  return !!document.getElementById('exb-' + k); }"""
JO_MAP = r"""async (law) => { const w = ms => new Promise(r => setTimeout(r, ms)); try{ closeAllPops(); }catch(e){}
  if (typeof ewmMap !== 'function') return null; S.law = law; S.tab = 'jimun'; S.jimunTab = 'ox'; S.oxQueue = ''; S.mok = null; await render();
  try{ await jpMlnReady(); }catch(e){} for (let i = 0; i < 50 && !(MLN && MLN.ok); i++) await w(100);
  const m = ewmMap(); const o = {}; Object.keys(m).forEach(k => { o[k] = m[k].map(x => x.r + '-' + x.i).sort(); }); return o; }"""


def jo_c1(br, src, tag):
    exp, lid = jo_expect()
    ok = True
    p = jo_open(br, src)
    try:
        st = ewm_wait(p)
        N('C1-jo', '시험 기록 받음', {'EWM.st': st, '틀림 줄(하네스)': len(WR), '뺀 줄(까닭)': sorted(set(x['why'] for x in WX))})
        # ★ ewm_list J6(10/5 · _task_ewm_list.md J6) — 이 판 앱은 ewmMap 에 문항 열쇠 'Q|해|번'(그 법 틀림 줄마다 · 기출뷰 문항 머리 표시용)을 세운다 · 옛 앱(바탕)엔 없음 = 옛 잣대 그대로
        HASQ = bool(p.ev("() => typeof ewmMap === 'function' && String(ewmMap).indexOf(\"'Q|'\") >= 0"))
        for law in LAWS:
            got = p.ev(JO_MAP, law)
            want = {k: sorted(v) for k, v in exp[law].items()}
            wq = {}
            if HASQ:
                for x in WR:
                    if LAWN.get(x['s']) == law:
                        wq.setdefault('Q|%d|%d' % (x['r'] + 1963, x['i']), set()).add('%d-%d' % (x['r'], x['i']))
                want.update({k: sorted(v) for k, v in wq.items()})
            ok &= T('C1-jo', '%s 앱 표 = 하네스 셈(열쇠 %d · 표시 %d)' % (SHORT[law], len(want), sum(len(v) for v in want.values())),
                    got == want, {'앱': None if got is None else {'열쇠': len(got), '다른 것': sorted(set(got) ^ set(want))[:8]}, '하네스': sorted(want)[:12], '문항 열쇠': len(wq)})
        if QJ.want('C1-jo-기출뷰'):   # smoke 칸 아님(smoke = 위 앱 표 셋)
            # 화면 — 연도별 기출뷰(해마다 · 쪽 전부) · 리담 지문 하나 = 표시 하나(그 해 틀림 줄)
            cases = [('특허법', '2024'), ('특허법', '2026'), ('특허법', '2025'), ('특허법', '2023'), ('상표법', '2024'), ('상표법', '2026'), ('디자인보호법', '2026')]
            for law, y in cases:
                r = p.ev(JO_EXV, [law, y]) or {}
                marks = r.get('marks') or []
                want = sorted('%s|%s' % (k, ri) for k, v in exp[law].items() if k in lid[law] and lid[law][k] == int(y) for ri in v)
                # ★ ewm_list J6(10/5) — 문항 머리(.exv-head) 표시는 따로: 이 판 앱 = 그 해 기출뷰에 선 틀린 문항마다 하나(「번|회-번」) · 옛 앱 = 0
                heads = [m for m in marks if m.get('h')]
                body = [m for m in marks if not m.get('h')]
                nos = set(r.get('nos') or [])
                wantH = sorted(set('%d|%d-%d' % (x['i'], x['r'], x['i']) for x in WR if LAWN.get(x['s']) == law and x['r'] + 1963 == int(y) and str(x['i']) in nos)) if HASQ else []
                gotH = sorted('%s|%s' % (m.get('no'), m['ewm']) for m in heads)
                gotk = sorted('%s|%s' % (m['k'], m['ewm']) for m in body)   # 옛 줄: for m in marks(머리 표시가 없던 앱)
                wtxt = sorted(set(w.split('|')[1] + '-X' for w in want))
                ok &= T('C1-jo', '기출뷰 %s %s — 표시 %d(기대 %d)' % (SHORT[law], y, len(marks), len(want) + len(wantH)),
                        gotk == want and gotH == wantH and r.get('n', 0) > 0, {'문항': r.get('n'), '쪽': r.get('nPg'), '글자': sorted(set(m['t'] for m in marks)), '기대 글자': wtxt,
                                                           '다른 것': sorted(set(gotk) ^ set(want))[:6], '머리': gotH, '기대 머리': wantH})
            excl = [x for x in WX if LAWN.get(x['s'])]
            N('C1-jo', '뺀 줄 — 위 기출뷰 2023(점수만) · 2025(지운 회차) 표시 0 · 2024 의 4번(맞힘)·6번(2차) 지문 = 표 밖', [(x['r'], x['s'], x['i'], x['why']) for x in excl])
        return ok
    finally:
        p.close()


def jo_line_case(p, law, y, k, want_t, want_u):
    """기출뷰 지문 k 의 표시를 마우스로 눌러 펼침 · 글 · 밑줄 · 자리 · 꼴 → 다시 누르면 접힘"""
    p.ev(JO_EXV_GO, [law, y, k])
    ew(p)
    at = p.ev("([k]) => __EW.pick('#exb-' + CSS.escape(k), '', '')", [k])
    if not press_at(p, at, 600):
        return {'press': False, 'at': at}
    ln = p.ev("([k]) => __EW.lines('#exb-' + CSS.escape(k))", [k]) or []
    mk = p.ev("() => __EW.cssOf(__EW.picked())")
    qs = p.ev(r"""([k]) => { const l = document.querySelector('#exb-' + CSS.escape(k) + ' .ewml'); if (!l) return null; const q = document.createElement('div'); q.className = 'qsub'; q.textContent = 'x';
      l.parentNode.insertBefore(q, l.nextSibling); const s = getComputedStyle(q), o = { fs: s.fontSize, c: s.color, m: [s.marginTop, s.marginRight, s.marginBottom, s.marginLeft].join(' '), pl: s.paddingLeft }; q.remove(); return o; }""", [k])
    at2 = p.ev("() => __EW.hitOf(__EW.picked())")
    press_at(p, at2, 500)
    ln2 = p.ev("([k]) => __EW.lines('#exb-' + CSS.escape(k))", [k]) or []
    one = ln[0] if len(ln) == 1 else None
    return {'press': True, 'n': len(ln), 't': one and one['t'], 'u': one and one['u'], 'prev': one and one['prev'], 'css': one and one['css'], 'mark': mk, 'qsub': qs, 'after': len(ln2),
            'ok': bool(one) and one['t'] == want_t and one['u'] == want_u and one['prev'].startswith('mbqhd') and len(ln2) == 0}


def jo_c2(br, src, tag):
    ok = True
    p = jo_open(br, src)
    try:
        ewm_wait(p)
        x3, x5, x35 = row_of('특허', 61, 3), row_of('특허', 63, 5), row_of('디보', 63, 35)
        L3 = line_of(x3)
        cases = [('특허법', '2024', 'T2461032', L3, ['내 답 ' + circ(x3['my'])], '내 답 선지(②)'),
                 ('특허법', '2024', 'T2461035', L3, ['정답 ' + circ(x3['ans'])], '정답 선지(⑤)'),
                 ('특허법', '2024', 'T2461031', L3, [], '둘 다 아님(①)'),
                 ('특허법', '2026', 'T266305ㄱ', line_of(x5), [], '보기 지문(ㄱ)'),
                 ('디자인보호법', '2026', 'D2663354', line_of(x35), ['정답 ' + circ(x35['ans'])], '정답 둘 ④⑤ 중 ④')]
        qsub = None
        for law, y, k, wt, wu, nm in cases:
            r = jo_line_case(p, law, y, k, wt, wu)
            ok &= T('C2-jo', '%s %s %s — 펼침 「%s」 밑줄 %s' % (SHORT[law], k, nm, wt, wu or '없음'), r.get('ok'), r)
            if r.get('css'):
                ok &= T('C2-jo', '%s 펼침 줄 꼴 = H7 .qsub 계산값 · 접힘 = 11px 800 빨강 글자만' % k,
                        css_ok(r['css'], r.get('qsub') or QSUB) and css_ok(r['css'], QSUB) and css_ok(r.get('mark'), MARK_CSS), {'펼침': r['css'], 'qsub': r.get('qsub'), '접힘': r.get('mark')})
                qsub = qsub or r.get('qsub')
        N('C2-jo', '조판기 .qsub 계산값(민법·자과 칸이 맞대는 값)', qsub)
        return ok
    finally:
        p.close()


# ── C3 조판기 자리 전수 표 ──
JO_CARDS = (('1차객 리담 카드 — 특허 61회 3번(제7판 병합 줄 같은 uid)', ['P', 'P7-0540', 'qb-T2461032', '특허법']),
            ('1차객 리담 카드 — 특허 63회 17번(제7판 P7-1818 같은 uid)', ['L', '2026-63-19', 'qb-T2663173', '특허법']),
            ('1차객 책 카드 — 상표 뷰객(리담에 없는 61회 22번)', ['P', 'V4-C3-S2-1', 'qb-S2461221', '상표법']),
            ('1차객 책 카드 — 상표 뷰객 · 리담 같은 uid(63회 24번)', ['P', 'V4-C3-S3-2', 'qb-S2663242', '상표법']),
            ('1차객 문항째 카드 — 상표(63회 30번)', ['P', 'V4-C3-S9', 'qb-S266330', '상표법']))
JO_GOTO = r"""async ([kind, id, dom, law]) => { try{ closeAllPops(); }catch(e){} await gotoJimun(kind, id, dom, '', law); await new Promise(r => setTimeout(r, 600));
  for (let i = 0; i < 100 && typeof busy !== 'undefined' && busy; i++) await new Promise(r => setTimeout(r, 100));
  const c = document.getElementById(dom); return c ? { mok: S.mok, bk: !!c.querySelector('.mbbk'), m: [...c.querySelectorAll('.ewmx')].filter(x => !x.classList.contains('cfhc')).map(x => x.textContent.trim()) } : { mok: S.mok, none: 1 }; }"""
JO_JP = r"""async ([sid]) => { const w = ms => new Promise(r => setTimeout(r, ms)); try{ closeAllPops(); }catch(e){}
  S.law = '특허법'; JOPANE = null; const J = await joPanelIdx();
  for (const k of Object.keys(J || {})){ const items = jsPanelItems(J[k], k); const ix = items.findIndex(it => it.sid === sid);
    if (ix >= 0){ S.tab = 'jo'; S.jo = k; S.joPanel = true; S.joPanelF = 'all'; S.joPanelP = Math.floor(ix / 5); await render(); await w(600); return { jo: k, page: S.joPanelP, card: !!document.getElementById('jp-' + sid) }; } }
  return null; }"""


def jo_place_check(p, sel, ewm, k, g, place, dev_name, nbr_extra=None, press=True):
    """자리 표본 하나 — 표시 있음 · 이웃 겹침 0 · 누름 → 펼침 → 다시 누름 → 접힘"""
    ew(p)
    at = p.ev("([s, e, k]) => __EW.pick(s, e, k)", [sel, ewm, k])
    if at:
        at = p.ev("() => __EW.settle()")
    n = len(p.ev("([s]) => __EW.list(s)", [sel]) or [])
    if not at:
        return {'자리': place, '기기': dev_name, '표시': n, 'ok': False, '왜': '표시 없음'}
    nb = p.ev("([x]) => __EW.nbr(__EW.picked(), x)", [nbr_extra]) or []
    r = {'자리': place, '기기': dev_name, '표시': n, '표본': at.get('t'), '보임': at.get('on'), '이웃': nb}
    if press:
        l0 = len(p.ev("() => __EW.lines('')") or [])
        press_at(p, at, 600)
        l1 = len(p.ev("() => __EW.lines('')") or [])
        at2 = p.ev("() => __EW.settle()")
        press_at(p, at2, 500)
        l2 = len(p.ev("() => __EW.lines('')") or [])
        r.update({'펼침': l1 - l0, '접힘': l2 - l0})
        r['ok'] = bool(at.get('on')) and nb_ok(nb) and l1 - l0 == 1 and l2 == l0
    else:
        r['ok'] = bool(at.get('on')) and nb_ok(nb)
    return r


def jo_c3_dev(br, src, dev_name, dev, census):
    ok = True
    p = jo_open(br, src, dev)
    try:
        ewm_wait(p)
        for place, args in JO_CARDS:   # 1차객 카드 넷 꼴 — 앱 「↪ 이동」 길(gotoJimun)로 그 카드 마디·거름·쪽
            g = p.ev(JO_GOTO, args) or {}
            r = jo_place_check(p, '#' + args[2], '', '', 'C3-jo', place, dev_name)
            r['마디'], r['책'] = g.get('mok'), g.get('bk')
            census.append(r)
            ok &= T('C3-jo', '%s %s' % (dev_name, place), r['ok'], r)
        # 연도별 기출뷰
        p.ev(JO_EXV_GO, ['특허법', '2024', 'T2461032'])
        r = jo_place_check(p, '#exb-T2461032', '', '', 'C3-jo', '연도별 기출뷰', dev_name)
        census.append(r)
        ok &= T('C3-jo', '%s 연도별 기출뷰' % dev_name, r['ok'], r)
        # 정리 창(연도) — jnxYearOpen
        p.ev("async () => { S.law = '특허법'; try{ closeAllPops(); }catch(e){} jnxYearOpen('2024'); await new Promise(r => setTimeout(r, 900)); return 1; }")
        r = jo_place_check(p, '.pop', '', 'T2461032', 'C3-jo', '정리 창(연도)', dev_name)
        census.append(r)
        ok &= T('C3-jo', '%s 정리 창(연도)' % dev_name, r['ok'], r)
        p.ev("() => { try{ closeAllPops(); }catch(e){} return 1; }")
        # 정오문제 창 — T2461032 가 걸린 조
        jp = p.ev(JO_JP, ['T2461032'])
        r = jo_place_check(p, '#jp-T2461032', '', '', 'C3-jo', '정오문제 창', dev_name) if jp and jp.get('card') else {'자리': '정오문제 창', '기기': dev_name, 'ok': False, '왜': '조 못 찾음', 'jp': jp}
        r['조'] = (jp or {}).get('jo')
        census.append(r)
        ok &= T('C3-jo', '%s 정오문제 창' % dev_name, r['ok'], r)
        p.ev("async () => { S.joPanel = false; S.tab = 'jimun'; try{ closeAllPops(); }catch(e){} await render(); return 1; }")
        # 문제 창 — popCard(출제연도 칩 없음 → ID 칩 바로 앞)
        p.ev("async () => { S.law = '특허법'; try{ closeAllPops(); }catch(e){} popCard('T2461032', null); await new Promise(r => setTimeout(r, 700)); return 1; }")
        r = jo_place_check(p, '.qp2', '', '', 'C3-jo', '문제 창', dev_name)
        census.append(r)
        ok &= T('C3-jo', '%s 문제 창' % dev_name, r['ok'], r)
        # 연결 창 머리(사본) — 문제 창의 「✏️ 연결」을 진짜로 눌러서
        at = p.ev("() => { const b = document.querySelector('.qp2 .qlk'); return b ? __EW.hitOf(b) : null; }")
        press_at(p, at, 900)
        cp = p.ev("() => __EW.copies('.pop.cflw')") or []
        r = {'자리': '연결 창 머리(사본)', '기기': dev_name, '표시': len(cp), '표본': cp[:2], 'ok': cp == [lab_of(row_of('특허', 61, 3))], '왜': '' if cp else ('사본 없음' if at and at.get('on') else '연결 단추 못 누름')}
        census.append(r)
        ok &= T('C3-jo', '%s 연결 창 머리(사본 · 누름 없음)' % dev_name, r['ok'], r)
        p.ev("() => { try{ closeAllPops(); }catch(e){} return 1; }")
        return ok
    finally:
        p.close()


def jo_c3(br, src, tag, census):
    ok = True
    for dn, dev in DEVS:
        ok &= jo_c3_dev(br, src, dn, dev, census)
    return ok


def jo_c4(br, src, base_src, tag):
    ok = True
    exv_n = "async () => { const r = await (%s)(['특허법', '2024']); return r ? r.marks.length : -1; }" % JO_EXV.strip()
    for nm, kw in (('토큰 없음', {'ls': NO_TOKEN}), ('404(기록 없음)', {'mode': '404'})):
        if QJ.SMOKE and nm != '토큰 없음':
            continue   # smoke = 토큰 없음 한 칸(표시 0 · 오류 0 · 알림 0)
        p = jo_open(br, src, **kw)
        try:
            st = ewm_wait(p)
            n = p.ev(exv_n)
            h = p.ev("() => window.__ewmH")
            ok &= T('C4-jo', '%s — 표시 0 · 오류 0 · 알림 0' % nm, n == 0 and not p.errs and not (h or {}).get('errs') and not (h or {}).get('alerts'),
                    {'EWM.st': st, '기출뷰 2024 특허 표시': n, '쪽 오류': p.errs[:3], 'h': h})
        finally:
            p.close()
    if QJ.want('C4-jo-나머지'):   # smoke 칸 아님(첫 화면 시각 · 늦게 와도)
        ok &= first_screen('jo', br, src, base_src, jo_open, 'C4-jo')
        # 늦게 와도(5초) — 펴 둔 기출뷰에 저절로
        p = jo_open(br, src, delay=5000)
        try:
            r0 = p.ev(exv_n)
            until(p, "() => window.__ewmH && window.__ewmH.tEx > 0", 12000)
            p.wait(1500)
            ew(p)
            n1 = len(p.ev("() => __EW.list('#slot')") or [])
            ok &= T('C4-jo', '기록이 5초 늦게 와도 — 펴 둔 기출뷰에 저절로 붙음', r0 == 0 and n1 > 0, {'오기 전': r0, '온 뒤(그 쪽)': n1})
        finally:
            p.close()
    return ok


def first_screen(app, br, src, base_src, opener, g, runs=3, delay=5000):
    """첫 화면 시각(쪽 첫머리 기준 · READY 가 처음 참이 된 때) — 새 판 · 바탕 번갈아 runs 번 · 시험 기록 5초 늦게 · 화면이 기록보다 먼저"""
    if QJ.REGRESS and app in ('jo', 'mb', 'jg'):   # ★ _task_qa_slim2(10/8) — 민법 · 자과 사슬도 regress(옛 줄: app == 'jo')
        runs = 1   # regress(jo) — 표본 1/3: 새 판만 1 번(바탕 판 부팅 3 번 · 새 판 2 번 뺌 — 한 번에 새 판은 기록 5초를 기다려 6 초 안팎)
    tn, tb, before = [], [], []
    for i in range(runs):
        for who, s, arr in ((('new', src, tn), ('base', base_src, tb)) if (QJ.GATE or app not in ('jo', 'mb', 'jg')) else (('new', src, tn),)):   # regress(jo · mb · jg) — 바탕 판은 안 띄운다
            QJ.launch(who)
            p = opener(br, s, delay=delay)
            try:
                h = until(p, "() => window.__ewmH && window.__ewmH.t1 > 0 ? window.__ewmH : null", 60000)
                arr.append(round((h or {}).get('t1') or 0))
                if who == 'new':
                    hh = until(p, "() => window.__ewmH && window.__ewmH.tEx > 0 ? window.__ewmH : null", 15000) or {}
                    before.append((round((h or {}).get('t1') or 0), round(hh.get('tEx') or 0)))
            finally:
                p.close()
    if QJ.GATE or app not in ('jo', 'mb', 'jg'):
        mn, mb = statistics.median(tn), statistics.median(tb)
    else:
        mn = statistics.median(tn)
        mb = QJ.base('C4-%s@first/mn' % app, mn)   # 바탕 중앙값 = 바탕 판 regress 가 남긴 기준 스냅샷(없으면 첫 기록 = 새 판 자신)
        tb = [mb]
    first = all(a > 0 and b > 0 and a < b for a, b in before)
    if QJ.REGRESS and app in ('jo', 'mb', 'jg'):
        before = before + ['(표본 1/3 · 새 판만 · 바탕 중앙값 = 기준 스냅샷 · %s)' % QJ.base_note('C4-%s@first/mn' % app)]
    return T(g, '첫 화면 시각 — 새 판 %dms · 바탕 %dms(중앙값 %d번) · 화면이 기록(5초 늦춤)보다 먼저' % (mn, mb, runs),
             first and mn <= mb * 1.25 + 300, {'새 판': tn, '바탕': tb, '(첫 화면, 기록 옴)': before})


# ════════════════════════ 민법OX ════════════════════════
class XRemote(JG.Remote):
    """가짜 원격 — 시험 기록 자리 = 지어낸 값 · 404 둘만(진짜 기록은 안 연다) · 기록(<과목>/기록.json)·settings = 새 기기(메모리만)"""

    def __init__(self, mode='ok'):
        super().__init__()
        self.mode = mode

    def get(self, repo, path):
        if path == 'exam/꼬까.json':
            return EXB if self.mode == 'ok' else None
        if path.endswith('기록.json') or path == 'settings.json':
            with self.lock:
                return self.files.get(repo + ':' + path)
        return super().get(repo, path)


def mb_route(remote):
    base = JG.route_handler(remote)

    def h(route):
        if route.request.url.startswith('https://cdn.tailwindcss.com') and not TWCSS:
            return route.continue_()   # 본 PC = 진짜 Tailwind cdn · 클라우드 = --tw 사본을 글에 넣었다
        return base(route)
    return h


TW_TAG = '<script src="https://cdn.tailwindcss.com"></script>'


def mb_html(src):
    if TWCSS and TW_TAG in src:
        return src.replace(TW_TAG, '<style>/* harness: Tailwind v3 사본(--tw) */\n' + open(TWCSS, encoding='utf-8').read() + '\n</style>', 1)
    return src


MB_SERVERS = {}


def mb_serve(tag, html):
    if tag in MB_SERVERS:
        return MB_SERVERS[tag][1]
    body = html.encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            pth = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            if pth in ('/minbeop/', '/minbeop/index.html'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
                return
            self.send_response(404)
            self.send_header('Content-Length', '0')
            self.end_headers()

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    MB_SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


MB_READY = "typeof quizData!=='undefined' && quizData.length>0 && !!document.querySelector('#dashboard-container > *')"


class MbPg:
    """민법OX 쪽 하나 = 기기 하나(문맥) — 문항 = SPD 문항마스터(가짜 원격) · 토큰(tt.cfg) · 손가락"""

    def __init__(self, br, src, dev=PC, token=True, delay=0, mode='ok'):
        W, Hh = dev
        self.eng = br.browser_type.name
        self.touch = dev != PC
        kw = dict(viewport={'width': W, 'height': Hh}, device_scale_factor=2 if self.touch else 1)
        if self.touch:
            kw.update(has_touch=True)
            if self.eng != 'webkit':
                kw.update(is_mobile=W < 700)
        self.ctx = br.new_context(**kw)
        self.remote = XRemote(mode)
        self.ctx.route('**/*', mb_route(self.remote))
        cfg = json.dumps({'token': 'harness-token', 'person': '꼬까'} if token else {'person': '꼬까'})
        self.ctx.add_init_script("if(!sessionStorage.getItem('__h')){sessionStorage.setItem('__h','1');try{localStorage.setItem('tt.cfg',%s)}catch(e){}}" % json.dumps(cfg))
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:240]))
        port = mb_serve(ntag('ewm'), with_probe('mb', mb_html(src), delay))
        self.pg.goto('http://127.0.0.1:%d/minbeop/index.html' % port, wait_until='load', timeout=180000)
        self._ready()

    def _ready(self):
        self.pg.wait_for_function(MB_READY, timeout=180000)
        self.pg.wait_for_timeout(800)
        self.ev(EW)

    def reload(self):
        self.pg.reload(wait_until='load', timeout=180000)
        self._ready()

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg)

    def wait(self, ms):
        self.pg.wait_for_timeout(ms)

    def click(self, x, y, wait=400):
        self.pg.mouse.click(x, y)
        self.pg.wait_for_timeout(wait)

    def tap(self, x, y, wait=400):
        if self.eng == 'webkit':
            self.pg.touchscreen.tap(x, y)
        else:
            c = self.ctx.new_cdp_session(self.pg)
            c.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y, 'radiusX': 6, 'radiusY': 6, 'id': 1}]})
            self.pg.wait_for_timeout(60)
            c.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            try:
                c.detach()
            except Exception:
                pass
        self.pg.wait_for_timeout(wait)

    def close(self):
        try:
            self.ctx.close()
        except Exception:
            pass


def mb_open(br, src, dev=PC, delay=0, mode='ok', token=True):
    QJ.launch('new')   # 셈(§B-4) — gate 의 첫 화면 바탕 띄움도 이 길(바탕 셈은 first_screen 이 따로)
    return MbPg(br, src, dev, token=token, delay=delay, mode=mode)


def mb_rows():
    M = json.load(open(os.path.join(SPD, 'minbeop', '문항마스터.json'), encoding='utf-8'))
    return [r for r in M['rows'] if r.get('uid') and r.get('문제')]


def mb_meta(r):
    """앱 buildQuizData 의 examMeta 꼴 — (해, 회, 번, 원래 선지 글자)"""
    yr = str(r.get('기출연도') or '').strip()
    if not yr:
        return []
    multi = str(r.get('출제연도') or '').strip()
    out = []
    for tok in ([t for t in re.split(r'[,\s]+', multi) if t] if multi else [yr]):
        y, no, opt = (tok.split(':') + ['', ''])[:3]
        rd = str(r.get('회차') or '').strip() if y == yr else str(int(y) - 1963)
        n = (int(no) if re.fullmatch(r'\d+', no or '') else 0) if no else (int(r.get('문번') or 0) if y == yr else 0)
        raw = opt or (str(r.get('지문') or '').strip() if y == yr else '')
        out.append((y, int(rd or 0) or (int(y) - 1963), n, raw))
    return out


def mb_expect():
    """Q-id → ['회-번' …](회 차례) · Q-id → 그 지문이 나온 해 모음"""
    by = {(x['r'], x['i']): x for x in WR if x['s'] == '민법'}
    exp, years = {}, {}
    for r in mb_rows():
        for y, rd, n, raw in mb_meta(r):
            years.setdefault(r['uid'], set()).add(y)
            x = by.get((rd, n))
            if x and '%d-%d' % (x['r'], x['i']) not in exp.setdefault(r['uid'], []):
                exp[r['uid']].append('%d-%d' % (x['r'], x['i']))
    for k in exp:
        exp[k].sort(key=lambda t: tuple(int(v) for v in t.split('-')))
    return exp, years


MB_IDX = r"""() => { if (typeof ewmIdx !== 'function') return null; const m = ewmIdx(), o = {}; Object.keys(m).forEach(k => { o[k] = m[k].map(x => x.r + '-' + x.i); }); return o; }"""
MB_GOQ = r"""async ([id]) => { const w = ms => new Promise(r => setTimeout(r, ms));
  document.querySelectorAll('.oxwin').forEach(x => x.remove()); const q = quizData.find(x => x.id === id); if (!q) return { err: 'no q' };
  try { goHome(); } catch (e) {} const lab = q.subChapter ? q.chapter + ' > ' + q.subChapter : q.chapter; startQuiz(q.subject, lab);
  for (let i = 0; i < 200 && !document.querySelector('#quiz-container .question-box'); i++) await w(100);
  const ix = (typeof currentFilteredData !== 'undefined' ? currentFilteredData : []).findIndex(x => x.id === id);
  if (ix >= 0 && typeof PAGE_SIZE !== 'undefined') { currentPageIndex = Math.floor(ix / PAGE_SIZE); renderQuizPage(); }
  for (let i = 0; i < 100 && !document.getElementById('q-box-' + id); i++) await w(100); await w(300);
  return { ok: !!document.getElementById('q-box-' + id) }; }"""
MB_EXV = r"""async ([y]) => { const w = ms => new Promise(r => setTimeout(r, ms));
  document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {}
  const rd = (quizData.find(q => (q.examMeta || []).some(m => String(m.year) === String(y) && String(q.examYear) === String(y))) || {}).examRound || String(+y - 1963);
  startQuiz('변리사 기출', y + '년 제' + rd + '회');
  for (let i = 0; i < 200 && !document.querySelector('#quiz-container .question-box'); i++) await w(100); await w(300);
  return { exv: typeof exvOn === 'function' ? exvOn() : null, n: (typeof currentFilteredData !== 'undefined' ? currentFilteredData.length : 0) }; }"""
MB_EXV_ALL = r"""async ([y]) => { const w = ms => new Promise(r => setTimeout(r, ms)); const out = [], seen = new Set(); let prev = '';
  const n = (typeof currentFilteredData !== 'undefined' ? currentFilteredData.length : 0);
  for (let pg = 0; pg < 30; pg++){ currentPageIndex = pg; renderQuizPage(); await w(250);
    const ids = [...document.querySelectorAll('#quiz-container .question-box[id^="q-box-"]')].map(b => b.id).join(',');
    if (!ids || ids === prev) break; prev = ids;
    __EW.list('#quiz-container').forEach(m => { const key = m.k + '|' + m.ewm; if (!seen.has(key)){ seen.add(key); out.push(m); } }); }
  currentPageIndex = 0; renderQuizPage(); await w(200);
  return { n: n, marks: out }; }"""
MB_EXV_FIND = r"""async ([id]) => { const w = ms => new Promise(r => setTimeout(r, ms)); let prev = '';
  for (let pg = 0; pg < 30 && !document.getElementById('q-box-' + id); pg++){ currentPageIndex = pg; renderQuizPage(); await w(250);
    const ids = [...document.querySelectorAll('#quiz-container .question-box[id^="q-box-"]')].map(b => b.id).join(','); if (!ids || ids === prev) break; prev = ids; }
  await w(200); return !!document.getElementById('q-box-' + id); }"""


def mb_c1(br, src, tag):
    exp, years = mb_expect()
    ok = True
    p = mb_open(br, src)
    try:
        st = ewm_wait(p)
        got = p.ev(MB_IDX)
        ok &= T('C1-mb', '앱 표 = 하네스 셈(Q %d · 표시 %d)' % (len(exp), sum(len(v) for v in exp.values())), got == exp,
                {'EWM.st': st, '앱': None if got is None else {'Q': len(got), '다른 것': sorted(set(got) ^ set(exp))[:8]}, '하네스': {k: exp[k] for k in sorted(exp)[:6]}})
        if QJ.SMOKE:   # smoke — C1-mb 앱 표 한 칸만
            return ok
        nn = [k for k in exp if len(exp[k]) > 1]
        ok &= T('C1-mb', '같은 지문이 61·63 둘 다 = 나란히(%s)' % ', '.join('%s %s' % (k, exp[k]) for k in nn), bool(nn) and got is not None and all(got.get(k) == exp[k] for k in nn), nn)
        for y in ('2024', '2026', '2025', '2023'):
            info = p.ev(MB_EXV, [y]) or {}
            ew(p)
            r = p.ev(MB_EXV_ALL, [y]) or {}
            marks = r.get('marks') or []
            want = sorted('%s|%s' % (k, ri) for k, v in exp.items() if y in years.get(k, ()) for ri in v)
            gotk = sorted('%s|%s' % (m['k'], m['ewm']) for m in marks)
            ok &= T('C1-mb', '기출뷰 %s — 표시 %d(기대 %d · 지문 %d)' % (y, len(marks), len(want), r.get('n', 0)), gotk == want and info.get('exv') is not False and r.get('n', 0) > 0,
                    {'기출뷰': info, '다른 것': sorted(set(gotk) ^ set(want))[:8], '글자': sorted(set(m['t'] for m in marks))})
        N('C1-mb', '뺀 줄 — 기출뷰 2023(점수만) · 2025(지운 회차) 표시 0 · 61-3(맞힘)·61-13(2차)·63-20(맞힘) = 표 밖', [(x['r'], x['s'], x['i'], x['why']) for x in WX if x['s'] == '민법'])
        return ok
    finally:
        p.close()


def mb_line_case(p, qid, ewm, want_t, want_u):
    p.ev(MB_GOQ, [qid])
    ew(p)
    sel = '#q-box-' + qid
    at = p.ev("([s, e]) => __EW.pick(s, e, '')", [sel, ewm])
    if not press_at(p, at, 600):
        return {'press': False, 'at': at}
    ln = p.ev("([s]) => __EW.lines(s)", [sel]) or []
    mk = p.ev("() => __EW.cssOf(__EW.picked())")
    at2 = p.ev("() => __EW.hitOf(__EW.picked())")
    press_at(p, at2, 500)
    ln2 = p.ev("([s]) => __EW.lines(s)", [sel]) or []
    one = ln[0] if len(ln) == 1 else None
    return {'press': True, 'n': len(ln), 't': one and one['t'], 'u': one and one['u'], 'prev': one and one['prev'], 'css': one and one['css'], 'mark': mk, 'after': len(ln2),
            'ok': bool(one) and one['t'] == want_t and one['u'] == want_u and len(ln2) == 0}


def mb_c2(br, src, tag):
    ok = True
    p = mb_open(br, src)
    try:
        ewm_wait(p)
        x12, x8, x7 = row_of('민법', 61, 12), row_of('민법', 61, 8), row_of('민법', 63, 7)
        cases = [('Q1204', '61-12', line_of(x12), ['내 답 ' + circ(x12['my'])], '내 답 선지(④)'),
                 ('Q1202', '61-12', line_of(x12), ['정답 ' + circ(x12['ans'])], '정답 선지(②)'),
                 ('Q0888', '61-8', line_of(x8), ['내 답 ' + circ(x8['my'])], '나란히 61 · 내 답 선지(②)'),
                 ('Q0888', '63-7', line_of(x7), [], '나란히 63 · 보기 지문(ㄴ)')]
        for qid, e, wt, wu, nm in cases:
            r = mb_line_case(p, qid, e, wt, wu)
            ok &= T('C2-mb', '%s %s %s — 펼침 「%s」 밑줄 %s' % (qid, e, nm, wt, wu or '없음'), r.get('ok'), r)
            if r.get('css'):
                ok &= T('C2-mb', '%s 펼침 줄 꼴 = H7 .qsub 값 · 접힘 = 11px 800 빨강 글자만' % qid, css_ok(r['css'], QSUB) and css_ok(r.get('mark'), MARK_CSS), {'펼침': r['css'], '접힘': r.get('mark')})
        # 나란히 — 한 머리 줄에 61 · 63 차례로 붙어 섬
        p.ev(MB_GOQ, ['Q0888'])
        side = p.ev(r"""() => { const ms = [...document.querySelectorAll('#q-box-Q0888 .ewmx')]; return { t: ms.map(m => m.textContent.trim()), adj: ms.length === 2 && ms[0].nextElementSibling === ms[1],
          afterExam: ms.length ? (ms[0].previousElementSibling || {}).hasAttribute && ms[0].previousElementSibling.hasAttribute('data-exam') : false }; }""")
        ok &= T('C2-mb', 'Q0888 머리 = 「61-8-X 63-7-X」 나란히 · 출제 칩 바로 뒤', side and side['t'] == ['61-8-X', '63-7-X'] and side['adj'] and side['afterExam'], side)
        return ok
    finally:
        p.close()


MB_JN = r"""async ([y]) => { const w = ms => new Promise(r => setTimeout(r, ms)); document.querySelectorAll('.oxwin').forEach(x => x.remove()); try { goHome(); } catch (e) {} await w(300);
  const b = [...document.querySelectorAll('button[onclick*="openJeongni"]')].find(x => /변리사 기출/.test(x.getAttribute('onclick')) && x.getAttribute('onclick').indexOf(y) >= 0);
  if (b) { const m = /openJeongni\(([^)]*)\)/.exec(b.getAttribute('onclick')); try { (new Function('btn', 'return openJeongni(' + m[1].replace(/,\s*this\s*$/, ', btn') + ')'))(b); } catch (e) { return { err: String(e) }; } }
  else { try { openJeongni('변리사 기출', '@' + y + '년 제' + (+y - 1963) + '회'); } catch (e) { return { err: String(e) }; } }
  await w(900); return { win: !!document.querySelector('[id^="oxwin-jn"], .oxwin [data-jnrow]'), rows: document.querySelectorAll('.oxwin [data-jnrow]').length }; }"""


def mb_c3_dev(br, src, dn, dev, census):
    ok = True
    p = mb_open(br, src, dev)
    try:
        ewm_wait(p)
        x12 = row_of('민법', 61, 12)
        p.ev(MB_GOQ, ['Q1204'])
        r = jo_place_check(p, '#q-box-Q1204', '61-12', '', 'C3-mb', '문제풀이 카드', dn)
        census.append(r)
        ok &= T('C3-mb', '%s 문제풀이 카드' % dn, r['ok'], r)
        info = p.ev(MB_EXV, ['2024']) or {}
        p.ev(MB_EXV_FIND, ['Q1204'])
        r = jo_place_check(p, '#q-box-Q1204', '61-12', '', 'C3-mb', '연도별 기출뷰 카드', dn)
        r['기출뷰'] = info.get('exv')
        r['ok'] = r['ok'] and info.get('exv') is True
        census.append(r)
        ok &= T('C3-mb', '%s 연도별 기출뷰 카드' % dn, r['ok'], r)
        jn = p.ev(MB_JN, ['2024']) or {}
        r = jo_place_check(p, '.oxwin', '61-12', 'Q1204', 'C3-mb', '정리 창 행(변리사 기출 2024)', dn)
        r['창'] = jn
        census.append(r)
        ok &= T('C3-mb', '%s 정리 창 행' % dn, r['ok'], r)
        p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); return 1; }")
        p.ev("() => { openQPopup('Q1204'); return 1; }")
        p.wait(500)
        r = jo_place_check(p, '#oxwin-q-Q1204', '61-12', '', 'C3-mb', '문항 팝업(문제 창)', dn)
        census.append(r)
        ok &= T('C3-mb', '%s 문항 팝업' % dn, r['ok'], r)
        p.ev("() => { document.querySelectorAll('.oxwin').forEach(x => x.remove()); return 1; }")
        p.ev(MB_GOQ, ['Q1204'])
        p.ev("() => { lwOpen('Q1204', null); return 1; }")
        p.wait(600)
        cp = p.ev("() => __EW.copies('#oxwin-lk')") or []
        r = {'자리': '연결 창 머리(사본)', '기기': dn, '표시': len(cp), '표본': cp, 'ok': cp == [lab_of(x12)]}
        census.append(r)
        ok &= T('C3-mb', '%s 연결 창 머리(사본 · 누름 없음)' % dn, r['ok'], r)
        return ok
    finally:
        p.close()


def mb_c3(br, src, tag, census):
    ok = True
    for dn, dev in DEVS:
        ok &= mb_c3_dev(br, src, dn, dev, census)
    return ok


def mb_c4(br, src, base_src, tag):
    ok = True
    exv_n = "async () => { await (%s)(['2024']); return __EW.list('#quiz-container').length; }" % MB_EXV.strip()
    p = mb_open(br, src)   # 토큰 없음 = 문항은 앞서 받아 둔(IndexedDB) 기기에서 토큰만 지우고 다시 연다
    try:
        p.ev("() => { localStorage.setItem('tt.cfg', JSON.stringify({ person: '꼬까' })); return 1; }")
        p.reload()
        st = ewm_wait(p)
        n = p.ev(exv_n)
        h = p.ev("() => window.__ewmH")
        ok &= T('C4-mb', '토큰 없음 — 표시 0 · 오류 0 · 알림 0', n == 0 and not p.errs and not (h or {}).get('errs') and not (h or {}).get('alerts') and (h or {}).get('nEx') == 0,
                {'EWM.st': st, '기출뷰 2024 표시': n, '쪽 오류': p.errs[:3], 'h': h})
    finally:
        p.close()
    if QJ.SMOKE:   # smoke — C4-mb 토큰 없음 한 칸만
        return ok
    p = mb_open(br, src, mode='404')
    try:
        st = ewm_wait(p)
        n = p.ev(exv_n)
        h = p.ev("() => window.__ewmH")
        ok &= T('C4-mb', '404(기록 없음) — 표시 0 · 오류 0 · 알림 0', n == 0 and not p.errs and not (h or {}).get('errs') and not (h or {}).get('alerts'),
                {'EWM.st': st, '기출뷰 2024 표시': n, '쪽 오류': p.errs[:3], 'h': h})
    finally:
        p.close()
    ok &= first_screen('mb', br, src, base_src, mb_open, 'C4-mb')
    p = mb_open(br, src, delay=5000)
    try:
        p.ev(MB_EXV, ['2024'])
        p.ev(MB_EXV_FIND, ['Q1204'])   # 기록이 오기 전에 표시가 설 쪽(12번)을 펴 둔다
        p.ev("() => { const r = document.querySelector('#q-box-Q1204 input[type=radio]'); if (r) { r.click(); } return 1; }")   # 고른 O/X — 끼울 때 그대로여야
        pick0 = p.ev("() => { const r = document.querySelector('#q-box-Q1204 input[type=radio]:checked'); return r ? r.value : null; }")
        h0 = p.ev("() => window.__ewmH")
        r0 = len(p.ev("() => __EW.list('#quiz-container')") or [])
        until(p, "() => window.__ewmH && window.__ewmH.tEx > 0", 12000)
        p.wait(1500)
        n1 = p.ev("() => __EW.list('#q-box-Q1204').map(m => m.t)")
        pick1 = p.ev("() => { const r = document.querySelector('#q-box-Q1204 input[type=radio]:checked'); return r ? r.value : null; }")
        ok &= T('C4-mb', '기록이 5초 늦게 와도 — 펴 둔 기출뷰 카드에 저절로(다시 그리지 않고 끼움 · 고른 O/X 그대로)',
                r0 == 0 and not (h0 or {}).get('tEx') and n1 == [lab_of(row_of('민법', 61, 12))] and pick1 == pick0,
                {'오기 전': r0, '온 뒤 Q1204': n1, '고른 O/X 전·뒤': [pick0, pick1]})
    finally:
        p.close()
    return ok


# ════════════════════════ 자과 ════════════════════════
JG_CODE = {'물리': 'phys', '생물': 'bio', '지학': 'earth'}


def jg_code(x):
    yy = str(x['r'] + 1963)[2:]
    if x['s'] == '물리' and 1 <= x['i'] <= 10:
        return 'PA%s%02d' % (yy, x['i'])
    if x['s'] == '생물' and 21 <= x['i'] <= 30:
        return 'B%s-%d-%02d' % (yy, x['r'], x['i'] - 20)
    if x['s'] == '지학' and 31 <= x['i'] <= 40:
        return 'G%s-%d-%02d' % (yy, x['r'], x['i'] - 30)
    return ''


def jg_expect():
    exp = {s: {} for s in ('phys', 'bio', 'earth')}
    for x in WR:
        c, s = jg_code(x), JG_CODE.get(x['s'])
        if c and s:
            exp[s].setdefault(c, []).append('%d-%d' % (x['r'], x['i']))
    return exp


JG_OF = r"""() => typeof ewmOf !== 'function' ? null : DATA.filter(r => ewmOf(r).length).map(r => [String(r[F.CODE]), ewmOf(r).map(x => x.r + '-' + x.i)])"""
JG_VIEW = r"""async ([c]) => { const r = DATA.find(x => String(x[F.CODE]) === c); if (!r) return { err: 'no ' + c }; await openView(r[F.NO]); await new Promise(z => setTimeout(z, 1500));
  const ms = [...document.querySelectorAll('#view .vtop .ewmx')]; return { no: r[F.NO], t1: (document.getElementById('vT1') || {}).textContent || '', marks: ms.map(m => m.textContent.trim()) }; }"""
JG_NBR = '#view .vtop button:not(.ewmx), #view .vtop #vT1'


def jg_open(br, src, subj='phys', dev=PC, delay=0, mode='ok', token=True):
    init0 = JG.INIT_PP
    if not token:
        JG.INIT_PP = JG.INIT_PP.replace("JSON.stringify({token:'harness-token',person:'__WHO__'})", "JSON.stringify({person:'__WHO__'})")
    try:
        QJ.launch('new')   # 셈(§B-4) — gate 의 첫 화면 바탕 띄움도 이 길(바탕 셈은 first_screen 이 따로)
        p = JG.Pg_PP(br, br.browser_type.name, ntag('ewg'), with_probe('jg', src, delay), subj, dev, who='꼬까', remote=XRemote(mode))
    finally:
        JG.INIT_PP = init0
    ew(p)
    return p


def jg_c1(br, src, tag):
    exp = jg_expect()
    ok = True
    for subj in (('phys', 'bio', 'earth') if not QJ.SMOKE else ('phys',)):   # smoke — 물리 하나
        p = jg_open(br, src, subj)
        try:
            st = ewm_wait(p)
            got = p.ev(JG_OF)
            gm = None if got is None else {c: v for c, v in got}
            ok &= T('C1-jg', '%s 앱 표 = 하네스 셈(%s)' % (subj, ', '.join('%s %s' % (c, v) for c, v in sorted(exp[subj].items()))), gm == exp[subj], {'EWM.st': st, '앱': gm})
            if QJ.SMOKE:   # smoke — C1-jg 물리 앱 표 한 칸만
                continue
            for c, v in sorted(exp[subj].items()):
                r = p.ev(JG_VIEW, [c]) or {}
                ok &= T('C1-jg', '%s 문제 창 머리 %s — 「%s」' % (subj, c, ' '.join(s + '-X' for s in v)), r.get('marks') == [s + '-X' for s in v], r)
            if subj == 'phys':
                for c in ('PA2402', 'PA2501', 'PA2403', 'PA2305'):
                    r = p.ev(JG_VIEW, [c]) or {}
                    ok &= T('C1-jg', 'phys %s(뺀 줄 — 맞힘 · 지운 회차 · 2차 · 점수만) 표시 0' % c, r.get('marks') == [] and not r.get('err'), r)
        finally:
            p.close()
    return ok


def jg_line(p, c, want_t):
    p.ev(JG_VIEW, [c])
    ew(p)
    at = p.ev("() => __EW.pick('#view .vtop', '', '')")
    if not press_at(p, at, 600):
        return {'press': False, 'at': at}
    ln = p.ev("() => __EW.lines('#ewmhold')") or []
    mk = p.ev("() => __EW.cssOf(__EW.picked())")
    pos = p.ev("""() => { const v = document.querySelector('#view .vtop'), h = document.getElementById('ewmhold'); return { after: !!v && v.nextElementSibling === h,
      below: !!(v && h) && h.getBoundingClientRect().top >= v.getBoundingClientRect().bottom - 0.5 }; }""")
    at2 = p.ev("() => __EW.hitOf(__EW.picked())")
    press_at(p, at2, 500)
    ln2 = p.ev("() => __EW.lines('#ewmhold')") or []
    one = ln[0] if len(ln) == 1 else None
    return {'press': True, 'n': len(ln), 't': one and one['t'], 'u': one and one['u'], 'css': one and one['css'], 'mark': mk, 'pos': pos, 'after': len(ln2),
            'ok': bool(one) and one['t'] == want_t and one['u'] == [] and (pos or {}).get('after') and (pos or {}).get('below') and len(ln2) == 0}


def jg_c2(br, src, tag):
    ok = True
    for subj, c, x in (('phys', 'PA2401', row_of('물리', 61, 1)), ('bio', 'B24-61-08', row_of('생물', 61, 28)), ('earth', 'G24-61-10', row_of('지학', 61, 40))):
        p = jg_open(br, src, subj)
        try:
            ewm_wait(p)
            r = jg_line(p, c, line_of(x))
            ok &= T('C2-jg', '%s %s — 머리 아래 펼침 「%s」 · 문항째 = 밑줄 없음' % (subj, c, line_of(x)), r.get('ok'), r)
            if r.get('css'):
                ok &= T('C2-jg', '%s 펼침 줄 꼴 = H7 .qsub 값 · 접힘 = 11px 800 빨강 글자만' % c, css_ok(r['css'], QSUB) and css_ok(r.get('mark'), MARK_CSS), {'펼침': r['css'], '접힘': r.get('mark')})
            if subj == 'phys':   # 같은 문항을 다시 그림(동기화·글 고침) = 펼친 줄 그대로 · 다른 문항 = 걷음
                at = p.ev("() => __EW.pick('#view .vtop', '', '')")
                press_at(p, at, 600)
                n1 = len(p.ev("() => __EW.lines('#ewmhold')") or [])
                p.ev("async () => { await showProblem(); await new Promise(r => setTimeout(r, 500)); return 1; }")
                n2 = len(p.ev("() => __EW.lines('#ewmhold')") or [])
                at2 = p.ev("() => __EW.pick('#view .vtop', '', '')")
                press_at(p, at2, 600)
                n3 = len(p.ev("() => __EW.lines('#ewmhold')") or [])
                press_at(p, p.ev("() => __EW.pick('#view .vtop', '', '')"), 600)
                n4 = len(p.ev("() => __EW.lines('#ewmhold')") or [])
                p.ev(JG_VIEW, ['PA2604'])
                n5 = len(p.ev("() => __EW.lines('#ewmhold')") or [])
                ok &= T('C2-jg', '같은 문항 다시 그림 = 펼친 줄 그대로(다시 그린 표시로 접힘) · 다른 문항 = 걷음', [n1, n2, n3, n4, n5] == [1, 1, 0, 1, 0],
                        {'펼침': n1, '다시 그림 뒤': n2, '누름(접힘)': n3, '다시 펼침': n4, '다른 문항': n5})
        finally:
            p.close()
    return ok


def jg_c3(br, src, tag, census):
    ok = True
    for dn, dev in DEVS:
        for subj, c in (('phys', 'PA2604'), ('bio', 'B26-63-01'), ('earth', 'G26-63-01')):
            p = jg_open(br, src, subj, dev)
            try:
                ewm_wait(p)
                p.ev(JG_VIEW, [c])
                r = jo_place_check(p, '#view .vtop', '', '', 'C3-jg', '문제 창 머리(%s)' % subj, dn, nbr_extra=JG_NBR)
                clip = p.ev("""() => { const m = document.querySelector('#view .vtop .ewmx'), t = document.querySelector('#view .vtop .title'); if (!m) return null; const a = m.getBoundingClientRect(), b = t.getBoundingClientRect();
                  return { inTitle: a.left >= b.left - 0.5 && a.right <= b.right + 0.5, t1clip: (() => { const e = document.getElementById('vT1'); return e.scrollWidth > e.clientWidth; })() }; }""")
                r['머리 안'] = clip
                r['ok'] = r['ok'] and bool(clip) and clip['inTitle']
                census.append(r)
                ok &= T('C3-jg', '%s 문제 창 머리 %s %s' % (dn, subj, c), r['ok'], r)
            finally:
                p.close()
    return ok


def jg_c4(br, src, base_src, tag):
    ok = True
    for nm, kw, c in (('토큰 없음(물리)', {'subj': 'phys', 'token': False}, 'PA2401'), ('404(기록 없음 · 생물)', {'subj': 'bio', 'mode': '404'}, 'B26-63-01')):
        if QJ.SMOKE and nm != '토큰 없음(물리)':
            continue   # smoke = 토큰 없음(물리) 한 칸(표시 0 · 오류 0 · 알림 0)
        p = jg_open(br, src, **kw)
        try:
            st = ewm_wait(p)
            r = p.ev(JG_VIEW, [c]) or {}
            h = p.ev("() => window.__ewmH")
            ok &= T('C4-jg', '%s — 표시 0 · 오류 0 · 알림 0' % nm, r.get('marks') == [] and not p.errs and not (h or {}).get('errs') and not (h or {}).get('alerts'),
                    {'EWM.st': st, c: r.get('marks'), '쪽 오류': p.errs[:3], 'h': h})
        finally:
            p.close()
    if QJ.SMOKE:   # smoke — C4-jg 토큰 없음 한 칸만
        return ok
    ok &= first_screen('jg', br, src, base_src, lambda b, s, delay=0: jg_open(b, s, 'phys', PC, delay=delay), 'C4-jg')
    p = jg_open(br, src, 'bio', delay=8000)   # 생물 = 시험지 PDF 를 안 기다린다(물리는 PDF 여섯을 받는 동안 기록이 와 버린다)
    try:
        r0 = p.ev(JG_VIEW, ['B26-63-01']) or {}
        h0 = p.ev("() => window.__ewmH") or {}
        until(p, "() => window.__ewmH && window.__ewmH.tEx > 0", 15000)
        p.wait(1200)
        m1 = p.ev("() => [...document.querySelectorAll('#view .vtop .ewmx')].map(m => m.textContent.trim())")
        ok &= T('C4-jg', '기록이 8초 늦게 와도 — 열어 둔 문제 창 머리에 저절로', not h0.get('tEx') and r0.get('marks') == [] and m1 == [lab_of(row_of('생물', 63, 21))],
                {'오기 전': r0.get('marks'), '그때 기록': h0.get('tEx'), '온 뒤': m1})
    finally:
        p.close()
    return ok


# ════════════════════════ 자과 2 — uid_unify_add1 (2026-10-04 · jagwa/gigu/_task_jagwa_uid_unify_add1.md §B) ════════════════════════
# 시험 틀림 「61-40-X」 가 문제 창 머리(위 C1~C4)뿐 아니라 서랍 줄 · 첫 화면 목록 카드 · 목차 「지금 목록」 줄에도(클래스 .ewmt · 글자만 · 누름 없음 · 거르개·셈·정렬 안 넣음).
# 위 C1~C4 는 한 글자도 안 바꿨다 — 더한 칸 = JG2-B1 ~ JG2-B5 · 이 칸만 = --only JG2 (앱만 = --apps jg --eng chromium · 새 판 = --jg <jagwa/index.html>)
JGBASE = ARG('--jgbase', '4754b1d')   # JG2 헛잣대 바탕(genie 커밋 · 파일도 됨) — uid_unify ④ 판이 서면 그 커밋으로 바꾼다(앱을 고치는 칸이 아니라 바탕만 갈아 끼운다)
REAL = ARG('--real', _roots.spd('exam', '꼬까.json'))   # B5 진짜 시험 기록 사본 — 읽기만(studyplandata 클론에 쓰지도 · fetch · pull 하지도 않는다) · 결과엔 수만 적는다
JG3 = ('phys', 'bio', 'earth')
JG2_WAIT = 1500 if YARD else 8000   # 표시가 셈에 닿기를 기다리는 한도(ms) — 헛잣대(바탕)는 끝내 안 닿으니 짧게
JG2ENG = [x for x in (ARG('--jg2eng', 'chromium') or '').split(',') if x]   # (add1 검수 10/4) JG2-B2 「늦게 오면」 을 어느 엔진으로 돌릴지 — 기본 chromium = 지금처럼 크롬만 · `chromium,webkit` = 크롬 칸 뒤에 WebKit 칸을 더함 · `webkit` = WebKit 칸만(스크롤 고정이 없어 scrollTop 은 그대로인데 카드가 밀릴 수 있다)
PWH = {}   # main() 이 Playwright 핸들을 둔다 — JG2-B2 WebKit 길이 쓴다
SPEC02 = {(63, '물리'): 4, (63, '생물'): 3, (63, '지학'): 2, (61, '물리'): 7, (61, '생물'): 1, (61, '지학'): 1}   # 지시서 바탕 _task_exam_wrong_mark §0-2 의 자과 줄(= 18)
_JGB = {}


def jg2_base_src():
    """JG2 바탕 앱 글(--jgbase · 기본 4754b1d = 이 판 앞) — 한 번만 푼다"""
    if 'v' not in _JGB:
        QJ.sub('git:show-app')
        _JGB['v'] = app_src('jg', JGBASE)
    return _JGB['v']


_JGH = {}


def jg2_hdr(src):
    """JG2 첫 단계가 한 번만 — 어느 앱 · 어느 바탕 · 진짜 기록 사본이 있는가(값은 안 적는다)"""
    if _JGH:
        return
    _JGH['x'] = 1
    try:
        real = '있음(%d B)' % os.path.getsize(REAL)
    except Exception:
        real = '없음'
    N('JG2', '새 판 · 바탕 · 지어낸 기록 · 진짜 기록 사본', {'새 판 md5(LF)': md5lf(src), '바탕': JGBASE, '바탕 md5(LF)': md5lf(jg2_base_src()) if QJ.GATE else '(regress — 안 읽음 · git show 0)', '지어낸 기록': os.path.relpath(FX, HERE), '진짜 기록 사본': real, '헛잣대 모드': YARD})


# ── 쪽 첫머리(PROBE 와 같은 것 + 응답 잡아 두기) — D < 0 이면 exam/꼬까.json 응답을 손으로 풀 때까지 잡아 둔다(window.__ewmRelease()) · D ≥ 0 은 PROBE 그대로 ──
PROBE2 = r"""<script>/* exam_wrong_mark 하네스 JG2 — D < 0 = 응답을 잡아 둠(__ewmRelease() 로 푼다) */(function(){ var D = __D__, READY = __R__;
 var H = window.__ewmH = { t1: 0, tEx: 0, nEx: 0, held: 0, alerts: 0, errs: [] };
 var gate = D < 0 ? { open: false, q: [] } : null;
 window.__ewmRelease = function(){ if (!gate) return 0; gate.open = true; var q = gate.q.splice(0); q.forEach(function(f){ f(); }); return q.length; };
 window.addEventListener('error', function(e){ H.errs.push(String(e.message || '').slice(0, 160)); });
 window.addEventListener('unhandledrejection', function(e){ H.errs.push('reject: ' + String((e.reason && e.reason.message) || e.reason).slice(0, 160)); });
 var of = window.fetch;
 window.fetch = function(u, o){ var s = String((u && u.url) || u), d = s; try{ d = decodeURIComponent(s); }catch(e){}
   if (/exam\/꼬까\.json/.test(d)){ H.nEx++; var go = function(){ return of.call(window, u, o).then(function(r){ H.tEx = performance.now(); return r; }, function(e){ H.tEx = performance.now(); throw e; }); };
     if (gate && !gate.open){ H.held++; return new Promise(function(res){ gate.q.push(res); }).then(go); }
     return D > 0 ? new Promise(function(res){ setTimeout(res, D); }).then(go) : go(); }
   return of.apply(window, arguments); };
 var iv = setInterval(function(){ try{ if (!H.t1 && READY()){ H.t1 = performance.now(); clearInterval(iv); } }catch(e){} }, 20);
 window.alert = function(){ H.alerts++; };
})();</script>"""


def with_probe2(app, src, delay=0):
    b = src.index('<body')
    bb = src.index('>', b) + 1
    return src[:bb] + PROBE2.replace('__D__', str(int(delay))).replace('__R__', READY[app]) + src[bb:]


# ── 쪽 도구 2(서랍 줄 · 목록 카드 · 지금 목록 줄의 .ewmt) — 열쇠 = 문항 uid(F.CODE) · 서랍 줄 = data-no · 목록 카드 = data-uid(생물·지학) / data-pv=P+번호(물리) · 지금 목록 = data-no ──
EW2 = r"""() => { if (window.__EW2) return 1;
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const codeOf = no => { try { const r = rec(no); return r ? String(r[F.CODE]) : ''; } catch (e) { return ''; } };
const itemCode = it => { if (!it) return ''; const d = it.dataset || {}; if (d.uid) return String(d.uid);
  if (d.pv) { const n = parseInt(String(d.pv).replace(/^\D+/, ''), 10); return n ? codeOf(n) : ''; } return ''; };
const add = (o, k, t) => { (o[k] = o[k] || []).push(t); };
const noOf = c => { const r = DATA.find(x => String(x[F.CODE]) === c); return r ? r[F.NO] : 0; };
const rowOf = no => document.querySelector('#ndList .ndrow[data-no="' + no + '"]');
const trqOf = no => document.querySelector('#trq .trqr[data-no="' + no + '"]');
const itemOf = c => [...document.querySelectorAll('#list .item')].find(it => itemCode(it) === c) || null;
const cs = e => e ? __EW.cssOf(e) : null;
const R1 = v => Math.round(v * 10) / 10;
window.__EW2 = {
  noOf: noOf,
  /* 세 자리의 .ewmt — 열쇠(uid)별 글자 · 개수 · 줄 수 */
  collect: () => { const out = { drawer: {}, list: {}, trq: {} };
    document.querySelectorAll('#ndList .ewmt').forEach(e => { const r = e.closest('.ndrow'); add(out.drawer, r ? codeOf(+r.dataset.no) : '(줄 밖)', txt(e)); });
    document.querySelectorAll('#list .ewmt').forEach(e => { const r = e.closest('.item'); add(out.list, r ? itemCode(r) : '(카드 밖)', txt(e)); });
    document.querySelectorAll('#trq .ewmt').forEach(e => { const r = e.closest('.trqr'); add(out.trq, r ? codeOf(+r.dataset.no) : '(줄 밖)', txt(e)); });
    out.n = { drawer: document.querySelectorAll('#ndList .ewmt').length, list: document.querySelectorAll('#list .ewmt').length, trq: document.querySelectorAll('#trq .ewmt').length, all: document.querySelectorAll('.ewmt').length,
      drawerRows: document.querySelectorAll('#ndList .ndrow').length, listItems: document.querySelectorAll('#list .item').length, trqRows: document.querySelectorAll('#trq .trqr').length };
    return out; },
  /* 한 문항의 표시 자리 · 꼴 — 서랍 = 꼬리(.ndtail) 맨 앞 · 목록 = .meta 안 · 뒤가 ★ 또는 제목(.sub) · 지금 목록 = 발문(.ndt) 바로 뒤 */
  place: c => { const no = noOf(c), row = rowOf(no), it = itemOf(c), tq = trqOf(no);
    const d = row ? row.querySelector('.ewmt') : null, ls = it ? [...it.querySelectorAll('.ewmt')] : [], l = ls.length ? ls[ls.length - 1] : null, t = tq ? tq.querySelector('.ewmt') : null;
    const sib = e => e ? String(e.className || e.tagName).slice(0, 24) : '';
    return { no: no, row: !!row, card: !!it, trq: !!tq,
      d: d ? { tail: d.parentElement.classList.contains('ndtail'), first: d === d.parentElement.firstElementChild, css: cs(d) } : null,
      /* 옛 줄(add1 검수 전): l: l ? { meta: l.parentElement.classList.contains('meta'), nextOk: !!(l.nextElementSibling && l.nextElementSibling.matches('.star, .sub')), next: sib(l.nextElementSibling), prev: sib(l.previousElementSibling), css: cs(l) } : null, */
      l: l ? { meta: l.parentElement.classList.contains('meta'), nextOk: !!(l.nextElementSibling && l.nextElementSibling.matches('.star, .sub')), next: sib(l.nextElementSibling), prev: sib(l.previousElementSibling),
        sub: [...l.parentElement.children].some(x => x.classList.contains('sub')), prevKind: (() => { let q = l.previousElementSibling; while (q && q.classList.contains('ewmt')) q = q.previousElementSibling; return !!(q && q.matches('.tag.tg')); })(), css: cs(l) } : null,
      t: t ? { afterNdt: !!(t.previousElementSibling && t.previousElementSibling.classList.contains('ndt')), css: cs(t) } : null }; },
  /* 서랍 줄 높이 · 가로 넘침 — 표시를 켠 채 · 끈 채(그 줄의 .ewmt 만 display:none) 잰 값 */
  rowH: no => { const row = rowOf(no); if (!row) return null; const tags = [...row.querySelectorAll('.ewmt')];
    const meas = () => { const r = row.getBoundingClientRect(), nd = row.querySelector('.ndt'); return { h: Math.round(r.height * 100) / 100, sw: row.scrollWidth, cw: row.clientWidth, ndt: nd ? Math.round(nd.getBoundingClientRect().width) : -1 }; };
    const a = meas(); tags.forEach(t => { t.style.display = 'none'; }); const b = meas(); tags.forEach(t => { t.style.display = ''; });
    return { n: tags.length, on: a, off: b }; },
  /* 목록 카드 가로 넘침 — 카드 · .meta · 쪽 전체 · 표시가 카드 안에 서는지 · 표시를 켠 채 · 끈 채 */
  cardOv: c => { const it = itemOf(c); if (!it) return null; const m = it.querySelector('.meta'), tags = [...it.querySelectorAll('.ewmt')]; if (!tags.length) return { n: 0 };
    const se = document.scrollingElement || document.documentElement;
    const meas = () => ({ sw: it.scrollWidth, cw: it.clientWidth, msw: m ? m.scrollWidth : 0, mcw: m ? m.clientWidth : 0, psw: se.scrollWidth, vw: innerWidth, h: R1(it.getBoundingClientRect().height) });
    const last = tags[tags.length - 1], R = it.getBoundingClientRect(), r = last.getBoundingClientRect();
    const a = Object.assign(meas(), { n: tags.length, tagL: R1(r.left), tagR: R1(r.right), cardL: R1(R.left), cardR: R1(R.right) });
    tags.forEach(t => { t.style.display = 'none'; }); const b = meas(); tags.forEach(t => { t.style.display = ''; });
    return { on: a, off: b }; },
  /* 누를 표시 고르기 · 굴림이 멎을 때까지 · 누른 뒤 상태 */
  pickTag: (kind, c) => { document.querySelectorAll('.ewmt[data-ewp2]').forEach(x => x.removeAttribute('data-ewp2'));
    const no = noOf(c); let e = null;
    if (kind === 'drawer') { const r = rowOf(no); e = r ? r.querySelector('.ewmt') : null; }
    else if (kind === 'list') { const it = itemOf(c); e = it ? it.querySelector('.ewmt') : null; }
    else { const t = trqOf(no); e = t ? t.querySelector('.ewmt') : null; }
    if (!e) return null; e.setAttribute('data-ewp2', '1'); return __EW.hitOf(e); },
  /* ★ 2026-10-09 _task_jagwa_gg3 §A-4(사용자 10/8 18:20 「첫 화면 · 카드 = 제목만 엶 · 세 과목」) — 표시가 붙은 목록 카드의 제목(.sub · 없으면 코드 .num) 누를 자리(gg3 판 갈음 칸) */
  pickTitle: c => { const it = itemOf(c); const e = it ? (it.querySelector('.sub') || it.querySelector('.num')) : null; return e ? __EW.hitOf(e) : null; },
  settleTag: async () => { const e = document.querySelector('.ewmt[data-ewp2]'); if (!e) return null; let last = '', same = 0;
    for (let i = 0; i < 60 && same < 3; i++) { await new Promise(r => setTimeout(r, 100)); const r = e.getBoundingClientRect(), k = Math.round(r.left) + ',' + Math.round(r.top); if (k === last) same++; else { same = 0; last = k; } }
    return __EW.hitOf(e); },
  state: () => ({ vno: (typeof VNO === 'undefined') ? null : VNO, hide: document.getElementById('view').classList.contains('hide') }),
  /* 스크롤 자리 — 쪽(첫 화면 목록) · 서랍(#ndList) · 기준 카드(첫 화면에 온전히 보이는 첫 카드 또는 a)의 위치 */
  scrollSet: (y, dy) => { const se = document.scrollingElement || document.documentElement, L = document.getElementById('ndList');
    se.scrollTop = Math.max(0, Math.min(y, se.scrollHeight - innerHeight - 40)); if (L) L.scrollTop = Math.max(0, Math.min(dy, L.scrollHeight - L.clientHeight - 20)); return 1; },
  scrollGet: a => { const se = document.scrollingElement || document.documentElement, L = document.getElementById('ndList'); let it = null, code = a || '';
    if (code) it = itemOf(code);
    else { it = [...document.querySelectorAll('#list .item')].find(x => { const r = x.getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; }) || null; code = it ? itemCode(it) : ''; }
    return { y: Math.round(se.scrollTop), nd: L ? Math.round(L.scrollTop) : -1, ndMax: L ? Math.round(L.scrollHeight - L.clientHeight) : -1, pageMax: Math.round(se.scrollHeight - innerHeight),
      anchor: code, anchorTop: it ? R1(it.getBoundingClientRect().top) : null }; },
  /* 위쪽 높이 변화 재기(add1 검수 10/4 · 참고 · 판정 아님) — tagOld = 지금 있는 목록 카드 노드에 표시(다시 그렸으면 사라진다) · topSnap(a) = 기준 카드(a)의 문서 위치 · 쪽 높이 · 목록 높이 · 그 위 카드마다 [uid, 높이, 머리 .meta, 발문 .prev, 그림 칸 .pvfig, 그림 칸 상태] */
  tagOld: () => { document.querySelectorAll('#list .item').forEach(x => x.setAttribute('data-ew2old', '1')); return 1; },
  topSnap: a => { const se = document.scrollingElement || document.documentElement, items = [...document.querySelectorAll('#list .item')], k = a ? items.findIndex(x => itemCode(x) === a) : -1;
    const hh = e => e ? R1(e.getBoundingClientRect().height) : 0, anc = k >= 0 ? items[k] : null, above = k > 0 ? items.slice(0, k) : [];
    const figE = x => { const f = x.querySelector('.pvfig'); return !f ? 'none' : ((f.firstElementChild || (f.textContent || '').trim()) ? 'filled' : 'empty'); };
    return { absTop: anc ? R1(anc.getBoundingClientRect().top + se.scrollTop) : null, sh: se.scrollHeight, listH: hh(document.getElementById('list')), n: items.length, kept: items.filter(x => x.hasAttribute('data-ew2old')).length,
      rows: above.map(x => [itemCode(x), hh(x), hh(x.querySelector('.meta')), hh(x.querySelector('.prev')), hh(x.querySelector('.pvfig')), figE(x)]) }; }
};
return 1; }"""
JG2_OPEN = r"""async ([c]) => { const r = DATA.find(x => String(x[F.CODE]) === c); if (!r) return { err: 'no ' + c };
  await openView(r[F.NO]); for (let i = 0; i < 40 && VNO !== r[F.NO]; i++) await new Promise(z => setTimeout(z, 50)); await new Promise(z => setTimeout(z, 1200));
  return { no: r[F.NO], vno: VNO, hide: document.getElementById('view').classList.contains('hide') }; }"""
JG2_CLOSE = "() => { const v = document.getElementById('view'); if (v && !v.classList.contains('hide')) { try { closeView(); } catch (e) {} } return 1; }"
JG2_FOLD = r"""([on]) => { try { ndResFold(on); return 1; } catch (e) { return String(e).slice(0, 80); } }"""   # 서랍 접기 · 펴기(앱 함수 그대로 — 좁은 폭은 접힌 채 시작한다)
JG2_WARN = r"""() => { if (window.__warns) return 1; window.__warns = []; const w = console.warn;
  console.warn = function(){ try { window.__warns.push([].slice.call(arguments).map(a => String((a && a.message) || a)).join(' ').slice(0, 200)); } catch (e) {} return w.apply(console, arguments); }; return 1; }"""


class XRemoteReal(XRemote):
    """가짜 원격 — 시험 기록 자리에 진짜 기록 사본(REAL 파일 바이트 · 읽기만)을 준다 · 그 밖은 XRemote 그대로(기록·settings = 새 기기 · 문항 = SPD 로컬 사본)"""

    def __init__(self, raw):
        super().__init__('ok')
        self.raw = raw

    def get(self, repo, path):
        if path == 'exam/꼬까.json':
            return self.raw
        return super().get(repo, path)


def jg2_open(br, src, subj='phys', dev=PC, delay=0, mode='ok', token=True, gate=False, remote=None, who='new'):
    """자과 쪽 하나(jg_open 과 같은 길 · 이 칸만의 쪽 첫머리 PROBE2 + 쪽 도구 EW2) — gate=True 면 시험 기록 응답을 잡아 둔다 · remote = 진짜 기록 사본 등"""
    init0 = JG.INIT_PP
    if not token:
        JG.INIT_PP = JG.INIT_PP.replace("JSON.stringify({token:'harness-token',person:'__WHO__'})", "JSON.stringify({person:'__WHO__'})")
    try:
        QJ.launch(who)
        p = JG.Pg_PP(br, br.browser_type.name, ntag('ewg'), with_probe2('jg', src, -1 if gate else delay), subj, dev, who='꼬까', remote=remote or XRemote(mode))
    finally:
        JG.INIT_PP = init0
    ew(p)
    p.ev(EW2)
    return p


# ── 기댓값 — 시험 기록(지어낸 것 · 진짜 사본)에서 하네스가 따로 센다(앱 ewmOf 를 안 쓴다) ──
def jg2_expect(rows):
    """{과목: {uid: ['61-40-X', …(회·번 순)]}} — 틀림 줄(ex_rows 가 이미 ok true · 화학 · 지운 회차 · 2차 · 점수만 을 뺀 것)을 앱이 보이는 ID(jg_code)로"""
    exp = {s: {} for s in JG3}
    for x in rows:
        c, s = jg_code(x), JG_CODE.get(x['s'])
        if c and s:
            exp[s].setdefault(c, []).append('%d-%d-X' % (x['r'], x['i']))
    for s in exp:
        for c in exp[s]:
            exp[s][c].sort(key=lambda t: tuple(int(q) for q in t[:-2].split('-')))
    return exp


def jg2_want(subj):
    return jg2_expect(WR)[subj]


def jg2_eq(got, want):
    return {k: list(v) for k, v in (got or {}).items()} == {k: list(v) for k, v in (want or {}).items()}


def jg2_diff(got, want):
    g, w = got or {}, want or {}
    return {'앱만': sorted(set(g) - set(w))[:6], '셈만': sorted(set(w) - set(g))[:6], '글자 다름': sorted(k for k in set(g) & set(w) if list(g[k]) != list(w[k]))[:6]}


def jg2_opened(o):
    """JG2_OPEN 결과 — 그 문항이 정말 열렸나(없는 코드 = err · 번호 없음이 거저 같아지지 않게)"""
    return bool(o) and bool(o.get('no')) and o.get('vno') == o.get('no') and o.get('hide') is False


# ── add1 검수 고침(2026-10-04) — 값 판정 함수(브라우저 없이 가짜 값으로 시험할 수 있게 순수 함수로) ──
def jg2_l_ok(l):
    """목록 카드 표시 자리(.meta 안) — 제목 칸(.sub)이 있는 줄 = 옛 잣대 그대로(표시 바로 뒤가 ★ 또는 제목 .sub) ·
    제목 칸이 없는 줄(uid_unify §G-1 이 기출 uid 줄의 .sub 를 안 그린다 — 생물 · 지학) = 기출 칩(kindTag .tag.tg) 바로 뒤(또는 옛 잣대대로 ★ 앞)"""
    if not l or not l.get('meta'):
        return False
    if l.get('sub') is False:   # 제목 칸 없음 — 새 값(sub · prevKind)이 없으면(None) 옛 잣대로
        return bool(l.get('nextOk')) or bool(l.get('prevKind'))
    return bool(l.get('nextOk'))


def jg2_scroll_keep(eng, mv_y, shift):
    """늦게 온 뒤 「스크롤 자리 그대로」(= 사용자가 보는 자리가 안 튐) — (통과, 까닭)
    크롬 = 기준 카드 이동 ≤ 1px(10/5 조임 — 쪽 스크롤 같음만으로는 통과 안 함 · 크롬의 스크롤 고정(overflow-anchor)이 위쪽 높이 변화를 scrollTop 으로 갚으면 쪽 스크롤은 달라도 화면은 제자리 · 값 칸에 둘 다)
    WebKit = 스크롤 고정이 없다 — scrollTop 은 그대로인데 카드가 밀릴 수 있어 scrollTop 같음은 증거가 못 된다 → 기준 카드 이동 ≤ 1px 만"""
    held = shift is not None and abs(shift) <= 1
    if eng == 'webkit':
        return held, (('기준 카드 제자리(이동 %s px)' % shift) if held else ('튐 — 기준 카드 이동 %s px(쪽 스크롤 이동 %s px)' % (shift, mv_y)))
    # 옛 줄(다섯째 일꾼 판): if mv_y <= 1: return True, …(쪽 스크롤 같음이면 통과) — scrollTop 그대로 · 카드 밀림을 통과시켜 조임(본 세션 10/5 00:0x)
    if shift is None:   # 기준 카드를 못 잼 — 쪽 스크롤 같음으로만
        return mv_y <= 1, '기준 카드 못 잼 · 쪽 스크롤 이동 %s px' % mv_y
    if held:
        return True, '기준 카드 제자리(이동 %s px · 쪽 스크롤 이동 %s px%s)' % (shift, mv_y, ' — 크롬의 스크롤 고정이 위쪽 높이 변화를 갚음' if mv_y > 1 else '')
    return False, '튐 — 쪽 스크롤 %s px · 기준 카드 이동 %s px' % (mv_y, shift)


def jg2_top_diff(s0, s1):
    """위쪽 높이 변화 재기(참고 · 판정 아님) — 풀기 직전(s0) · 온 뒤(s1)의 topSnap 을 맞댄다: 기준 카드의 문서 위치 변화(= 그 위에서 줄거나 는 높이) · 어느 카드의 어느 칸(머리 · 발문 · 그림 칸)이 바뀌었나 · 목록을 다시 그렸나(옛 카드 노드 남음)"""
    if not s0 or not s1:
        return {'재지 못함': {'전': bool(s0), '후': bool(s1)}}
    r0 = {r[0]: r for r in (s0.get('rows') or [])}
    r1 = {r[0]: r for r in (s1.get('rows') or [])}
    both = sorted(set(r0) & set(r1))
    ch = [{'카드': u, '높이': [r0[u][1], r1[u][1]], '머리': [r0[u][2], r1[u][2]], '발문': [r0[u][3], r1[u][3]], '그림 칸': [r0[u][4], r1[u][4]], '그림 상태': [r0[u][5], r1[u][5]]}
          for u in both if abs(r0[u][1] - r1[u][1]) > 0.5]

    def cnt(rs):
        o = {}
        for r in rs.values():
            o[r[5]] = o.get(r[5], 0) + 1
        return o

    def dl(a, b):
        return None if a is None or b is None else round(b - a, 1)
    dsum = round(sum(r1[u][1] - r0[u][1] for u in both), 1)
    dabs = dl(s0.get('absTop'), s1.get('absTop'))
    return {'기준 카드 문서 위치 변화(px)': dabs, '쪽 높이 변화(px)': dl(s0.get('sh'), s1.get('sh')), '목록 높이 변화(px)': dl(s0.get('listH'), s1.get('listH')),
            '위 카드 수(전 · 후 · 둘 다)': [len(r0), len(r1), len(both)], '위 카드 높이 합 변화(px · 둘 다 있는 카드)': dsum, '카드 높이 밖에서 온 변화(px · 문서 위치 변화 − 위 카드 높이 합 변화)': (None if dabs is None else round(dabs - dsum, 1)),
            '높이 바뀐 위 카드 수': len(ch), '표본(최대 4)': ch[:4], '그림 칸 상태(전 · 후)': [cnt(r0), cnt(r1)],
            '카드 수(전 · 후)': [s0.get('n'), s1.get('n')], '옛 카드 노드 남음(전 · 후)': [s0.get('kept'), s1.get('kept')]}


def jg2_open_notoken(br, src, subj, dev=PC):
    """토큰 없음 쪽(JG2-B3) — 물리 = 처음부터 토큰 없이(문항이 파일 안 · 옛 길 그대로) · 생물 · 지학 = 문항을 비공개 저장소에서 토큰으로 받아 IndexedDB 에 두는 과목이라
    처음부터 토큰이 없으면 그 과목을 못 열어 물리에 머문다(add1 검수 · 값 「서랍 줄 · 카드 · 지금 목록 줄」 [577, 577, 0] = 물리 줄 수) → 토큰 있게 한 번 열어 문항을 받아 둔 뒤
    토큰만 지우고(tt.cfg 에 person 만) 다시 연다 — 조판기 · 민법 C4-mb 와 같은 길. 같은 문맥(IndexedDB 그대로) · sessionStorage 가 남아 쪽 첫머리 INIT 이 토큰을 되살리지 않는다.
    쪽 오류는 토큰 없는 부팅 것만 센다(첫 열기 것은 수만 '길' 에 적고 비운다)"""
    if subj == 'phys':
        p = jg2_open(br, src, subj, dev, token=False)
        p.ew2way = '처음부터 토큰 없음(물리 · 옛 길)'
        return p
    p = jg2_open(br, src, subj, dev)   # 토큰 있게 — 문항(IndexedDB kv)을 받아 둔다
    try:
        n0 = p.ev("() => typeof DATA === 'undefined' ? -1 : DATA.length")
        e0 = len(p.errs)
        del p.errs[:]
        p.ev("() => { localStorage.setItem('tt.cfg', JSON.stringify({ person: '꼬까' })); return 1; }")
        p.reload()   # 쪽이 새로 서므로 하네스 도구(__EW · __EW2)를 다시 건다
        ew(p)
        p.ev(EW2)
        p.ew2way = '토큰 있게 한 번 열어 문항을 받아 둔 뒤 토큰만 지우고 다시 열음(생물 · 지학 · 받아 둔 문항 줄 %s · 첫 열기 쪽 오류 %d)' % (n0, e0)
    except Exception:
        p.close()
        raise
    return p


def jg2_settle(p, total, ms=None):
    """서랍 · 목록 표시가 셈에 닿을 때까지(서랍은 다시 짓기가 80ms 늦게 따라온다) — 닿으면 400ms 더 두고 한 번 더 읽는다(그 뒤 더 늘거나 줄지 않는지)"""
    ms = ms or JG2_WAIT
    t0 = time.time()
    c = None
    while time.time() - t0 < ms / 1000.0:
        c = p.ev("() => __EW2.collect()")
        n = (c or {}).get('n') or {}
        if n.get('drawer') == total and n.get('list') == total:
            break
        p.wait(200)
    p.wait(400)
    return p.ev("() => __EW2.collect()") or c or {}


def jg2_press(p, kind, code, no):
    """표시 글자(.ewmt) 한가운데를 진짜로 눌러(PC 마우스 · 폰·아이패드 손가락) 그 문제가 열리는지 — 서랍 줄 · 목록 카드"""
    p.ev(JG2_CLOSE)
    p.wait(500)
    at = p.ev("([k, c]) => __EW2.pickTag(k, c)", [kind, code])
    if at:
        at = p.ev("() => __EW2.settleTag()")
    pressed = press_at(p, at, 900) if QJ.GATE else press_at(p, at, 0)
    if pressed and not QJ.GATE:   # regress — 누른 뒤 고정 900 대신 표지(그 문제가 열림 = 바로 아래 판정이 읽는 값 · 상한 900)
        _rg_until(p, _RG_OPENED, 900, 'JG2-B4 누름 → 그 문제 열림', [no])
    st = p.ev("() => __EW2.state()") or {}
    ok = bool(pressed) and bool(no) and st.get('vno') == no and st.get('hide') is False
    p.ev(JG2_CLOSE)
    p.wait(600)
    return {'눌림': bool(pressed), '보임': bool(at and at.get('on')), '열린 문항': st.get('vno'), '기대': no, '창 열림': st.get('hide') is False, 'ok': ok}


def jg2_press_title(p, code, no):
    """★ 2026-10-09 _task_jagwa_gg3 §A-4(사용자 10/8 18:20 「첫 화면 · 카드 = 제목만 엶 · 세 과목」) — 표시가 붙은 목록 카드의 제목을 진짜로 눌러(PC 마우스 · 폰·아이패드 손가락) 그 문제가 열리는지(gg3 판 갈음 칸 · 표시가 제목을 가리지 않는지)"""
    p.ev(JG2_CLOSE)
    p.wait(500)
    at = p.ev("([c]) => __EW2.pickTitle(c)", [code])
    if at:   # 굴린 뒤 자리가 멎게 한 번 더 잰다
        p.wait(400)
        at = p.ev("([c]) => __EW2.pickTitle(c)", [code])
    pressed = press_at(p, at, 900) if QJ.GATE else press_at(p, at, 0)
    if pressed and not QJ.GATE:
        _rg_until(p, _RG_OPENED, 3000, 'JG2-B4 제목 누름 → 그 문제 열림', [no])
    st = p.ev("() => __EW2.state()") or {}
    ok = bool(pressed) and bool(no) and st.get('vno') == no and st.get('hide') is False
    p.ev(JG2_CLOSE)
    p.wait(600)
    return {'눌림': bool(pressed), '보임': bool(at and at.get('on')), '누른 것': (at or {}).get('t', '')[:20], '열린 문항': st.get('vno'), '기대': no, '창 열림': st.get('hide') is False, 'ok': ok}


# ── B-1 — 지어낸 기록 · 세 자리(서랍 줄 · 목록 카드 · 그 문제를 연 뒤 「지금 목록」 줄) · 과목마다 + 거르개 줄 0 + 헛잣대(바탕에서 셋 다 0) ──
def jg2_b1(br, src):
    jg2_hdr(src)
    ok = True
    for subj in JG3:
        want = jg2_want(subj)
        codes = sorted(want)
        total = sum(len(v) for v in want.values())
        lab = ', '.join('%s %s' % (cd, ' '.join(want[cd])) for cd in codes)
        p = jg2_open(br, src, subj, PC)
        try:
            st = ewm_wait(p)
            c = jg2_settle(p, total)
            n0 = c.get('n') or {}
            ok &= T('JG2-B1', '%s 서랍 줄 — 틀림 줄마다 「회-번-X」 하나씩(%s)' % (subj, lab), jg2_eq(c.get('drawer'), want) and total > 0,
                    {'EWM.st': st, '다른 것': jg2_diff(c.get('drawer'), want), '서랍 줄 수': n0.get('drawerRows'), '표시 수': n0.get('drawer')})
            ok &= T('JG2-B1', '%s 목록 카드 — 틀림 줄마다 「회-번-X」 하나씩(%s)' % (subj, lab), jg2_eq(c.get('list'), want) and total > 0,
                    {'다른 것': jg2_diff(c.get('list'), want), '카드 수': n0.get('listItems'), '표시 수': n0.get('list')})
            o = p.ev(JG2_OPEN, [codes[0]]) or {}   # 그 문제를 연 뒤 — 「지금 목록」(#trq) 은 문제를 열어야 선다
            c2 = p.ev("() => __EW2.collect()") or {}
            n2 = c2.get('n') or {}
            opened = jg2_opened(o)
            trq_rows = n2.get('trqRows') or 0
            if subj == 'phys' and trq_rows == 0:
                # 물리는 앱이 「지금 목록」 을 안 채운다(navSync 갈래가 카드 층(생물·지학)만 — 바탕도 같다) → 문제를 연 채 기록이 늦게 오는 길(JG2-B2)에서 잰다
                N('JG2-B1', '%s 지금 목록 줄 — 문제를 연 뒤에도 앱이 안 채움(줄 0 · 바탕 같음) → JG2-B2 「문제를 연 채 늦게 와도」 에서 잼' % subj,
                  {'열림': opened, '지금 목록 줄 수': trq_rows, '표시 수': n2.get('trq')})
            else:
                ok &= T('JG2-B1', '%s 지금 목록 줄 — 문제를 연 뒤 틀림 줄마다 「회-번-X」 하나씩(%s)' % (subj, lab), opened and trq_rows > 0 and jg2_eq(c2.get('trq'), want) and total > 0,
                        {'열림': opened, '다른 것': jg2_diff(c2.get('trq'), want), '지금 목록 줄 수': trq_rows, '표시 수': n2.get('trq')})
            ok &= T('JG2-B1', '%s 그 밖 자리 0 — 문서 전체 표시 수 = 서랍 + 목록 + 지금 목록(문제 창 머리 · 다른 면에 새지 않음)' % subj,
                    n2.get('all') == (n2.get('drawer') or 0) + (n2.get('list') or 0) + (n2.get('trq') or 0) and (n2.get('all') or 0) > 0, n2)
            pl = {cd: p.ev("([x]) => __EW2.place(x)", [cd]) for cd in codes}   # 자리 · 꼴(열어 둔 채라 지금 목록 줄도 있다)
            okp = total > 0
            for cd in codes:
                z = pl[cd] or {}
                d, l, t = z.get('d') or {}, z.get('l') or {}, z.get('t') or {}
                okp = okp and bool(d) and bool(d.get('tail')) and bool(d.get('first')) and css_ok(d.get('css'), MARK_CSS)
                # 옛 줄(add1 검수 전): okp = okp and bool(l) and bool(l.get('meta')) and bool(l.get('nextOk')) and css_ok(l.get('css'), MARK_CSS)
                okp = okp and jg2_l_ok(l) and css_ok(l.get('css'), MARK_CSS)   # 제목 칸(.sub)이 없는 줄(uid_unify §G-1 · 생물 · 지학)은 기출 칩 바로 뒤면 맞는 자리 — 제목 칸이 있으면 옛 잣대 그대로
                if trq_rows > 0:
                    okp = okp and bool(t) and bool(t.get('afterNdt')) and css_ok(t.get('css'), MARK_CSS)
            ok &= T('JG2-B1', '%s 표시 자리 · 꼴 — 서랍 = 꼬리 맨 앞 · 목록 = 기출 칩 뒤 .meta 안(★·제목 앞) · 지금 목록 = 발문 바로 뒤 · 11px 800 #dc2626 글자만' % subj, okp, pl)
            if subj == 'phys':   # 거르개 줄(ok true · 지운 회차 · 2차 · 점수만) — 줄은 앱에 있고(거저 참 아님) 표시만 0
                fl = {cd: p.ev("([x]) => __EW2.place(x)", [cd]) for cd in ('PA2402', 'PA2501', 'PA2403', 'PA2305')}
                ok &= T('JG2-B1', 'phys 거르개 줄(맞힘 PA2402 · 지운 회차 PA2501 · 2차 PA2403 · 점수만 PA2305) — 서랍 줄 · 목록 카드는 있고 표시 0',
                        all(z and z.get('row') and z.get('card') and not z.get('d') and not z.get('l') for z in fl.values()), fl)
        finally:
            p.close()
        if QJ.GATE:   # 헛잣대 — 바탕(--jgbase 4754b1d) 띄움 · 바탕 측정 줄(JG2-B1 BASE) · 헛잣대 칸 — regress 끔(관문만)
            pb = jg2_open(br, jg2_base_src(), subj, PC, who='base')   # 헛잣대 — 바탕에 같은 시험 기록으로 같은 셋 자리를 센다
            try:
                sb = ewm_wait(pb)
                pb.wait(1500)
                cb0 = (pb.ev("() => __EW2.collect()") or {}).get('n') or {}
                ob = pb.ev(JG2_OPEN, [codes[0]]) or {}
                cb = pb.ev("() => __EW2.collect()") or {}
                nb = cb.get('n') or {}
                N('JG2-B1 BASE', '%s 바탕 .ewmt — 서랍 · 목록 · 지금 목록(문제를 연 뒤)' % subj,
                  {'바탕': JGBASE, 'EWM.st': sb, '서랍': nb.get('drawer'), '목록': nb.get('list'), '지금 목록': nb.get('trq'), '서랍 줄 수': nb.get('drawerRows'), '카드 수': nb.get('listItems'), '지금 목록 줄 수': nb.get('trqRows'), '열기 전 합': cb0.get('all')})
                ok &= T('JG2-B1', '%s 헛잣대 — 바탕에서 서랍 · 목록 · 지금 목록 표시 모두 0(줄은 있다)' % subj,
                        nb.get('all') == 0 and (nb.get('drawerRows') or 0) > 0 and (nb.get('listItems') or 0) > 0 and jg2_opened(ob),
                        {'바탕': JGBASE, '서랍': nb.get('drawer'), '목록': nb.get('list'), '지금 목록': nb.get('trq'), '서랍 줄 수': nb.get('drawerRows'), '카드 수': nb.get('listItems')})
            finally:
                pb.close()
    return ok


# ── B-2 — 받기 늦음 · (a) 응답을 잡아 둔 채 서랍·목록을 굴려 두고 풀어 줌 → 세 자리에 나타남 · 스크롤 자리 그대로 · (b) 문제를 연 채 풀어 줌 → 지금 목록 줄도 · (c) 응답 2초 늦춤 → 첫 그리기 시각 ±10% ──
# 옛 줄(add1 검수 전): def jg2_b2_late(br, src, subj):
def jg2_b2_late(br, src, subj, eng='chromium', parts='ab'):   # eng = 열린 브라우저 엔진(chromium · webkit) · parts = 'ab'(옛 길 그대로) · 'a'(WebKit 길 — 스크롤 칸만)
    want = jg2_want(subj)
    codes = sorted(want)
    total = sum(len(v) for v in want.values())
    ok = True
    p = jg2_open(br, src, subj, PC, gate=True)   # (a) 목록 · 서랍 · 스크롤
    try:
        p.ev(JG2_WARN)
        until(p, "() => (window.__ewmH && window.__ewmH.held >= 1) ? 1 : 0", 10000)   # 앱이 기록을 달라고 한 요청이 잡힐 때까지(풀기 전 상태를 거저 참 없이)
        sc = {}
        for _ in range(4):   # 쪽 · 서랍을 굴려 둔다(뒤늦은 다시 그리기로 0 으로 돌아가면 다시 굴림 — 풀기 직전에 읽은 값을 기준으로 쓴다)
            p.ev("() => __EW2.scrollSet(1500, 600)")
            p.wait(700)
            sc = p.ev("() => __EW2.scrollGet('')") or {}
            if (sc.get('y') or 0) >= 300 and (sc.get('nd') or 0) >= 100:
                break
        p.ev("() => __EW2.tagOld()")   # 위쪽 높이 변화 재기(참고) — 풀기 직전 기준 카드 위 카드들의 높이 · 옛 카드 노드 표시(다시 그렸나)
        snap0 = p.ev("([a]) => __EW2.topSnap(a)", [sc.get('anchor')]) or {}
        pre = p.ev("() => ({ st: EWM.st, h: window.__ewmH, c: __EW2.collect().n })") or {}
        released = p.ev("() => window.__ewmRelease()")
        st = ewm_wait(p)
        c = jg2_settle(p, total)
        sc1 = p.ev("([a]) => __EW2.scrollGet(a)", [sc.get('anchor')]) or {}
        snap1 = p.ev("([a]) => __EW2.topSnap(a)", [sc.get('anchor')]) or {}
        h = p.ev("() => window.__ewmH") or {}
        warns = [w for w in (p.ev("() => window.__warns || []") or []) if str(w).startswith('ewm')]
        n = c.get('n') or {}
        before = pre.get('st') == 'wait' and (pre.get('h') or {}).get('held', 0) >= 1 and (pre.get('c') or {}).get('all') == 0   # 풀기 전에 정말 아직 안 온 상태(거저 참 아님)
        mv_y = abs((sc1.get('y') or 0) - (sc.get('y') or 0))
        mv_nd = abs((sc1.get('nd') or 0) - (sc.get('nd') or 0))
        shift = None if sc1.get('anchorTop') is None or sc.get('anchorTop') is None else round(sc1['anchorTop'] - sc['anchorTop'], 1)   # 기준 카드가 화면에서 움직인 px(= 사용자 눈에 튄 만큼)
        keep, keep_why = jg2_scroll_keep(eng, mv_y, shift)   # 크롬 = 쪽 스크롤 같음 또는 기준 카드 이동 ≤ 1px · WebKit = 기준 카드 이동 ≤ 1px(스크롤 고정이 없어 scrollTop 같음은 증거가 못 된다)
        # 옛 줄(add1 검수 전): ok_a = (before and (released or 0) >= 1 and total > 0 and jg2_eq(c.get('drawer'), want) and jg2_eq(c.get('list'), want)
        #                              and (sc.get('y') or 0) >= 300 and (sc.get('nd') or 0) >= 100 and mv_y <= 1 and mv_nd <= 1 and not warns and not p.errs and not h.get('errs'))
        ok_a = (before and (released or 0) >= 1 and total > 0 and jg2_eq(c.get('drawer'), want) and jg2_eq(c.get('list'), want)
                and (sc.get('y') or 0) >= 300 and (sc.get('nd') or 0) >= 100 and keep and mv_nd <= 1 and not warns and not p.errs and not h.get('errs'))
        # 옛 줄(add1 검수 전): ok &= T('JG2-B2', '%s 늦게 오면 — 오기 전 표시 0 · 온 뒤 서랍 · 목록에 틀림 줄마다 하나씩 · 쪽 · 서랍 스크롤 자리 그대로 · 경고 0' % subj, ok_a,
        # (옛 값 칸 끝에 「'기준 카드 위치 이동(px · 참고)': …」 가 참고 값이었다 — 지금은 판정에 든다)
        lab_a = ('%s 늦게 오면 — 오기 전 표시 0 · 온 뒤 서랍 · 목록에 틀림 줄마다 하나씩 · 쪽 · 서랍 스크롤 자리 그대로 · 경고 0' % subj) if eng != 'webkit' else \
            ('%s 늦게 오면(WebKit · 스크롤 고정 없음) — 오기 전 표시 0 · 온 뒤 서랍 · 목록에 틀림 줄마다 하나씩 · 기준 카드 제자리(이동 ≤ 1px) · 서랍 스크롤 자리 그대로 · 경고 0' % subj)
        ok &= T('JG2-B2', lab_a, ok_a,
                {'엔진': eng, '오기 전': {'EWM.st': pre.get('st'), '잡힌 요청': (pre.get('h') or {}).get('held'), '표시 합': (pre.get('c') or {}).get('all')}, '푼 요청 수': released, '온 뒤': {'EWM.st': st, '서랍': n.get('drawer'), '목록': n.get('list')},
                 '다른 것': {'서랍': jg2_diff(c.get('drawer'), want), '목록': jg2_diff(c.get('list'), want)},
                 '쪽 스크롤(전 → 후)': [sc.get('y'), sc1.get('y')], '쪽 스크롤 이동(px)': mv_y, '기준 카드 위치 이동(px)': shift, '자리 판정': keep_why,
                 '서랍 스크롤(전 → 후)': [sc.get('nd'), sc1.get('nd')],
                 '위쪽 높이 변화(참고 · 판정 아님)': jg2_top_diff(snap0, snap1),
                 '경고': warns[:3], '쪽 오류': p.errs[:2]})
    finally:
        p.close()
    if parts == 'a':   # WebKit 길 = 스크롤 칸만(문제를 연 채 길(b)은 엔진과 무관)
        return ok
    p = jg2_open(br, src, subj, PC, gate=True)   # (b) 문제를 연 채 — 지금 목록 줄(물리도 이 길로 선다) · 문제 창 머리는 옛 칸 그대로
    try:
        p.ev(JG2_WARN)
        until(p, "() => (window.__ewmH && window.__ewmH.held >= 1) ? 1 : 0", 10000)
        o = p.ev(JG2_OPEN, [codes[0]]) or {}
        pre = p.ev("() => ({ st: EWM.st, h: window.__ewmH, c: __EW2.collect().n })") or {}
        released = p.ev("() => window.__ewmRelease()")
        st = ewm_wait(p)
        t0 = time.time()
        c = {}
        while time.time() - t0 < JG2_WAIT / 1000.0:   # 세 자리 다 닿을 때까지
            c = p.ev("() => __EW2.collect()") or {}
            nn = c.get('n') or {}
            if nn.get('drawer') == total and nn.get('list') == total and nn.get('trq') == total:
                break
            p.wait(200)
        p.wait(400)
        c = p.ev("() => __EW2.collect()") or c
        hd = p.ev("() => [...document.querySelectorAll('#view .vtop .ewmx')].map(m => m.textContent.trim())") or []
        warns = [w for w in (p.ev("() => window.__warns || []") or []) if str(w).startswith('ewm')]
        n = c.get('n') or {}
        h = p.ev("() => window.__ewmH") or {}
        before = pre.get('st') == 'wait' and (pre.get('h') or {}).get('held', 0) >= 1 and (pre.get('c') or {}).get('all') == 0
        ok_b = (jg2_opened(o) and before and (released or 0) >= 1 and total > 0 and jg2_eq(c.get('trq'), want) and jg2_eq(c.get('drawer'), want) and jg2_eq(c.get('list'), want)
                and hd == want[codes[0]] and not warns and not p.errs and not h.get('errs'))
        ok &= T('JG2-B2', '%s 문제를 연 채 늦게 와도 — 지금 목록 · 서랍 · 목록에 틀림 줄마다 하나씩 · 문제 창 머리도 그대로 · 경고 0' % subj, ok_b,
                {'열림': jg2_opened(o), '오기 전': {'EWM.st': pre.get('st'), '잡힌 요청': (pre.get('h') or {}).get('held'), '표시 합': (pre.get('c') or {}).get('all')}, '푼 요청 수': released,
                 '온 뒤': {'EWM.st': st, '서랍': n.get('drawer'), '목록': n.get('list'), '지금 목록': n.get('trq'), '지금 목록 줄 수': n.get('trqRows')},
                 '다른 것': {'지금 목록': jg2_diff(c.get('trq'), want)}, '문제 창 머리': hd, '경고': warns[:3], '쪽 오류': p.errs[:2]})
    finally:
        p.close()
    return ok


# 옛 줄(10/5 사용자 「1,2 둘다 고쳐」 전): def jg2_b2_first(br, src, subj, runs=3, delay=2000): … for i in range(runs): for who, s, arr in (('new', src, tn), ('base', base_src, tb)):
#   — 매 회 새 판을 먼저 열어 새 판만 늘 ≈300 ms 손해(결정로그 10/5 03:34 · 같은 두 판을 새 판 먼저 +433 ms · 바탕 먼저 −159 ms)
def jg2_b2_first(br, src, subj, runs=6, delay=2000):   # ★ (10/5 채팅 11:0x 진행 「ABBA · 바탕/새 판 각 여섯 이상」) 4 → 6
    """(c) 응답을 2초 늦춰도 첫 화면 시각은 바탕과 같다(±10% — 잡음 바닥 +150ms) · 화면이 기록보다 먼저 — 새 판 · 바탕 번갈아 runs 번 중앙값
    ★ (10/5) 몸풀기 두 쪽(새 판 · 바탕 한 번씩 · 셈 밖 — 브라우저 첫 쪽 찬 시동) + ABBA 차례(회 0 · 3 = 새 판 먼저 · 1 · 2 = 바탕 먼저) — 먼저 여는 몫을 두 판에 같게"""
    if YARD:
        N('JG2-B2', '%s 첫 화면 시각 — 헛잣대 해당 없음' % subj, '바탕끼리 맞대면 거저 참')
        return True
    if QJ.REGRESS:   # regress — 바탕(4754b1d) 띄움 0 · 새 판만(몸풀기 1 + 3 번 중앙값) · 바탕 중앙값 = 기준 스냅샷(_rg_jg2_first)
        return _rg_jg2_first(br, src, subj, delay)
    base_src = jg2_base_src()
    tn, tb, pairs = [], [], []
    seq = (('new', src, tn), ('base', base_src, tb))
    for who, s, _ in seq:   # 몸풀기(셈 밖)
        p = jg2_open(br, s, subj, PC, delay=delay, who=who)
        try:
            until(p, "() => window.__ewmH && window.__ewmH.t1 > 0 ? 1 : null", 60000)
        finally:
            p.close()
    for i in range(runs):
        for who, s, arr in (seq if i % 4 in (0, 3) else seq[::-1]):   # ABBA
            p = jg2_open(br, s, subj, PC, delay=delay, who=who)
            try:
                h = until(p, "() => window.__ewmH && window.__ewmH.t1 > 0 ? window.__ewmH : null", 60000)
                arr.append(round((h or {}).get('t1') or 0))
                if who == 'new':
                    hh = until(p, "() => window.__ewmH && window.__ewmH.tEx > 0 ? window.__ewmH : null", 15000) or {}
                    pairs.append((round((h or {}).get('t1') or 0), round(hh.get('tEx') or 0)))
            finally:
                p.close()
    mn, mb = statistics.median(tn), statistics.median(tb)
    first = all(a > 0 and b > 0 and a < b for a, b in pairs)
    lim = max(mb * 1.10, mb + 150)
    return T('JG2-B2', '%s 첫 화면 시각(기록 2초 늦춤) — 바탕 ±10%%(잡음 바닥 +150ms) 안 · 화면이 기록보다 먼저' % subj, first and mn <= lim,
             {'새 판(ms)': tn, '바탕(ms)': tb, '중앙값': [mn, mb], '허용 상한(ms)': round(lim), '(첫 화면, 기록 옴)': pairs, '바탕 판': JGBASE, '차례': '몸풀기 2 + ABBA %d 회' % runs})


def _rg_jg2_first(br, src, subj, delay, runs=3):
    """regress(_task_qa_slim2 · 10/8) — JG2-B2 첫 화면 시각: 새 판만 몸풀기 1 + runs 번 중앙값 · 바탕 중앙값 = 기준 스냅샷(앞 인도판 같은 칸의 새 판 중앙값 · QJ.base) ·
    칸 이름 · 판정식(±10% · 잡음 바닥 +150ms · 화면이 기록보다 먼저)은 gate 와 같다 — ⚠ 기댓값이 같은 짐에서 잰 바탕이 아니라 다른 때 잰 앞 판 값(결정 거리)"""
    tn, pairs = [], []
    p = jg2_open(br, src, subj, PC, delay=delay)   # 몸풀기(셈 밖)
    try:
        until(p, "() => window.__ewmH && window.__ewmH.t1 > 0 ? 1 : null", 60000)
    finally:
        p.close()
    for i in range(runs):
        p = jg2_open(br, src, subj, PC, delay=delay)
        try:
            h = until(p, "() => window.__ewmH && window.__ewmH.t1 > 0 ? window.__ewmH : null", 60000)
            tn.append(round((h or {}).get('t1') or 0))
            hh = until(p, "() => window.__ewmH && window.__ewmH.tEx > 0 ? window.__ewmH : null", 15000) or {}
            pairs.append((round((h or {}).get('t1') or 0), round(hh.get('tEx') or 0)))
        finally:
            p.close()
    mn = statistics.median(tn)
    cid = 'JG2-B2@first/%s' % subj
    mb = QJ.base(cid, mn)
    first = all(a > 0 and b > 0 and a < b for a, b in pairs)
    lim = max(mb * 1.10, mb + 150)
    return T('JG2-B2', '%s 첫 화면 시각(기록 2초 늦춤) — 바탕 ±10%%(잡음 바닥 +150ms) 안 · 화면이 기록보다 먼저' % subj, first and mn <= lim,
             {'새 판(ms)': tn, '바탕(ms)': [mb], '중앙값': [mn, mb], '허용 상한(ms)': round(lim), '(첫 화면, 기록 옴)': pairs, '바탕 판': '기준 스냅샷 · %s' % QJ.base_note(cid),
              '차례': 'regress — 몸풀기 1 + 새 판 %d 회(바탕 띄움 0)' % runs})


def _rg_until(p, js, ms, what, arg=None):
    """regress — 고정 대기 대신 앱 표지(QJ.until · 상한 = gate 의 ms) · 못 만나면(시간 넘김 · 표지 글 오류) 남은 시간을 채워 gate 와 같은 길이"""
    t = time.time()
    if not QJ.until(p.pg, js, ms, what, arg):
        left = ms - (time.time() - t) * 1000.0
        if left > 1:
            p.pg.wait_for_timeout(left)


_RG_OPENED = "([no]) => typeof VNO !== 'undefined' && VNO === no && !document.getElementById('view').classList.contains('hide')"   # 표지 = 앱 VNO · #view 보임(바로 뒤 판정이 읽는 그 값)


def jg2_b2_wk(src):
    """(add1 검수 10/4) 「늦게 오면」 (a) 를 WebKit 으로도 — 스크롤 고정이 없다(크롬은 위쪽 높이 변화를 scrollTop 으로 갚지만 WebKit 은 scrollTop 은 그대로인데 카드가 밀릴 수 있다)"""
    if YARD:
        N('JG2-B2', 'WebKit 길 — 헛잣대 해당 없음', '바탕끼리 맞대면 거저 참(바탕엔 표시가 없다)')
        return True
    wk = webkit_try(PWH.get('pw'))
    if not wk:
        N('JG2-B2', 'WebKit 길 — 못 돌림(--jg2eng 로 청했으나 이 컴퓨터에 WebKit 이 없다)', 'WK 줄 참고')
        return True
    ok = True
    try:
        for subj in JG3:
            ok &= jg2_b2_late(wk, src, subj, eng='webkit', parts='a')
    finally:
        wk.close()
    return ok


# 옛 줄(add1 검수 전): def jg2_b2(br, src): … for subj in JG3: ok &= jg2_b2_late(br, src, subj) / for subj in JG3: ok &= jg2_b2_first(br, src, subj) / return ok  (아래 — 크롬 갈래는 그대로 `if` 안으로)
def jg2_b2(br, src):
    jg2_hdr(src)
    ok = True
    if 'chromium' in JG2ENG:   # 기본 = 크롬만(지금처럼) · --jg2eng webkit 이면 크롬 칸은 건너뛴다
        for subj in JG3:
            ok &= jg2_b2_late(br, src, subj)
        for subj in JG3:
            ok &= jg2_b2_first(br, src, subj)
    if 'webkit' in JG2ENG:
        ok &= jg2_b2_wk(src)
    return ok


# ── B-3 — 토큰 없음 · 404(기록 없음) = 표시 0 · 오류 0 · 알림 0 (세 자리 모두 · 문제를 연 뒤 지금 목록도) ──
def jg2_b3(br, src):
    jg2_hdr(src)
    ok = True
    for subj in JG3:
        codes = sorted(jg2_want(subj))
        for nm, kw, ask in (('토큰 없음', {'token': False}, False), ('404(기록 없음)', {'mode': '404'}, True)):
            # 옛 줄(add1 검수 전): p = jg2_open(br, src, subj, PC, **kw)   — 생물 · 지학은 처음부터 토큰이 없으면 그 과목을 못 열어 물리에 머물렀다(값 [577, 577, 0] = 물리 줄 수)
            p = jg2_open_notoken(br, src, subj, PC) if nm == '토큰 없음' else jg2_open(br, src, subj, PC, **kw)
            try:
                st = ewm_wait(p)
                p.wait(1500)
                c = p.ev("() => __EW2.collect()") or {}
                o = p.ev(JG2_OPEN, [codes[0]]) or {}
                c2 = p.ev("() => __EW2.collect()") or {}
                h = p.ev("() => window.__ewmH") or {}
                errs = p.ev("() => (window.__err || []).slice(0, 4)") or []
                n1, n2 = c.get('n') or {}, c2.get('n') or {}
                seen = (n1.get('drawerRows') or 0) > 0 and (n1.get('listItems') or 0) > 0 and jg2_opened(o)   # 줄은 있다(거저 참 아님)
                asked = (h.get('nEx') or 0) >= 1 if ask else h.get('nEx') == 0   # 404 = 요청이 갔다 · 토큰 없음 = 요청도 안 감
                ok &= T('JG2-B3', '%s %s — 표시 0 · 오류 0 · 알림 0(서랍 · 목록 · 지금 목록)' % (subj, nm),
                        seen and asked and n1.get('all') == 0 and n2.get('all') == 0 and not p.errs and not h.get('errs') and not h.get('alerts'),   # window.__err(PP INIT 이 더 일찍 건 귀)는 값으로만 남긴다 — 옛 C4 와 같은 잣대(p.errs · h.errs · 알림)
                        # 옛 줄(add1 검수 전): {'EWM.st': st, '표시 합(열기 전 · 뒤)': [n1.get('all'), n2.get('all')], '서랍 줄 · 카드 · 지금 목록 줄': [n1.get('drawerRows'), n1.get('listItems'), n2.get('trqRows')], '기록 요청 수': h.get('nEx'),
                        {'길': getattr(p, 'ew2way', ''), 'EWM.st': st, '표시 합(열기 전 · 뒤)': [n1.get('all'), n2.get('all')], '서랍 줄 · 카드 · 지금 목록 줄': [n1.get('drawerRows'), n1.get('listItems'), n2.get('trqRows')], '기록 요청 수': h.get('nEx'),
                         '쪽 오류': p.errs[:3], 'h.errs': h.get('errs'), '알림': h.get('alerts'), '__err': errs})
            finally:
                p.close()
    return ok


# ── B-4 — 폭 1440 · 834 · 390: 서랍 줄 높이 무변 · 목록 카드 가로 넘침 0 · 표시 글자 위를 눌러도 그 문제가 열림 ──
def jg2_ov(m):
    return max(m['sw'] - m['cw'], m['msw'] - m['mcw'], m['psw'] - m['vw'])


def jg2_row_ok(h, n):
    if not h or h.get('n') != n or not h.get('on') or not h.get('off'):
        return False
    a, b = h['on'], h['off']
    return a['h'] > 0 and abs(a['h'] - b['h']) <= 0.5 and (a['sw'] - a['cw']) <= max(1, (b['sw'] - b['cw']) + 0.5)


def jg2_card_ok(h, n):
    if not h or not h.get('on') or not h.get('off') or h['on'].get('n') != n:
        return False
    a, b = h['on'], h['off']
    oa, ob = jg2_ov(a), jg2_ov(b)
    return (oa <= 1 or oa <= ob + 0.5) and a['tagR'] <= a['cardR'] + 0.5 and a['tagL'] >= a['cardL'] - 0.5


def jg2_b4(br, src):
    jg2_hdr(src)
    ok = True
    for subj in JG3:
        want = jg2_want(subj)
        codes = sorted(want)
        total = sum(len(v) for v in want.values())
        for dn, dev in DEVS:
            p = jg2_open(br, src, subj, dev)
            try:
                ewm_wait(p)
                jg2_settle(p, total)
                nos = {cd: p.ev("([x]) => __EW2.noOf(x)", [cd]) for cd in codes}
                fo = p.ev(JG2_FOLD, [False])   # 좁은 폭은 접힌 채 시작한다 — 펴고 잰다(펼침 뒤 400ms 유령 click 막이가 풀리게 기다린다)
                p.wait(900)
                hs = {cd: p.ev("([x]) => __EW2.rowH(x)", [nos[cd]]) for cd in codes}
                ok &= T('JG2-B4', '%s %s 서랍 줄 — 한 줄 유지(표시를 껐다 켠 높이 무변 · 가로 넘침 안 늘어남)' % (dn, subj), total > 0 and all(jg2_row_ok(hs[cd], len(want[cd])) for cd in codes),
                        dict({cd: (None if not hs[cd] else {'표시 수': hs[cd].get('n'), '높이(켬 · 끔)': [(hs[cd].get('on') or {}).get('h'), (hs[cd].get('off') or {}).get('h')],
                                                            '제목 폭(켬 · 끔)': [(hs[cd].get('on') or {}).get('ndt'), (hs[cd].get('off') or {}).get('ndt')]}) for cd in codes}, **{'서랍 펴기': fo}))
                pr = {cd: jg2_press(p, 'drawer', cd, nos[cd]) for cd in codes}
                ok &= T('JG2-B4', '%s %s 서랍 줄 누름 — 표시 글자 위를 눌러도 그 문제가 열림' % (dn, subj), total > 0 and all(pr[cd]['ok'] for cd in codes), pr)
                p.ev(JG2_FOLD, [True])   # 목록을 가리지 않게 접는다
                p.wait(900)
                cv = {cd: p.ev("([x]) => __EW2.cardOv(x)", [cd]) for cd in codes}
                ok &= T('JG2-B4', '%s %s 목록 카드 — 가로 넘침 0(표시 때문에 늘지 않음 · 표시가 카드 안에 섬)' % (dn, subj), total > 0 and all(jg2_card_ok(cv[cd], len(want[cd])) for cd in codes),
                        {cd: (None if not cv[cd] or not cv[cd].get('on') else {'넘침 px(켬 · 끔)': [jg2_ov(cv[cd]['on']), jg2_ov(cv[cd]['off'])], '카드 높이(켬 · 끔)': [cv[cd]['on'].get('h'), cv[cd]['off'].get('h')],
                                                                              '표시 가로(왼 · 오른 · 카드 오른)': [cv[cd]['on'].get('tagL'), cv[cd]['on'].get('tagR'), cv[cd]['on'].get('cardR')]}) for cd in codes})
                pc = {cd: jg2_press(p, 'list', cd, nos[cd]) for cd in codes}
                if 'window.G3=' in src:   # ★ 2026-10-09 _task_jagwa_gg3 §A-4(사용자 10/8 18:20 「첫 화면 · 카드 = 제목(.sub · 없으면 코드)만 엶 · 세 과목」) — 표시 글자(제목 밖) 누름 = 안 엶이 뜻한 차 · 값 그대로 INFO · 갈음 칸 = 제목 누름 → 열림(옛 줄은 else 아래 그대로)
                    N('JG2-B4', '%s %s 목록 카드 누름 — 표시 글자 위를 눌러도 그 문제가 열림' % (dn, subj), {'gg3 갈음': '§A-4 첫 화면 카드 = 제목만 엶(표시 글자는 제목 밖)', '값': pc})
                    pt = {cd: jg2_press_title(p, cd, nos[cd]) for cd in codes}
                    ok &= T('JG2-B4', '%s %s 목록 카드 제목 누름 — 표시가 붙어도 그 문제가 열림(gg3 · 카드 = 제목만 엶)' % (dn, subj), total > 0 and all(pt[cd]['ok'] for cd in codes), pt)
                else:
                    ok &= T('JG2-B4', '%s %s 목록 카드 누름 — 표시 글자 위를 눌러도 그 문제가 열림' % (dn, subj), total > 0 and all(pc[cd]['ok'] for cd in codes), pc)
            finally:
                p.close()
    return ok


# ── B-5 — 진짜 기록(읽기만 · 값은 안 적고 수만): 자과 표시 문항 수 = 기록의 자과 틀림 줄(지시서 §0-2 = 18) 중 앱에 있는 문항 수 ──
def jg2_b5(br, src):
    jg2_hdr(src)
    try:
        raw = open(REAL, 'rb').read()
        real = json.loads(raw.decode('utf-8'))
    except Exception as e:
        N('JG2-B5', '진짜 시험 기록 사본을 못 읽음 — 안 잼(--real <exam/꼬까.json 사본>)', str(e).splitlines()[0][:120])
        return not YARD
    rows, drop = ex_rows(real)
    exp = jg2_expect(rows)
    cnt = {}
    for x in rows:
        if x['s'] in ('물리', '생물', '지학'):
            cnt[(x['r'], x['s'])] = cnt.get((x['r'], x['s']), 0) + 1
    tot = sum(cnt.values())
    same = {k: cnt.get(k, 0) for k in SPEC02} == SPEC02 and tot == sum(SPEC02.values())
    N('JG2-B5', '진짜 기록 사본 — 자과 틀림 줄 수(수만) · 지시서 §0-2(= 18)와 %s' % ('같음' if same else '다름'),
      {'합': tot, '지시서 §0-2 합': sum(SPEC02.values()), '회 · 과목별': {'%d회 %s' % k: v for k, v in sorted(cnt.items(), reverse=True)}, '사본 크기(B)': len(raw)})
    ok = True
    shown = {}
    for subj in JG3:
        e = exp[subj]
        lines = sum(len(v) for v in e.values())
        p = jg2_open(br, src, subj, PC, remote=XRemoteReal(raw))
        try:
            st = ewm_wait(p)
            present = p.ev("([cs]) => cs.filter(c => DATA.some(r => String(r[F.CODE]) === c))", [sorted(e)]) or []
            want = {c: e[c] for c in present}
            total = sum(len(v) for v in want.values())
            c = jg2_settle(p, total)
            n1 = c.get('n') or {}
            o = (p.ev(JG2_OPEN, [sorted(want)[0]]) or {}) if want else {}
            c2 = p.ev("() => __EW2.collect()") or {}
            n2 = c2.get('n') or {}
            tr = n2.get('trqRows') or 0
            trq_ok = True if (subj == 'phys' and tr == 0) else (tr > 0 and jg2_eq(c2.get('trq'), want))   # 물리 = 앱이 지금 목록을 안 채운다(JG2-B1 · B2 참고)
            shown[subj] = [lines, total, n1.get('drawer'), n1.get('list'), n2.get('trq')]
            ok &= T('JG2-B5', '%s 진짜 기록 — 표시 문항 수 = 기록의 틀림 줄 중 앱에 있는 수(서랍 · 목록 · 지금 목록)' % subj,
                    total > 0 and jg2_eq(c.get('drawer'), want) and jg2_eq(c.get('list'), want) and jg2_opened(o) and trq_ok,
                    {'EWM.st': st, '기록 줄': lines, '앱에 있음': total, '서랍': n1.get('drawer'), '목록': n1.get('list'), '지금 목록': n2.get('trq'), '지금 목록 줄 수': tr,
                     '앱에 없는 줄': lines - total, '쪽 오류 수': len(p.errs)})
        finally:
            p.close()
    N('JG2-B5', '진짜 기록 — 자과 표시 문항 수 합계(서랍 · 목록 · 기록 줄 · 앱에 있음 · 지시서 §0-2 합)',
      {'서랍': sum((v[2] or 0) for v in shown.values()), '목록': sum((v[3] or 0) for v in shown.values()), '기록 줄': sum(v[0] for v in shown.values()), '앱에 있음': sum(v[1] for v in shown.values()), '지시서 §0-2': sum(SPEC02.values())})
    return ok


# ════════════════════════ 돌림 ════════════════════════
def census_table(census):
    rows = {}
    for r in census:
        key = r.get('자리')
        rows.setdefault(key, {})[r.get('기기')] = r
    out = []
    for place, d in rows.items():
        cells = []
        for dn, _ in DEVS:
            r = d.get(dn)
            cells.append('—' if not r else ('%s 표시 %s%s' % ('PASS' if r.get('ok') else 'FAIL', r.get('표시', '?'), '' if r.get('ok') else ' (' + str(r.get('왜') or '') + ')')))
        out.append('%-32s | %s' % (place, ' | '.join(cells)))
    return out


def webkit_try(pw):
    try:
        return pw.webkit.launch()
    except Exception as e:
        N('WK', 'WebKit 안 잼', str(e).splitlines()[0][:160])
        return None


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    srcs = {a: app_src(a, NEWA[a]) for a in APPS}
    if QJ.GATE:
        bases = {a: app_src(a, BASE) for a in APPS}
    else:
        # regress · smoke — 바탕(afd6339) 앱 글을 안 푼다(git:show-app 0 · 첫 화면 시각의 바탕 중앙값 = 기준 스냅샷)
        # 옛 줄(10/4 · jo 만): bases = {a: (None if a == 'jo' else app_src(a, BASE)) for a in APPS}
        bases = {a: None for a in APPS}   # ★ _task_qa_slim2(10/8) — 민법 · 자과 사슬도
    if YARD:
        srcs = dict(bases)
    print('══ exam_wrong_mark %s · 바탕 %s · 시험 기록 %s(md5 %s)' % ('헛잣대' if YARD else '새 판', BASE, os.path.relpath(FX, HERE), hashlib.md5(EXB).hexdigest()[:8]))
    for a in APPS:
        print('   %s 앱 md5(LF) %s · 바탕 %s' % (NAME[a], md5lf(srcs[a]), md5lf(bases[a]) if (QJ.GATE or bases[a] is not None) else '(regress — 안 읽음)'))
    N('C0', '틀림 줄(시험 기록 · 하네스 거르기)', ['%s %d-%d' % (x['s'], x['r'], x['i']) for x in WR])
    N('C0', '뺀 줄', ['%s %d-%d %s' % (x['s'], x['r'], x['i'], x['why']) for x in WX])
    if QJ.REGRESS:
        N('C0', 'regress 갈래(jo)', '새 판만(%s) · 바탕(%s · JG2 %s) 판은 안 띄움 · 첫 화면 시각 = 새 판 1 번(JG2-B2 = 몸풀기 1 + 3 번) + 바탕 중앙값은 기준 스냅샷(QJ.base) · 헛잣대(JG2-B1 바탕) 끔' % (','.join(APPS), BASE, JGBASE))   # ★ _task_qa_slim2(10/8) — 민법 · 자과도(옛 글: 「… · 민법 · 자과 실행은 gate 그대로」)
    got, times, census = {}, {}, {'jo': [], 'mb': [], 'jg': []}
    with sync_playwright() as pw:
        PWH['pw'] = pw   # (add1 검수) JG2-B2 WebKit 길이 쓴다
        br = pw.chromium.launch()
        steps = []
        if 'jo' in APPS:
            steps += [('C1-jo', lambda: jo_c1(br, srcs['jo'], 'c1j')), ('C2-jo', lambda: jo_c2(br, srcs['jo'], 'c2j')),
                      ('C3-jo', lambda: jo_c3(br, srcs['jo'], 'c3j', census['jo'])), ('C4-jo', lambda: jo_c4(br, srcs['jo'], bases['jo'], 'c4j'))]
        if 'mb' in APPS:
            steps += [('C1-mb', lambda: mb_c1(br, srcs['mb'], 'c1m')), ('C2-mb', lambda: mb_c2(br, srcs['mb'], 'c2m')),
                      ('C3-mb', lambda: mb_c3(br, srcs['mb'], 'c3m', census['mb'])), ('C4-mb', lambda: mb_c4(br, srcs['mb'], bases['mb'], 'c4m'))]
        if 'jg' in APPS:
            steps += [('C1-jg', lambda: jg_c1(br, srcs['jg'], 'c1g')), ('C2-jg', lambda: jg_c2(br, srcs['jg'], 'c2g')),
                      ('C3-jg', lambda: jg_c3(br, srcs['jg'], 'c3g', census['jg'])), ('C4-jg', lambda: jg_c4(br, srcs['jg'], bases['jg'], 'c4g'))]
        if 'jg' in APPS:   # JG2(uid_unify_add1) — 서랍 줄 · 목록 카드 · 지금 목록 줄 표시 · 위 C1~C4 는 그대로 · --only JG2 로 이 칸만 · --yardstick 이면 바탕(--jgbase)을 새 판 자리에(B3 는 해당 없음)
            _jg2 = (lambda: jg2_base_src()) if YARD else (lambda: srcs['jg'])
            steps += [('JG2-B1', lambda: jg2_b1(br, _jg2())), ('JG2-B2', lambda: jg2_b2(br, _jg2()))]
            if YARD:
                if not ONLY or any('JG2-B3'.startswith(o) for o in ONLY):
                    N('JG2-B3', '헛잣대 해당 없음', '바탕엔 표시가 없어 「기록 못 받음 = 표시 0」을 가를 수 없다')
            else:
                steps += [('JG2-B3', lambda: jg2_b3(br, _jg2()))]
            steps += [('JG2-B4', lambda: jg2_b4(br, _jg2())), ('JG2-B5', lambda: jg2_b5(br, _jg2()))]
        for g, fn in steps:
            if ONLY and not any(g.upper() == o or g.upper().startswith(o) for o in ONLY):
                continue
            if QJ.SMOKE and g not in ('C1-jo', 'C4-jo', 'C1-mb', 'C4-mb', 'C1-jg', 'C4-jg'):
                continue   # smoke = 조판기 C1(앱 표 셋) · C4(토큰 없음) 만 · ★ (10/8) 민법 C1-mb(앱 표) · C4-mb(토큰 없음) · 자과 C1-jg(물리 앱 표) · C4-jg(토큰 없음 물리)
            if YARD and g.startswith('C4'):
                N(g, '헛잣대 해당 없음', '바탕엔 표시가 없어 「기록 못 받음 = 표시 0」을 가를 수 없다')
                continue
            print('── %s' % g, flush=True)
            t1 = time.time()
            try:
                got[g] = bool(fn())
            except Exception as e:
                got[g] = False
                T(g, '돌다 멈춤', False, str(e).splitlines()[0][:300])
            times[g] = round(time.time() - t1)
            print('   (%s %d초)' % (g, times[g]), flush=True)
        br.close()
        if 'webkit' in ENGS and not YARD and not QJ.SMOKE and (QJ.GATE or 'jo' in APPS or 'mb' in APPS):   # regress — WebKit 칸은 jo · mb C3 폰만(자과 사슬 --apps jg 는 띄움만 하던 헛띄움 → 0)
            wk = webkit_try(pw)
            if wk:
                try:
                    for a, fn in (('jo', lambda c: jo_c3_dev(wk, srcs['jo'], '폰390-wk', PHONE, c)), ('mb', lambda c: mb_c3_dev(wk, srcs['mb'], '폰390-wk', PHONE, c))):
                        if a in APPS:
                            got['C3-%s-wk' % a] = bool(fn(census[a]))
                finally:
                    wk.close()
    lines = []
    for a in APPS:
        if census[a]:
            print('\n══ 자리 전수 표 — %s' % NAME[a])
            print('%-32s | %s' % ('자리', ' | '.join(dn for dn, _ in DEVS)))
            for ln in census_table(census[a]):
                print(ln)
                lines.append('%s | %s' % (NAME[a], ln))
    print('\n══ 요약 (%.0f초)%s' % (time.time() - t0, ' — 헛잣대' if YARD else ''))
    summ = []
    for g in got:
        cells = [r for r in RES if r[0] == g and r[2] is not None]
        nf = sum(1 for r in cells if not r[2])
        verdict = (('FAIL(헛잣대 통과)' if not got[g] else 'PASS(헛잣대 실패)') if YARD else ('PASS' if got[g] else 'FAIL'))
        s = '  %-10s %s (%d 칸 중 FAIL %d · %s초)' % (g, verdict, len(cells), nf, times.get(g, '-'))
        print(s)
        summ.append(s)
    os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8', newline='\n') as f:
        for r in RES:
            d = r[3] if isinstance(r[3], str) else json.dumps(r[3], ensure_ascii=False, default=str)
            f.write('%s | %s · %s | %s\n' % ('INFO' if r[2] is None else ('PASS' if r[2] else 'FAIL'), r[0], r[1], d))
        f.write('\n'.join(lines + summ) + '\n')
    print('결과 → %s' % OUTF)


if __name__ == '__main__':
    main()
