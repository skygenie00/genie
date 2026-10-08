# -*- coding: utf-8 -*-
"""폰 목록 단원 칩 넘침 고침 관문(2026-09-29 · _patch_jagwa_chipwrap.py)

  python _harness_jagwa_chipwrap.py [--new <앱>] [--eng chromium,webkit] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE(헛잣대) = genie HEAD(바로 앞 인도판 = jagwa_search)
  틀 = _harness_jagwa_phone_win 의 Pg(폰 390×844 손가락 · PC 1553×900 마우스 · 같은 출처 데이터 · 기록 PUT 가로챔)
  C1 폰 세 과목 — 머리 펼친 뒤 목록 안 가로 넘침 0 · 쪽 scrollWidth = clientWidth(바탕 생물 = 넘침)
  C2 폰 목록 글자(textContent) = 바탕
  C3 폰 생물 가장 긴 단원 칩 — 화면 안 · 칩 안 두 줄 이상 · 손가락 톡 → 그 단원으로 거름(FL.unit = data-unit)
  C4 PC 칩 자리·크기 = 바탕 · 목록 글자 = 바탕
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — 자리 = getBoundingClientRect · 가림 = elementFromPoint
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import io, json, os, sys, time, hashlib
import re   # ★ uid_unify 옛 잣대 고침 — NEW 앱 글에서 §G-1 새 판(ynUid)을 가린다(main)
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_chipwrap_result.txt'))
from playwright.sync_api import sync_playwright   # noqa: E402
RES = []
# ★ uid_unify 옛 잣대 고침(2026-10-04 · 근거 gigu/_task_jagwa_uid_unify.md §G-1 · §G-2 · _add1) ──────────────────────────────────────────────────────────────────────────────
#   목록 줄(.item .meta)에서 새 판이 **뜻해서** 바꾼 것 셋 = ① §G-1 카드 층 기출 uid 줄(^[BG]\d\d-\d+-\d+$)의 .sub(titleOf = 「NN회 N번」)를 안 그림(사용자 10/4 16:45 「uid 랑 중복되니까 nn회 n번 없애」)
#   ② §G-2 카드 층(HASBOOK) 목록 줄의 「N회독」 칩을 안 그림(앱 `(rep&&!HASBOOK)` · 물리 줄은 그대로) ③ _add1 시험 틀림 .ewmt 를 더함(앱 `${kindTag(r)}${ewmTagHTML(r)}` · 데이터가 있을 때만 — 이 하네스의 데이터에는 꼬까 시험 틀림 파일이 없어 늘 0).
#   그래서 C2(폰 목록 글자 = 바탕) · C4(PC 칩 자리·크기 · 목록 글자 = 바탕)는 **새 판(NEW 앱 글에 ynUid)과 맞댈 때만** 바탕(옛 판 eb1113e · ynUid 없음) 쪽 DOM 에서 같은 ①②를 걷고(칩 자리는 걷은 DOM 으로 다시 잰다) ·
#   새 판 쪽에서는 ③ 만 걷고 맞댄다 — 새 판에 .sub · N회독이 남아 있으면 바탕에서만 걷었으니 어긋나 FAIL(걷지 않은 것도 잡는다 · 걷은 개수는 값에 남긴다). 옛 판끼리(바탕 4754b1d 의 저장본)는 아무것도 안 걷음 = 옛 잣대 그대로.
#   ⚠ 생물 §G-1 은 **결정 대기** — 생물 기출 uid 270 중 260 은 뒷자리가 문번이 아니라(지시서 §G-1 의 「uid 회·번 = 데이터 회차·문번」 은 지학만 맞다) .sub 를 걷으면 연도·문번이 사라진다.
#   G1_BIO = False 면 생물 줄은 .sub 를 걷지 않고 바탕과 그대로 맞댄다(= 새 판이 .sub 를 걷은 만큼 FAIL 로 남는다 · 결정이 「지학만」이면 이대로 맞다). 결정이 「지시서대로(생물도 걷음)」면 아래 한 줄을 True 로 바꾼다(손으로 재 볼 때는 실행에 --g1bio).
G1_BIO = '--g1bio' in sys.argv
NEWG1 = False   # main() 이 NEW 앱 글에서 가린다 — 앱 글에 ynUid(§G-1 새 판)가 있으면 참

CJS = """
window.__C={
 over(){const W=document.documentElement.clientWidth,L=document.getElementById('list'),bad=[];
   if(L)L.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>W+0.5)bad.push(String(e.className||e.tagName).slice(0,24)+':'+Math.round(r.right))});
   return {W,sw:document.documentElement.scrollWidth,n:bad.length,first:bad.slice(0,4),items:L?L.querySelectorAll('.item').length:0}},
 /* ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2: 물리(HASBOOK 거짓)만 미리보기 칸(.prev · .pvfig)을 두 판 모두 떼고 · 칩 세로 자리는 제 줄(.item) 위 끝 기준(줄이 길어져도 칩 자리 무변을 잰다 · 숨은 칩(크기 0)은 옛 값 그대로) · 카드 층은 옛 잣대 그대로 */
 ph(){return typeof HASBOOK!=='undefined'&&!HASBOOK},
 /* ★ uid_unify 옛 잣대 고침(2026-10-04 · §G-1 · §G-2 · _add1) — 새 판과 맞댈 때만(window.__CG1) 목록 줄에서 뜻한 차이만 걷는다 · 아니면 아무것도 안 함(옛 잣대 그대로)
    · 어느 판이든 .ewmt(시험 틀림 표시 · _add1 이 더한 것)
    · 옛 판(바탕 · typeof ynUid 없음) 카드 층(HASBOOK)만: 기출 uid 줄(window.__CG1SUB 가 참인 과목)의 .meta > .sub(§G-1) · 「N회독」 .tag 칩(§G-2) — 새 판(ynUid 있음)은 이미 안 그렸으니 걷지 않는다(남았으면 어긋나 FAIL)
    걷은 개수 = window.__CUTN */
 cut(c){window.__CUTN=0;if(!window.__CG1||!c)return 0;let n=0;
   c.querySelectorAll('.ewmt').forEach(x=>{x.remove();n++});
   /* ★ 2026-10-07 (_task_jagwa_phys_win §A-36 · §A-37 ㊴) — 물리 목록 「기출」 칩 자리에 「V3」 글자(.vno) · 「볼트 N」 칩(.tag.vlt) 걷음 = 뜻한 차 →
      물리(HASBOOK 거짓)만 두 판 모두 그 칸(.vno · .tag.vlt · 기출 딱지)을 걷고 맞댄다(칩 자리는 걷은 DOM 으로 다시 잰다 · 카드 층은 무변) */
   if(__C.ph())c.querySelectorAll('.item .meta .vno,.item .meta .tag').forEach(x=>{if(x.classList.contains('vno')||x.classList.contains('vlt')||/^(기출|타기출|확인|예상)$/.test(String(x.textContent||'').trim())){x.remove();n++}});
   if(typeof ynUid!=='function'&&typeof HASBOOK!=='undefined'&&HASBOOK)c.querySelectorAll('.item').forEach(it=>{
     if(window.__CG1SUB&&/^[BG][0-9][0-9]-[0-9]+-[0-9]+$/.test(String(it.dataset.uid||'')))it.querySelectorAll('.meta > .sub').forEach(x=>{x.remove();n++});
     it.querySelectorAll('.meta > .tag').forEach(x=>{if(/^[0-9]+회독$/.test(String(x.textContent||'').trim())){x.remove();n++}})});
   window.__CUTN=n;return n},
 cutLive(){return __C.cut(document.getElementById('list'))},   /* 살아 있는 #list 에서 걷는다 — 칩 자리(getBoundingClientRect)를 걷은 DOM 으로 재려고 */
 /* 옛: text(){const L=document.getElementById('list');if(!L)return '';if(!__C.ph())return String(L.textContent||'');const c=L.cloneNode(true);c.querySelectorAll('.prev,.pvfig').forEach(x=>x.remove());return String(c.textContent||'')}, */
 text(){const L=document.getElementById('list');if(!L)return '';if(!__C.ph()&&!window.__CG1)return String(L.textContent||'');const c=L.cloneNode(true);if(__C.ph())c.querySelectorAll('.prev,.pvfig').forEach(x=>x.remove());__C.cut(c);return String(c.textContent||'')},
 tags(){const ph=__C.ph();return [...document.querySelectorAll('#list .item .meta .tag')].slice(0,600).map(e=>{const r=e.getBoundingClientRect(),it=(ph&&(r.width||r.height))?e.closest('.item'):null,t0=it?it.getBoundingClientRect().top:0;return [Math.round(r.left*10)/10,Math.round((r.top-t0)*10)/10,Math.round(r.width*10)/10,Math.round(r.height*10)/10]})},
 longest(){const t=[...document.querySelectorAll('#list .item .meta .tag.unit')];if(!t.length)return null;
   const e=t.reduce((a,b)=>(String(b.textContent).length>String(a.textContent).length?b:a));
   e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),cs=getComputedStyle(e);
   const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.4;
   const inner=r.height-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom)-parseFloat(cs.borderTopWidth)-parseFloat(cs.borderBottomWidth);
   return {txt:String(e.textContent),unit:e.dataset.unit||'',right:Math.round(r.right),h:Math.round(r.height*10)/10,lines:Math.round(inner/lh),W:document.documentElement.clientWidth,hit:__W.hit(e)}},
 unitNow(){return (typeof FL!=='undefined'&&FL)?String(FL.unit||''):null}
};
"""


def cg1(q, subj):
    """★ uid_unify 옛 잣대 고침 — 새 판(NEWG1)과 맞댈 때만 목록 줄에서 뜻한 차이를 걷게 이 페이지에 표시를 둔다(아니면 옛 잣대 그대로)
       window.__CG1 = 새 판과 맞대는 중 · window.__CG1SUB = 이 과목은 §G-1 .sub 걷음을 허용하나(지학 = 허용 · 생물 = G1_BIO(결정 대기) · 물리 = 해당 없음)"""
    sub = (subj == 'earth') or (subj == 'bio' and G1_BIO)
    q.ev("()=>{window.__CG1=%s;window.__CG1SUB=%s}" % ('true' if NEWG1 else 'false', 'true' if sub else 'false'))


def cutdict(n, b, subj):
    """새 판과 맞댈 때만(물리 뺌) — 이 칸에서 걷은 개수(NEW · 바탕)와 생물 §G-1 결정 대기 표시. 값에 남겨 걷은 만큼이 보이게 한다"""
    if not NEWG1 or subj == 'phys':
        return {}
    d = {'걷음 NEW·바탕': [n.get('cut'), b.get('cut')]}
    if subj == 'bio' and not G1_BIO:
        d['결정 대기'] = '생물 G-1(기출 uid 줄 .sub 걷음) — 걷지 않고 맞댄다 · G1_BIO=True 로 바꾸면 걷고 맞댄다'
    return d


def cutinfo(n, b, subj):
    d = cutdict(n, b, subj)
    return [d] if d else []


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, (detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False, default=str))[:420]), flush=True)


def md(t):
    return hashlib.md5(t.encode('utf-8')).hexdigest()[:8] + ':' + str(len(t))


NEWPW = False   # ★ 2026-10-08 (_task_jagwa_phys_win §A-37 · §A-40) 새 판 표지 — main 에서 NEW 앱 글에 function pfDecor 가 있으면 참


def _tn(t, subj):   # ★ 2026-10-08 (_task_jagwa_phys_win §A-37 · §A-40) 새 판 표지 있을 때만 · 두 판 모두 — 빈칸 접기(세 과목 · row() 템플릿 「볼트 N」 줄 빠짐) · 단원 머리 「🃏📋」 뒤 「공식」 칩 뗌(물리만)
    # 옛 줄: if not NEWPW or subj != 'phys' or not isinstance(t, str):
    if not NEWPW or not isinstance(t, str):
        return t
    # 옛 줄: return re.sub(r'\s+', ' ', t.replace('🃏📋공식', '🃏📋')).strip()
    return re.sub(r'\s+', ' ', t.replace('🃏📋공식', '🃏📋') if subj == 'phys' else t).strip()   # ★ 10/8 02:4x — 생물·지학도 같은 템플릿 줄 빠짐(생물 C2·C4 바탕 PASS → 새 판 FAIL 까닭)


def open_head(q):
    q.ev(CJS)
    fb = q.ev("()=>__W.at('#fFoldBtn')")
    if fb and q.ev("()=>document.body.classList.contains('fold')"):
        q.press(fb, 700) if QC.GATE else (q.press(fb, 0), QC.until(q.pg, "()=>!document.body.classList.contains('fold')", 700, '머리 펼침(body.fold 풀림)'))   # regress — 같은 상한의 표지
    q.wait(500) if QC.GATE else QC.sleep(500, '펼친 뒤 목록 다시 그림 · 넘침 잴 자리 안착 — 표지 없음', q.pg)


def phone(br, eng, subj):
    def f(q):
        open_head(q)
        cg1(q, subj)   # ★ uid_unify 옛 잣대 고침 — 새 판과 맞댈 때만 걷는 표시(아니면 옛 잣대 그대로)
        # 옛 줄: o = {'over': q.ev("()=>__C.over()"), 'text': md(q.ev("()=>__C.text()")), 'fold': q.ev("()=>document.body.classList.contains('fold')")}
        o = {'over': q.ev("()=>__C.over()"), 'text': md(_tn(q.ev("()=>__C.text()"), subj)), 'fold': q.ev("()=>document.body.classList.contains('fold')")}
        o['cut'] = q.ev("()=>window.__CUTN||0")   # 이 쪽 목록 글자에서 걷은 개수(.text() 가 마지막으로 걷은 값 · 아무것도 안 걷으면 0)
        if subj == 'phys':   # ★ 2026-10-07 (_task_jagwa_phys_win 회귀) 진단만 · 판정 무변 — 물리 목록 글자 날것(걷은 뒤 · 맞대기에 안 씀 · 갈리면 main 이 TEMP 에 떠 둔다)
            o['raw'] = q.ev("()=>__C.text()")
        if subj == 'bio':
            lg = q.ev("()=>__C.longest()")
            o['long'] = lg
            if lg and lg.get('hit') and lg['hit'].get('on'):
                q.press(lg['hit'], 900) if QC.GATE else (q.press(lg['hit'], 0), QC.until(q.pg, "u=>typeof FL!=='undefined'&&!!FL&&String(FL.unit||'')===u", 900, '단원 칩 톡 → FL.unit', lg.get('unit') or ''))   # regress — 같은 상한의 표지
                o['unitAfter'] = q.ev("()=>__C.unitNow()")
        return o
    return JG.both(br, eng, subj, True, f) if QC.GATE else _rg_both(br, eng, subj, True, f)   # regress — 새 판만 · 바탕 자리 = 기준 스냅샷


def tags_eq(a, b, subj):
    """★ physprev(10/1) — 물리 칩 세로 자리 = 제 줄 위 끝 기준 · 1px 안 차는 같은 자리(줄 높이 소수 반올림 차) · 카드 층은 옛 잣대(글자까지 같음) 그대로"""
    if subj != 'phys':
        return a == b
    return len(a) == len(b) and all(x[0] == y[0] and x[2] == y[2] and x[3] == y[3] and abs(x[1] - y[1]) <= 1 for x, y in zip(a, b))


def pc(br, eng, subj):
    def f(q):
        q.ev(CJS); q.wait(300)
        # 옛 줄: return {'tags': q.ev("()=>__C.tags()"), 'text': md(q.ev("()=>__C.text()")), 'over': q.ev("()=>__C.over()")}
        cg1(q, subj)   # ★ uid_unify 옛 잣대 고침 — 새 판과 맞댈 때만 걷는 표시(아니면 옛 잣대 그대로)
        ov = q.ev("()=>__C.over()")   # 넘침은 걷기 앞에서 잰다(옛 값 그대로)
        cn = q.ev("()=>__C.cutLive()")   # 새 판과 맞댈 때만 DOM 에서 뜻한 차이를 걷는다(그 밖엔 0) — 칩 자리는 걷은 DOM 으로 다시 잰다
        # 옛 줄: return {'tags': q.ev("()=>__C.tags()"), 'text': md(q.ev("()=>__C.text()")), 'over': ov, 'cut': cn}
        return {'tags': q.ev("()=>__C.tags()"), 'text': md(_tn(q.ev("()=>__C.text()"), subj)), 'over': ov, 'cut': cn}
    return JG.both(br, eng, subj, False, f) if QC.GATE else _rg_both(br, eng, subj, False, f)   # regress — 새 판만 · 바탕 자리 = 기준 스냅샷


# ── _task_qa_slim2(10/8) regress 도우미 — 이름이 `_rg` 로 시작하는 것 = gate 에서 안 쓰는 갈래 ──
def _rg_both(br, eng, subj, phone, f):
    """regress — JG.both 를 NEW 한 벌만(whos) · BASE 자리 = 기준 스냅샷(앞 인도판 새 판의 같은 칸 값: 목록 글자 md5 · 칩 자리 · 긴 칩 글자) · 바탕 넘침(C1-헛 재료)은 없음
    smoke 는 C1 · Z 만 재므로 스냅샷에 아무것도 안 적는다"""
    QC.launch('new')   # 셈(§B-4) — JG.both 가 NEW 문맥 하나를 띄운다(JG 는 QC 를 안 부른다 · 바탕은 gate 의 JG.both 에서만)
    r = JG.both(br, eng, subj, phone, f, whos=('NEW',))
    n = r.get('NEW') or {}
    b = {'cut': None, 'over': {'n': None, 'sw': None, 'W': None, '기준': '바탕 안 띄움(regress)'}}
    if not QC.SMOKE:
        tag = '%s@%s/%s' % (subj, eng, 'phone' if phone else 'pc')
        if 'text' in n:
            b['text'] = QC.base('text.' + tag, n['text'])
        if 'tags' in n:
            b['tags'] = QC.base('tags.' + tag, n['tags'])
        if 'long' in n:
            b['long'] = {'txt': QC.base('long.txt.' + tag, (n.get('long') or {}).get('txt'))}
    r['BASE'] = b
    return r


def main():
    JG.APPS['NEW'] = io.open(NEWF, encoding='utf-8').read()
    global NEWG1   # ★ uid_unify 옛 잣대 고침 — NEW 앱 글에 ynUid 가 있으면 §G-1·§G-2 새 판(바탕 4754b1d 와 인도 앞 판 eb1113e 는 없다)
    NEWG1 = re.search(r'\b(?:var|let|const|function)\s+ynUid\b', JG.APPS['NEW']) is not None
    global NEWPW
    NEWPW = 'function pfDecor(' in JG.APPS['NEW']   # ★ 2026-10-08 (_task_jagwa_phys_win §A-37 · §A-40) 새 판 표지
    if QC.GATE:   # regress — 바탕(eb1113e · git show) 풀기 0
        JG.APPS['BASE'] = JG.git_PW('show', 'eb1113e:jagwa/index.html').decode('utf-8')   # ★ A-6(d) 9/30 _task_qa_baseline — 헛잣대 바탕 = 인도 앞 판 eb1113e(jagwa_search · 인도 결과 머리 「바탕 genie HEAD eb1113e」) · 인도(95cc766) 뒤 HEAD 는 이 판 자신
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in (ENGS if not QC.SMOKE else ([e for e in ENGS if e == 'chromium'] or ENGS[:1])):   # smoke — chromium 한 판
            br = getattr(pw, eng).launch()
            try:
                for subj in (('phys', 'bio', 'earth') if not QC.SMOKE else ('bio',)):   # smoke — 생물 폰 한 과목(C1 · Z)
                    r = phone(br, eng, subj)
                    n, b = r['NEW'], r['BASE']
                    T('C1', '%s 폰 %s — 머리 펼친 뒤 목록 안 가로 넘침 0 · 쪽 scrollWidth = clientWidth' % (eng, subj),
                      n['over']['n'] == 0 and n['over']['sw'] <= n['over']['W'] and not n['fold'] and n['over']['items'] > 0,
                      {'NEW': n['over'], '바탕': b['over']})
                    if QC.SMOKE:   # smoke — C1 · Z 만(아래 Z 칸과 같은 셈)
                        T('Z', '%s 폰 %s 오류 0' % (eng, subj), not r['NEW_err'], r['NEW_err'][:3])
                        continue
                    if subj == 'bio' and QC.GATE:   # 관문만 — 헛잣대(바탕 폰 생물 넘침)
                        T('C1-헛', '%s 헛잣대 바탕 — 폰 생물 목록이 가로로 넘침' % eng, b['over']['n'] > 0 and b['over']['sw'] > b['over']['W'], b['over'])
                    # 옛 줄: T('C2', '%s 폰 %s — 목록 글자 = 바탕' % (eng, subj), n['text'] == b['text'], [n['text'], b['text']])
                    T('C2', '%s 폰 %s — 목록 글자 = 바탕' % (eng, subj), n['text'] == b['text'], [n['text'], b['text']] + cutinfo(n, b, subj))
                    if subj == 'phys' and n['text'] != b['text'] and QC.GATE:   # ★ 2026-10-07 (_task_jagwa_phys_win 회귀) 진단만 · 판정 무변 — 갈린 두 글을 TEMP 에(무엇이 갈렸는지 줄로 가름)
                        _hd = JG.git_PW('rev-parse', '--short', 'HEAD').decode().strip()
                        for _k, _v in (('new', n), ('base', b)):
                            open(os.path.join(os.environ.get('TEMP', '.'), 'cw_%s_%s_phys_%s.txt' % (_hd, eng, _k)), 'w', encoding='utf-8').write(str(_v.get('raw')))
                    if subj == 'bio':
                        lg, lb = n.get('long') or {}, b.get('long') or {}
                        T('C3', '%s 폰 생물 가장 긴 단원 칩 — 화면 안 · 칩 안 두 줄 이상 · 손가락 톡 → 그 단원으로 거름' % eng,
                          bool(lg) and lg['right'] <= lg['W'] and lg['lines'] >= 2 and lg['hit']['on'] and n.get('unitAfter') == lg['unit'] and lg['txt'] == lb.get('txt'),
                          {'NEW': {k: lg.get(k) for k in ('txt', 'right', 'h', 'lines', 'W')}, '톡 뒤 FL.unit': n.get('unitAfter'), '단원': lg.get('unit'),
                           '바탕': {k: lb.get(k) for k in ('right', 'h', 'lines')}, '바탕 톡': b.get('unitAfter')})
                    T('Z', '%s 폰 %s 오류 0' % (eng, subj), not r['NEW_err'], r['NEW_err'][:3])
                    rp = pc(br, eng, subj)
                    T('C4', '%s PC %s — 칩 자리·크기 = 바탕(%d 칩) · 목록 글자 = 바탕 · 넘침 0' % (eng, subj, len(rp['NEW']['tags'])),
                      tags_eq(rp['NEW']['tags'], rp['BASE']['tags'], subj) and rp['NEW']['text'] == rp['BASE']['text'] and rp['NEW']['over']['n'] == 0 and len(rp['NEW']['tags']) > 0,
                      # 옛 줄: {'다른 칩': [i for i, (x, y) in enumerate(zip(rp['NEW']['tags'], rp['BASE']['tags'])) if not tags_eq([x], [y], subj)][:5], '글자': [rp['NEW']['text'], rp['BASE']['text']]})
                      {**{'다른 칩': [i for i, (x, y) in enumerate(zip(rp['NEW']['tags'], rp['BASE']['tags'])) if not tags_eq([x], [y], subj)][:5], '글자': [rp['NEW']['text'], rp['BASE']['text']]}, **cutdict(rp['NEW'], rp['BASE'], subj),
                         **({'첫 다른 칩(새·바탕)': next(([x, y] for x, y in zip(rp['NEW']['tags'], rp['BASE']['tags']) if not tags_eq([x], [y], subj)), None)} if subj == 'phys' else {})})   # ★ 2026-10-08 (_task_jagwa_phys_win) 진단만 — 첫 다른 칩 값
            finally:
                br.close()
    npass = sum(1 for x in RES if x[2]); nfail = sum(1 for x in RES if not x[2])
    print('\n== PASS %d · FAIL %d · %.0f초' % (npass, nfail, time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as fo:
        fo.write('\n==== %s · chipwrap · NEW %s · 바탕 eb1113e · genie HEAD %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF),
                 JG.git_PW('rev-parse', '--short', 'HEAD').decode().strip() if QC.GATE else '(regress · git 0)', ','.join(ENGS)))
        for g, nm, ok, d in RES:
            fo.write('%s | %s · %s | %s\n' % ('PASS' if ok else 'FAIL', g, nm, (d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str))[:1200]))
        fo.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
