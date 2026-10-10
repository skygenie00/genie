# -*- coding: utf-8 -*-
r"""_task_cloud_batch_1010 로컬 몫 — 민법OX 한 판(클라우드 ① 76a3a03 · 합친 후보 56836b8)의 WebKit 칸 관문(앱은 고치지 않는다)

  python _harness_ox_batch_webkit.py [--mode gate|regress|smoke] [--new <앱>] [--base <판 = 7299ec3>] [--base2 <판 = 56836b8>] [--base3 <판 = d48e4a8>] [--only W1,W2,…]
                                     [--dev 폰,iPad] [--w5-eng webkit,chromium] [--w6-eng webkit,chromium] [--spd <studyplandata>] [--data-rev <판 = 3065ca0 · '' = 작업트리>]
                                     [--rec-rev <판 = ddc6ea7>] [--tw <Tailwind 사본>] [--res <결과>] [--shots <그림>]

  NEW  = genie 작업트리 minbeop/index.html(GENIE_ROOT) · BASE = 바탕 7299ec3(헛잣대 — gate 만 · W1 · W2 · W4 · W5 FAIL 이어야)
  BASE2 = 56836b8(합친 후보 · ox_fix 앞 판 — gate 만 · W5 만) — W5 ② iPad 헛잣대는 이 판이다: 7299ec3 은 띠가 없어 「잘못 열림 0」 이라
          그 칸의 헛잣대가 못 된다(10/10 [채팅] 03:50 ㉠ · 56836b8 = iPad ✎ +3px 톡에 아랫줄 칸 열림) · W5 ① 「겉모양 무변」 도 이 판과 그림으로 맞댐
  BASE3 = d48e4a8(main · ox_fix 들어간 판 · ox_del 앞 — gate 만 · W6 만) — 「× 연결 끊기」 가 되묻지 않고 바로 끊는 판 = W6 헛잣대(사용자 10/10 08:3x 「더하기」)
  엔진 = WebKit 하나(playwright webkit = iPhone · iPad Safari 엔진) — 클라우드 관문 셋(_harness_ox_search_all · _queue_compare · _ggref_phone)은 Chromium 만이라 못 잰 칸
  기기 = 폰 390×844 · iPad 820×1180(has_touch · is_mobile(되면) · DPR 2)
  누름 = touchscreen.tap(**진짜 터치**) · 굴림 = 마우스 휠(되면 · 굴림 통 보이는 가운데) 아니면 그 통 scrollTop 을 끝으로 + scroll 사건
        — playwright 웹킷은 톡만 진짜 터치(손가락 끌기 · 밀기 없음 · CDP 없음 = 도구 한계) · 모바일 웹킷(is_mobile)은 휠도 안 받는다
          (「Mouse wheel is not supported in mobile WebKit」 · 10/10 잼) → 모바일 칸은 scrollTop · W1 은 같은 칸을 비모바일 웹킷(has_touch · 같은 크기)
          휠로 한 번 더 돈다(믿는 입력 굴림 길) · 어느 쪽으로 굴렸는지 칸마다 적는다
  데이터 = studyplandata --data-rev 판의 minbeop/*(git show · 읽기만 · 클라우드 관문과 같은 3065ca0) · W4 기록 = --rec-rev(ddc6ea7) ·
        가짜 GitHub contents · PUT 메모리 = OL(_ox_live.py) 그대로
  網 = route 는 http(s) 만(웹킷은 blob: 도 route 에 태운다) · 127.0.0.1 · 가짜 GitHub 밖은 OL 처럼 끊되 Tailwind cdn 만 그대로(본 PC · --tw 면 <style>) ·
        Tailwind 실림은 WK 환경 줄에 찍는다(tailwind · 검색 결과 통 max-h · overflow) — 안 실리면 W1 처음 100 · W5 줄 꼴이 거짓으로 갈린다
  ⚠ 개인 문항 · 해설 · 근거 글은 출력하지 않는다(D11) — 문항 ID · 번호 · 색 · 수 · 폭만
  칸:
    W1 첫 화면 검색 「대위」(runSearch) — 검색 칸 진짜 톡 · 타자 → 셈 글 = 기대(앱 거르기 식을 하네스가 따로 셈) · 처음 100 줄 · 「상위 N건만」 글 0 ·
       결과 통 끝까지 굴림 → 붙은 줄 = 기대 · 차례 = 기대 · 겹침 0(같은 ID 두 번 · 줄 네모 겹침) · 끝 줄 진짜 톡 = 그 문항 팝업
       + 같은 칸 휠 갈래(비모바일 웹킷 · 휠로만 굴렸어야 PASS)
    W2 연결 창 「대리」(lwOpen 찾기 칸 진짜 톡 · lwFind) · 근거 창 「취소」(문항 팝업 🔍 진짜 톡 · linkSearch geunge) — 셈 보임 · 처음 100 ·
       끝까지 굴려 다 붙음 · 차례 = 기대 · (근거 창) 칸 다시 톡 = 보던 줄 수 · 굴린 자리 그대로
    W3 「대위」 둘째 100 줄까지 굴리는 중 검색 칸 진짜 톡 → 「상계」 — 옛 줄 0 · 새 결과 첫 100 줄 = 기대 앞 100 · 통 맨 위(0) · 새 결과 끝까지 = 기대
    W4 ⚡ 채점 창 실데이터(기록 ddc6ea7 · ⚡ 약점 10/10 회독 17 문항 다시 그림 = 클라우드 Q2 와 같은 길) — 지난 결과 빨강 3(2) · 5 · 158 · 83 · 초록 13 ·
       계속 틀림 3(2) · 극복함 5 · 158 · 83 · 148 어느 쪽도 아님 · 빨강 칩 진짜 톡 = 그 문항 팝업 · 회독 비교 창 같은 값 · 하네스가 기록에서 따로 센 값 = 지시서 값
    W5 연결한 근거 펼침(문항 팝업 근거 줄 🔗 칩 진짜 톡) — 줄 둘 · 엔진 = WebKit + Chromium(coarse · has_touch · 같은 W5 코드 · --w5-eng):
       ① 꼴 · 누름 — 단추 줄 오른끝 · 글 ↔ 단추 네모 겹침 0 · 누를 것마다 가운데 맨 위 = 제 것 · ✎ 진짜 톡 = 고치기 칸 열림(글 = 저장된 글) · 「취소」 진짜 톡 = 닫힘 ·
          폰 = 단추 네모 위 13px 진짜 톡 = 열림 · 글 폭 / 줄 폭 ≥ 0.90 · iPad = 글 폭 · 13px 위 INFO(한 줄 꼴이면 13px 위는 윗줄 자리) ·
          gate = 상자 그림 = 56836b8(겉모양 무변 · 허용 = 앤티앨리어싱 차 ≤ 4 · 화소 ≤ 64 · PNG_TOL)
       ② ✎ 누를 자리 — 줄마다 elementsFromPoint 맨 위로 찔러 잰 폭 ≥ 36 · 높이 폰 ≥ 36 · iPad ≥ min(36, 그 줄 높이) − 2(줄 사이만큼) ·
          ✎ 끼리 침범 0(그 줄 안 · 가운데 ±18 겨냥 자리를 다른 ✎ 가 맨 위로 덮은 데 0) · ✎ 가운데 ±3px(위 · 아래) 진짜 톡 = 그 줄 고치기 칸 ·
          헛잣대 = 폰 7299ec3(띠 없음 = 18) · iPad 56836b8(띠 겹침 = +3px 톡 아랫줄 칸)
    W6 「× 연결 끊기」 되묻기(ox_del · WebKit + Chromium · --w6-eng · 진짜 confirm 창 = OL.INIT 의 「늘 참」 을 걷고 page.on('dialog') 로 받음) —
       × 진짜 톡 = 되묻기 한 번(confirm · 글에 「연결을 끊」 · 그 문항 ID) · 「취소」 = 연결 그대로(refOf · 상자 · stampAll 도장 무변) ·
       「확인」 = 끊김(refOf · 상자 없음 · 도장/묘비 · syncRecords 뒤 원격 기록.json 에서 빠짐) · iPad 한 줄 꼴 본문 ✎ 위 빗누름(맨 위 = ×) = 되묻기만 · 안 끊김 ·
       쓰임 창(useWin → useUnlink) 끊기 = 되묻기 없이 끊김(무변) · 헛잣대 = d48e4a8(되묻기 없이 바로 끊김)
    W0 페이지 오류 0(pageerror · error · unhandledrejection — 칸마다 띄운 쪽 모두)
    (INFO) WK 환경 — 웹킷 판 · is_mobile · (pointer:coarse) · (hover:none) · maxTouchPoints · Tailwind 실림 · 휠 굴림 됨
  모드(QC): gate = 바탕도 띄워 헛잣대 · regress = 새 판만 · smoke = 새 판 폰 W1(모바일) · W5 만
  결과 = 화면 PASS/FAIL/INFO 줄 · --res(같은 줄 · 기본 = 임시 폴더 h_oxwk · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다
import json, os, re, subprocess, sys, tempfile, time, traceback   # noqa: E402
_sys_r.path.append(_os_r.path.dirname(_os_r.path.abspath(__file__)))
import _ox_live as OL   # noqa: E402 — 앱 글 · 서버 · 가짜 원격 · INIT · __H(클라우드 관문 셋과 같은 띄우기)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEWF = ARG('--new', _roots.genie('minbeop', 'index.html'))
BASE = ARG('--base', '7299ec3')
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
DEVS_ALL = {'폰': dict(name='폰', W=390, H=844), 'iPad': dict(name='iPad', W=820, H=1180)}
DSEL = [x.strip() for x in (ARG('--dev', '') or '').split(',') if x.strip()] or (['폰'] if QC.SMOKE else ['폰', 'iPad'])
DEVS = [DEVS_ALL[d] for d in DSEL if d in DEVS_ALL]
TMPD = os.path.join(tempfile.gettempdir(), 'h_oxwk')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ox_batch_webkit_result.txt'))
OL.conf(spd=ARG('--spd', _roots.spd()), tw=ARG('--tw'), shots=ARG('--shots'))
DREV = ARG('--data-rev', '3065ca0')       # 클라우드 관문(76a3a03 커밋 글 「데이터 = studyplandata 3065ca0(현행)」)과 같은 판 · '' = 작업트리 파일
REC_REV = ARG('--rec-rev', 'ddc6ea7')     # _task_ox_queue_compare §B-2 실데이터 기록
GATE = QC.GATE                            # gate = 바탕을 띄워 헛잣대 · regress · smoke = 새 판만(바탕 풀기 · 띄우기 0)
if GATE:
    QC.sub('git:show-app')
BASE2 = ARG('--base2', '56836b8')        # W5 만 — ox_fix 앞 판(합친 후보) = iPad ✎ 띠 겹침 판
W5ENG = [x.strip() for x in (ARG('--w5-eng', '') or '').split(',') if x.strip()] or (['webkit'] if QC.SMOKE else ['webkit', 'chromium'])
SRC = {'NEW': OL.app_src(NEWF)}
if GATE:
    SRC['BASE'] = OL.app_src(BASE)
VERS = tuple(SRC)
if GATE:
    QC.sub('git:show-app')
    SRC['B2'] = OL.app_src(BASE2)
VERS5 = VERS + (('B2',) if GATE else ())
BASE3 = ARG('--base3', 'd48e4a8')        # W6 만 — ox_del 앞 판(main · ox_fix 들어간 판) = 「× 연결 끊기」 되묻지 않고 바로 끊음
W6ENG = [x.strip() for x in (ARG('--w6-eng', '') or '').split(',') if x.strip()] or ['webkit', 'chromium']
if GATE:
    QC.sub('git:show-app')
    SRC['B3'] = OL.app_src(BASE3)
VERS6 = ('NEW', 'B3') if GATE else ('NEW',)
TERM, TERM2 = '대위', '상계'
LW_CANDS = ['대리', '취소', '소멸시효', '채권자', '계약', '무효', '등기', '점유']   # 클라우드 S2 와 같은 후보 · 100 넘는 첫 말(이어 붙음까지)
GG_CANDS = ['취소', '등기', '변제', '보증', '손해', '효력', '무효', '채권자']       # 클라우드 S3 와 같은 후보 · 100 넘고 300 안쪽 첫 말
QS = '⚡빠른실행'
QN = '🔥 약점 (틀림+헷갈림)'
QK = QS + '||' + QN + '||all||all'
# 지시서 §B-2 실데이터 기대값(채팅 10/10 00:3x 잼 · 클라우드 Q2 와 같음) — 17 문항 중
EXP2 = {'n': 17, 'red': ['Q5517', 'Q5681', 'Q0705', 'Q0684'], 'red_lab': ['3(2)', '5', '158', '83'], 'green': 13,
        'always': ['Q5517'], 'fixed': ['Q5681', 'Q0705', 'Q0684'], 'neither': 'Q0695'}
RES, LINES, STEP, BOOTS = [], [], {}, []
ENV = {'mobile': None}
ERRS = {v: [] for v in VERS5 + (('B3',) if GATE else ())}
T0 = time.time()


def want(c):
    return (not ONLY or c in ONLY) and (not QC.SMOKE or c in ('W1', 'W5'))   # smoke = 폰 W1 · W5


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def R(g, name, new, base=None, d='', yard=True, b2=None, ycol='BASE', b3=None):
    """ycol = 헛잣대 열(BASE = 7299ec3 · B2 = 56836b8 · B3 = d48e4a8) — 헛잣대 셈은 그 열의 판정으로"""
    yv = b2 if ycol == 'B2' else (b3 if ycol == 'B3' else base)
    RES.append(dict(g=g, name=name, new=new, base=base, b2=b2, b3=b3, ycol=ycol, ybase=yv, yard=yard, d=d))
    tag = 'INFO' if new is None else ('PASS' if new else 'FAIL')
    yb = '' if base is None else (' · 바탕 ' + ((('PASS(바탕도 같음)' if ycol == 'BASE' else 'PASS') if yard else 'PASS(바탕 = 기준)') if base else 'FAIL'))
    for bv, lab, col in ((b2, BASE2, 'B2'), (b3, BASE3, 'B3')):
        if bv is not None:
            yb += ' · %s %s' % (lab, ('PASS' + ('(헛잣대 · 같음)' if ycol == col and yard else '')) if bv else ('FAIL' + ('(헛잣대)' if ycol == col else '')))
    ln = '%s | %s · %s%s | %s' % (tag, g, name, yb, _s(d)[:1800])
    LINES.append(ln)
    print(ln, flush=True)


# ---------- 데이터 · 網 ----------
class DRemote(OL.Remote):
    """가짜 원격 — 데이터 판(DREV)의 git blob(읽기만 · 한 번 꺼내 캐시) · over = 갈아 끼운 파일 · PUT = 메모리(OL.Remote 그대로)"""
    CACHE = {}

    def get(self, path):
        with self.lock:
            if path in self.files:
                return self.files[path]
        if not DREV:
            return OL.Remote.get(self, path)
        if path not in DRemote.CACHE:
            QC.sub('git:show-data')
            r = subprocess.run(['git', '-C', OL.CONF['spd'], 'show', '%s:%s' % (DREV, path)], capture_output=True)
            DRemote.CACHE[path] = r.stdout if r.returncode == 0 else None
        return DRemote.CACHE[path]


def route_wk(remote):
    h = OL.route(remote)

    def f(rt):
        if rt.request.url.startswith('https://cdn.tailwindcss.com'):
            return rt.continue_()   # 본 PC = Tailwind cdn 그대로 — OL.route 도 10/10 ca8837e6 부터 통과(그 앞 c2c49616 은 끊었음 · 이 겹은 어느 판 헬퍼든 같게) · --tw 면 OL.inject 가 <style> 로 갈아 요청 자체가 없음
        return h(rt)
    return f


# ---------- 웹킷 쪽 도구 ----------
WKH = r"""
window.__W={
 own(e,x,y){const a=document.elementsFromPoint(x,y)[0];return !!a&&(a===e||e.contains(a))},
 sig(a){return a?(a.id?'#'+a.id:a.tagName.toLowerCase()+'.'+String(a.className&&a.className.baseVal!==undefined?a.className.baseVal:(a.className||'')).slice(0,28)):null},
 /* 누를 점 — 보이는 네모(화면과 겹친 몫) 안에서 그 점과 ±2px 여덟 이웃의 맨 위가 다 그 요소(또는 안)인 점 · 가운데 먼저 · 그다음 격자 */
 safe(e){if(!e)return null;try{e.scrollIntoView({block:'center',inline:'nearest'})}catch(_){}
   const r=e.getBoundingClientRect(),L=Math.max(r.left,0),T=Math.max(r.top,0),Rr=Math.min(r.right,innerWidth),B=Math.min(r.bottom,innerHeight);
   const o={w:+r.width.toFixed(1),h:+r.height.toFixed(1),x0:Math.round(r.left),y0:Math.round(r.top)};
   if(Rr-L<1||B-T<1)return Object.assign(o,{on:false,why:'화면 밖'});
   const ok=(x,y)=>{for(const dx of [-2,0,2])for(const dy of [-2,0,2])if(!__W.own(e,x+dx,y+dy))return false;return true};
   const cand=[[(L+Rr)/2,(T+B)/2]];for(const fy of [0.5,0.3,0.7])for(const fx of [0.5,0.3,0.7,0.15,0.85])cand.push([L+(Rr-L)*fx,T+(B-T)*fy]);
   for(const [x,y] of cand)if(ok(x,y))return Object.assign(o,{on:true,cx:x,cy:y,margin:2});
   for(const [x,y] of cand)if(__W.own(e,x,y))return Object.assign(o,{on:true,cx:x,cy:y,margin:0});
   return Object.assign(o,{on:false,why:'가림 '+__W.sig(document.elementsFromPoint((L+Rr)/2,(T+B)/2)[0])})},
 /* 누를 자리 — 가운데에서 위 · 아래 · 왼 · 오른으로 elementsFromPoint 맨 위가 그 요소(또는 안)인 데까지(::before 로 넓힌 자리도 셈) */
 hitExt(e){if(!e)return null;const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;
   if(!__W.own(e,cx,cy))return {h:0,w:0,on:false,top:__W.sig(document.elementsFromPoint(cx,cy)[0])};let u=0,d=0,l=0,rt=0;
   while(u<60&&__W.own(e,cx,cy-u-1))u++;while(d<60&&__W.own(e,cx,cy+d+1))d++;while(l<160&&__W.own(e,cx-l-1,cy))l++;while(rt<160&&__W.own(e,cx+rt+1,cy))rt++;
   /* 막은 것 — 36px 띠(가운데 ±18) 안에서 끊겼으면 그 자리 맨 위가 무엇인가(다른 ✎ = 이웃 줄 누를 자리가 덮음) */
   const by=a=>{if(!a)return 'null';const x=a.closest&&a.closest('button[onclick^="ggRefEdit("]');return x&&x!==e?'다른 ✎':__W.sig(a)};   /* ✎ = onclick 으로 가름(7299ec3 엔 .ggrefed 없음) */
   return {h:u+d+1,w:l+rt+1,up:u,down:d,on:true,cutUp:u<17?by(document.elementsFromPoint(cx,cy-u-1)[0]):null,cutDown:d<17?by(document.elementsFromPoint(cx,cy+d+1)[0]):null}},
 env(){const sr=document.getElementById('search-results'),cs=sr?getComputedStyle(sr):null;
   return {coarse:matchMedia('(pointer:coarse)').matches,anyCoarse:matchMedia('(any-pointer:coarse)').matches,hoverNone:matchMedia('(hover:none)').matches,
     maxTouchPoints:navigator.maxTouchPoints,ontouchstart:'ontouchstart' in window,dpr:devicePixelRatio,iw:innerWidth,ih:innerHeight,
     tailwind:typeof tailwind!=='undefined',searchBoxCss:cs?{maxH:cs.maxHeight,ovY:cs.overflowY}:null,
     ua:String(navigator.userAgent).replace(/^.*?(AppleWebKit\/[\d.]+).*?(Version\/[\d.]+)?.*$/,'$1 $2').trim()}}
};
"""
VISC = r"""(s)=>{const b=document.querySelector(s);if(!b)return null;const r=b.getBoundingClientRect();
 const L=Math.max(r.left,0),T=Math.max(r.top,0),R=Math.min(r.right,innerWidth),B=Math.min(r.bottom,innerHeight);
 return {x:(L+R)/2,y:(T+B)/2,vis:R-L>4&&B-T>4,top:b.scrollTop,max:b.scrollHeight-b.clientHeight}}"""
SCROLL_ST = r"""([s,r])=>{const b=document.querySelector(s);if(!b)return null;return {rows:document.querySelectorAll(r).length,top:Math.round(b.scrollTop),
 max:Math.round(b.scrollHeight-b.clientHeight),more:!!b.querySelector(':scope > [data-res-more]')}}"""
GEO_JS = r"""(rs)=>{const L=[...document.querySelectorAll(rs)].map(e=>e.getBoundingClientRect());let ov=0,zero=0;
 for(let i=0;i<L.length;i++){if(L[i].height<1)zero++;if(i&&L[i-1].bottom-L[i].top>0.5)ov++}return {ov,zero,n:L.length}}"""
ERR_JS = "(()=>(window.__err||[]).slice(0,8))()"


class WL:
    """웹킷 기기 하나 = 문맥 하나 — OL 서버 · 가짜 원격 · INIT · __H 그대로 · 톡 = touchscreen.tap(진짜 터치) · 굴림 = 휠(되면) 아니면 scrollTop"""

    def __init__(self, br, tag, dev, label, remote=None, wait_sync=True, mobile=True, pre_init=''):
        QC.launch('new' if tag == 'NEW' else 'base')   # BASE(7299ec3) · B2(56836b8) · B3(d48e4a8) = 바탕 띄움
        self.tag, self.dev, self.label = tag, dev, label
        kw = dict(viewport={'width': dev['W'], 'height': dev['H']}, device_scale_factor=2, has_touch=True)
        if mobile and ENV['mobile'] is not False:
            kw['is_mobile'] = True
        try:
            self.ctx = br.new_context(**kw)
            if mobile and ENV['mobile'] is None:
                ENV['mobile'] = bool(kw.get('is_mobile'))
        except Exception as e:
            ENV['mobile'], ENV['mobile_err'] = False, str(e)[:200]
            kw.pop('is_mobile', None)
            self.ctx = br.new_context(**kw)
        self.mobile = bool(kw.get('is_mobile'))
        self.remote = remote or DRemote()
        self.ctx.route(re.compile(r'^https?://'), route_wk(self.remote))   # http(s) 만 — blob: · data: 는 route 밖
        if pre_init:   # OL.INIT 앞 — 예: 진짜 confirm 을 잡아 둠(OL.INIT 이 confirm = 늘 참 으로 갈아 끼우기 전)
            self.ctx.add_init_script(pre_init)
        self.ctx.add_init_script(OL.INIT)
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append(str(e)[:240]))
        self.wkey = 'wheel@' + ('mobile' if self.mobile else 'desktop')
        self.wheel = ENV.get(self.wkey)   # None = 아직 모름 · True = 휠 굴림 됨 · False = 안 됨(모바일 웹킷 = playwright 가 휠을 안 받음)
        t = time.time()
        try:
            port = OL.serve(tag, SRC[tag])
            self.pg.goto('http://127.0.0.1:%d/minbeop/index.html' % port, wait_until='commit', timeout=120000)   # onload 를 안 기다림 — 시동 표지로
            if not QC.until(self.pg, "() => typeof quizData !== 'undefined' && quizData.length > 1000 && typeof runSearch === 'function'", 120000, 'WK 부팅 — quizData · runSearch'):
                raise RuntimeError('부팅 표지(quizData · runSearch) 120 초 안 옴 · 오류 %s' % self.errs[:2])
            self.synced = True
            if wait_sync:
                self.synced = QC.until(self.pg, "() => typeof recBusy !== 'undefined' && !recBusy && ((JSON.parse(localStorage.getItem('ox_sync_meta')||'{}').lastSync)||0) > 0",
                                       120000, 'WK 부팅 — 첫 기록 맞추기 끝(recBusy 거짓 · lastSync)')
            QC.sleep(500, 'WK 부팅 뒤 첫 그림 가라앉힘(OL.Live 와 같은 0.5 초)', self.pg)
            self.pg.evaluate(OL.H)
            self.pg.evaluate(WKH)
        except Exception:
            try:
                self.ctx.close()
            except Exception:
                pass
            raise
        self.boot = round(time.time() - t, 1)
        BOOTS.append(self.boot)
        if 'env' not in ENV:
            ENV['env'] = dict(self.ev("(()=>__W.env())()"), dev=dev['name'], boot_s=self.boot, synced=self.synced)

    def ev(self, js, arg=None):
        return self.pg.evaluate(js, arg)

    def wait(self, ms, why):
        QC.sleep(ms, why, self.pg)

    def tap(self, at):
        if not at or not at.get('on'):
            return False
        self.pg.touchscreen.tap(at['cx'], at['cy'])
        return True

    def tap_xy(self, x, y):
        self.pg.touchscreen.tap(x, y)

    def scroll_box(self, sel, dy=3000):
        """굴림 통 하나를 아래로 — 휠(통 보이는 가운데 · 되면) · 아니면 scrollTop = 끝 + scroll 사건 · 돌려줌 = 쓴 길"""
        r = self.ev(VISC, sel)
        if not r:
            return 'none'
        if not r['vis']:
            self.ev("(s)=>document.querySelector(s).scrollIntoView({block:'nearest'})", sel)
            r = self.ev(VISC, sel)
        if r['top'] >= r['max'] - 1:
            return 'at-end'   # 이미 끝 — 관찰자가 붙이기를 기다림(따로 안 굴림)
        if self.wheel is not False and r['vis']:
            try:
                self.pg.mouse.move(r['x'], r['y'])
                self.pg.mouse.wheel(0, dy)
            except Exception as e:   # 모바일 웹킷 — 「Mouse wheel is not supported in mobile WebKit」(playwright 한계)
                self.wheel = ENV[self.wkey] = False
                ENV[self.wkey + ' 까닭'] = str(e).split('\n')[0][:120]
            if self.wheel is not False:
                self.pg.wait_for_timeout(150)
                t1 = self.ev("(s)=>document.querySelector(s).scrollTop", sel)
                if t1 <= r['top'] + 0.5 and self.wheel is None:   # 첫 휠 — 굴림이 늦게 붙는지 한 번 더 봄(휠이 안 먹는다고 판정하기 전에)
                    self.pg.wait_for_timeout(350)
                    t1 = self.ev("(s)=>document.querySelector(s).scrollTop", sel)
                if t1 > r['top'] + 0.5:
                    self.wheel = ENV[self.wkey] = True
                    return 'wheel'
                if self.wheel is None:
                    self.wheel = ENV[self.wkey] = False
        self.ev("(s)=>{const b=document.querySelector(s);b.scrollTop=b.scrollHeight;b.dispatchEvent(new Event('scroll'))}", sel)
        return 'scrollTop'

    def errors(self):
        try:
            return (self.errs or []) + (self.ev(ERR_JS) or [])
        except Exception as e:
            return self.errs + ['ev: ' + str(e)[:120]]

    def shot(self, name):
        if not OL.CONF['shots']:
            return None
        try:
            os.makedirs(OL.CONF['shots'], exist_ok=True)
            f = os.path.join(OL.CONF['shots'], 'wk_%s.png' % name)
            self.pg.screenshot(path=f)
            return f
        except Exception:
            return None

    def close(self):
        e = self.errors()
        if e:
            ERRS[self.tag].append({'칸': self.label, '기기': self.dev['name'], '오류': e[:4]})
        try:
            self.ctx.close()
        except Exception:
            pass
        return e


def scroll_all(p, sel, rowsel, want_n, cap=120):
    """그 통을 끝까지 — 줄 수 = want_n 이고 꼬리(data-res-more) 없으면 멈춤 · 줄 수도 굴린 자리도 세 번 그대로면 멈춤 · 돌려줌 = (줄, 돈 수, 쓴 길 셈)"""
    how, last, same, k = {}, None, 0, 0
    for k in range(cap):
        st = p.ev(SCROLL_ST, [sel, rowsel])
        if not st:
            break
        if st['rows'] >= want_n and not st['more']:
            break
        key = (st['rows'], st['top'])
        same = same + 1 if key == last else 0
        if same >= 3:
            break
        last = key
        m = p.scroll_box(sel)
        how[m] = how.get(m, 0) + 1
        p.wait(250, 'W 굴림 — 관찰자(IntersectionObserver)가 다음 100 줄 붙임')
    st = p.ev(SCROLL_ST, [sel, rowsel]) or {}
    return st.get('rows', 0), k + 1, how


# ---------- 기대 수 — 앱 거르기 식과 같은 식(쪽 안에서 따로 셈 · 클라우드 관문 셋과 같은 글) ----------
EXP_Q = r"""(term)=>{const low=term.toLowerCase(),lowNS=low.replace(/\s+/g,'');return quizData.filter(q=>{
  if(!q.pending&&String(q.q).toLowerCase().includes(low))return true;if(!q.pending&&String(q.exp||'').toLowerCase().includes(low))return true;
  if(lowNS&&String(q.id||'').toLowerCase().includes(lowNS))return true;if(lowNS&&String(q.source||'').toLowerCase().replace(/\s+/g,'').includes(lowNS))return true;return false}).map(q=>q.id)}"""
EXP_LW = r"""([owner,term])=>{const low=String(term).trim().toLowerCase();return quizData.filter(q=>{if(String(q.id)===String(owner))return false;
  const no=`${q.displayNo??q.probNum}${q.subNum||''}`;return [q.id,no,q.q,q.source,q.subject,q.subChapter].map(v=>String(v||'').toLowerCase()).some(h=>h.includes(low))}).map(q=>q.id)}"""
EXP_GG = r"""([owner,term])=>{const low=String(term).trim().toLowerCase(),gst=ggStore();return quizData.filter(q=>{if(String(q.id)===String(owner).replace(/^cmp_/,''))return false;
  const L=Array.isArray(gst[q.id])?gst[q.id]:[];const extra=ggTextOfList(L);if(!String(extra).trim())return false;
  const no=`${q.displayNo??q.probNum}${q.subNum||''}`;return [q.id,no,q.q,q.source,q.subject,q.subChapter,extra].map(v=>String(v||'').toLowerCase()).some(h=>h.includes(low))}).map(q=>q.id)}"""
IDS_SEARCH = r"""()=>[...document.querySelectorAll('#search-results > button')].map(e=>{const m=/openQPopup\('([^']+)'/.exec(e.getAttribute('onclick')||'');return m?m[1]:null})"""
FIRST_SEARCH = r"""()=>{const b=document.getElementById('search-results'),cs=getComputedStyle(b);return {cnt:document.getElementById('search-count').textContent,
 rows:document.querySelectorAll('#search-results > button').length,note:/상위 \d+건만/.test(b.textContent),val:document.getElementById('search-input').value,
 top:Math.round(b.scrollTop),css:{maxH:cs.maxHeight,ovY:cs.overflowY}}}"""


def pick_term(p, js, owner, cands, lo, hi):
    for t in cands:
        n = len(p.ev(js, [owner, t]))
        if lo <= n <= hi:
            return t, n
    return None, 0


def type_into(p, sel, text, select_all=False):
    """칸을 진짜 톡 → 포커스(안 오면 focus() 로 · 적음) → (select_all 이면 글 다 고름) → 타자(웹킷 = 한글은 insertText · input 사건)"""
    at = p.ev("(s)=>__W.safe(document.querySelector(s))", sel)
    tapped = p.tap(at)
    p.wait(200, 'W 칸 톡 뒤 포커스')
    foc = p.ev("(s)=>document.activeElement===document.querySelector(s)", sel)
    if not foc:
        p.ev("(s)=>document.querySelector(s).focus()", sel)
    if select_all:
        p.ev("(s)=>document.querySelector(s).select()", sel)
    p.pg.keyboard.type(text, delay=30)
    return {'톡 자리': bool(at and at.get('on')), '톡': tapped, '톡 → 포커스': foc, '값 = 친 말': p.ev("([s,t])=>document.querySelector(s).value===t", [sel, text]),
            '가림': None if (at and at.get('on')) else (at or {}).get('why')}


# ---------- W1 · W3 — 첫 화면 검색 ----------
def w1(br, v, dev, mobile=True):
    p = WL(br, v, dev, 'W1' if mobile else 'W1 휠', mobile=mobile)
    try:
        exp = p.ev(EXP_Q, TERM)
        p.ev("()=>{setSearchMode('q');const i=document.getElementById('search-input');i.value='';runSearch();}")
        tin = type_into(p, '#search-input', TERM)
        QC.until(p.pg, "()=>document.querySelectorAll('#search-results > button').length>0", 8000, 'W1 첫 줄')
        p.wait(500, 'W1 첫 100 줄 뒤 관찰자 첫 셈(끝 줄 앞 200px 안 닿음)')
        first = p.ev(FIRST_SEARCH)
        n, rounds, how = scroll_all(p, '#search-results', '#search-results > button', len(exp))
        got = p.ev(IDS_SEARCH)
        geo = p.ev(GEO_JS, '#search-results > button')
        last = p.ev("()=>{const L=document.querySelectorAll('#search-results > button');return L.length?__W.safe(L[L.length-1]):null}")
        opened = None
        if last and last.get('on') and got:
            p.tap(last)
            opened = QC.until(p.pg, "(id)=>!!document.getElementById('oxwin-q-'+id)", 5000, 'W1 끝 줄 톡 → 그 문항 팝업', arg=got[-1])
        p.shot('w1_%s_%s' % (v, dev['name']))
        errs = p.errors()
    finally:
        p.close()
    wheel_ok = mobile or (how.get('wheel', 0) > 0 and not how.get('scrollTop'))   # 휠 갈래는 휠로만 굴렸어야 뜻이 있다
    d = {'기대': len(exp), '셈': first['cnt'], '처음 줄': first['rows'], '상위 N건만 글': first['note'], '굴린 뒤 줄': n, '굴림(번 · 길)': [rounds, how],
         '모바일 문맥': p.mobile, '차례 = 기대': got == exp, '겹침(같은 ID · 줄 네모 · 높이 0)': [len(got) - len(set(got)), geo['ov'], geo['zero']], '끝 줄 톡 → 팝업': opened,
         '끝 줄 톡 자리': {k: (last or {}).get(k) for k in ('on', 'margin', 'w', 'h')}, '검색 칸': tin, '결과 통 CSS': first['css'], '오류': errs[:3]}
    ok = (len(exp) > 100 and first['cnt'] == '%d건' % len(exp) and first['rows'] == 100 and not first['note'] and n == len(exp) and got == exp
          and len(got) == len(set(got)) and geo['ov'] == 0 and geo['zero'] == 0 and opened is True and tin['톡 자리'] and tin['값 = 친 말'] and wheel_ok and not errs)
    return ok, d


def w3(br, v, dev):
    p = WL(br, v, dev, 'W3')
    try:
        exp2 = p.ev(EXP_Q, TERM2)
        p.ev("(t)=>{setSearchMode('q');const i=document.getElementById('search-input');i.value=t;runSearch();}", TERM)
        p.wait(400, 'W3 「대위」 첫 100 줄')
        how = {}
        for _ in range(12):   # 둘째 100 줄이 붙을 때까지 굴림(굴리는 중 · 바탕은 100 에서 멈춤)
            m = p.scroll_box('#search-results')
            how[m] = how.get(m, 0) + 1
            p.wait(300, 'W3 굴림 — 둘째 100 줄 붙음 기다림')
            if p.ev("document.querySelectorAll('#search-results > button').length") > 100:
                break
        mid = p.ev("document.querySelectorAll('#search-results > button').length")
        mid_top = p.ev("Math.round(document.getElementById('search-results').scrollTop)")
        tin = type_into(p, '#search-input', TERM2, select_all=True)
        p.wait(800, 'W3 새 검색어 그림')
        st_new = p.ev("Math.round(document.getElementById('search-results').scrollTop)")
        cnt = p.ev("document.getElementById('search-count').textContent")
        got = p.ev(IDS_SEARCH)
        old = [x for x in got if x not in set(exp2)]
        n2, rounds, how2 = scroll_all(p, '#search-results', '#search-results > button', len(exp2))
        got2 = p.ev(IDS_SEARCH)
        errs = p.errors()
    finally:
        p.close()
    d = {'옛 검색어 굴린 줄 · 자리': [mid, mid_top], '굴림 길(옛)': how, '새 검색어': TERM2, '새 기대': len(exp2), '셈': cnt, '새 줄': len(got), '옛 줄 남음': len(old),
         '첫 100 = 기대 앞 100': got == exp2[:100], '새 검색어 굴림 자리(맨 위 = 0)': st_new, '새 결과 끝까지 = 기대': got2 == exp2, '끝까지 줄': n2,
         '굴림(번 · 길)': [rounds, how2], '검색 칸': tin, '오류': errs[:3]}
    ok = (len(exp2) > 100 and mid > 100 and cnt == '%d건' % len(exp2) and not old and got == exp2[:100] and st_new == 0 and got2 == exp2
          and tin['톡 자리'] and tin['값 = 친 말'] and not errs)
    return ok, d


# ---------- W2 — 연결 창 · 근거 창 ----------
def w2_link(br, v, dev):
    p = WL(br, v, dev, 'W2 연결')
    try:
        owner = p.ev("quizData[0].id")
        term, _n = pick_term(p, EXP_LW, owner, LW_CANDS, 101, 900)
        exp = p.ev(EXP_LW, [owner, term]) if term else []
        p.ev("(o)=>{lwOpen(o)}", owner)
        QC.until(p.pg, "()=>!!document.querySelector('#oxwin-lk .cfq')", 5000, 'W2 연결 창')
        p.wait(300, 'W2 연결 창 자리 맞춤(lwFit)')
        tin = type_into(p, '#oxwin-lk .cfq', term or '')
        QC.until(p.pg, "()=>document.querySelectorAll('#oxwin-lk .cfrs > .cfr').length>0", 8000, 'W2 연결 창 첫 줄(120ms 모음 뒤)')
        p.wait(500, 'W2 첫 100 줄 뒤 관찰자 첫 셈')
        first = p.ev("()=>({cnt:(document.querySelector('#oxwin-lk .cfcnt')||{}).textContent||null,rows:document.querySelectorAll('#oxwin-lk .cfrs > .cfr').length})")
        n, rounds, how = scroll_all(p, '#oxwin-lk .cfrs', '#oxwin-lk .cfrs > .cfr', len(exp))
        got = p.ev("()=>[...document.querySelectorAll('#oxwin-lk .cfrs > .cfr')].map(e=>{const x=e.querySelector('.cfid');return x?x.textContent.replace(/^ID /,''):null})")
        geo = p.ev(GEO_JS, '#oxwin-lk .cfrs > .cfr')
        errs = p.errors()
    finally:
        p.close()
    d = {'검색어': term, '기대': len(exp), '셈': first['cnt'], '처음 줄': first['rows'], '굴린 뒤 줄': n, '굴림(번 · 길)': [rounds, how], '차례 = 기대': got == exp,
         '겹침(같은 ID · 줄 네모)': [len(got) - len(set(got)), geo['ov']], '찾기 칸': tin, '오류': errs[:3]}
    ok = (len(exp) > 100 and first['cnt'] == '%d건' % len(exp) and first['rows'] == 100 and n == len(exp) and got == exp and len(got) == len(set(got))
          and geo['ov'] == 0 and tin['톡 자리'] and tin['값 = 친 말'] and not errs)
    return ok, d


def w2_geunge(br, v, dev):
    p = WL(br, v, dev, 'W2 근거')
    try:
        owner = p.ev("(()=>{const g=ggStore();const q=quizData.find(q=>Array.isArray(g[q.id])&&g[q.id].length);return q?q.id:quizData[0].id})()")
        term, _n = pick_term(p, EXP_GG, owner, GG_CANDS, 101, 300)
        exp = p.ev(EXP_GG, [owner, term]) if term else []
        p.ev("(o)=>{openQPopup(o)}", owner)
        QC.until(p.pg, "(o)=>!!document.getElementById('oxwin-q-'+o)", 5000, 'W2 근거 — 문항 팝업', arg=owner)
        p.wait(500, 'W2 근거 — 팝업 그림 가라앉힘')
        btn = "#oxwin-q-%s button[onclick^=\"ggSearchToggle(\"]" % owner
        at = p.ev("(s)=>__W.safe(document.querySelector(s))", btn)
        lens_tap = p.tap(at)   # 🔍 진짜 톡 → 찾기 칸 펴짐 · 포커스 · linkSearch
        sel_in = '#qp-link-search-geunge-' + owner
        lens_open = QC.until(p.pg, "(s)=>{const i=document.querySelector(s);return !!i&&__H.vis(i)}", 3000, 'W2 근거 — 🔍 톡 → 찾기 칸', arg=sel_in)
        if not lens_open:
            p.ev("(o)=>{ggSearchToggle(o,'qp-')}", owner)
            p.wait(300, 'W2 근거 — 🔍 함수로 폄(톡이 안 먹음 · 적음)')
        tin = type_into(p, sel_in, term or '')
        box = '#qp-link-results-geunge-' + owner
        QC.until(p.pg, "(b)=>document.querySelectorAll(b+' > button').length>0", 8000, 'W2 근거 첫 줄(120ms 모음 뒤)', arg=box)
        p.wait(600, 'W2 근거 첫 100 줄 뒤 관찰자 첫 셈')
        first = p.ev("(b)=>{const e=document.querySelector(b),cs=getComputedStyle(e);return {cnt:(e.querySelector('[data-res-cnt]')||{}).textContent||null,rows:document.querySelectorAll(b+' > button').length,css:{maxH:cs.maxHeight,ovY:cs.overflowY}}}", box)
        n, rounds, how = scroll_all(p, box, box + ' > button', len(exp))
        got = p.ev(r"(b)=>[...document.querySelectorAll(b+' > button')].map(e=>{const m=/,'([^']+)'(?:,'qp-')?\)/.exec(e.getAttribute('onclick')||'');return m?m[1]:null})", box)
        geo = p.ev(GEO_JS, box + ' > button')
        # 같은 검색어 다시 그림 — 칸을 다시 진짜 톡(onfocus linkSearch) = 보던 줄 수 · 굴린 자리 그대로
        st0 = p.ev("(b)=>Math.round(document.querySelector(b).scrollTop)", box)
        p.ev("(s)=>document.querySelector(s).blur()", sel_in)
        p.wait(150, 'W2 근거 칸 블러')
        at2 = p.ev("(s)=>{const e=document.querySelector(s);const r=e.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)e.scrollIntoView({block:'nearest'});return __W.safe(e)}", sel_in)
        again_tap = p.tap(at2)
        p.wait(500, 'W2 근거 칸 다시 톡 → 다시 그림')
        again = p.ev("([b,s])=>({rows:document.querySelectorAll(b+' > button').length,st:Math.round(document.querySelector(b).scrollTop),foc:document.activeElement===document.querySelector(s)})", [box, sel_in])
        errs = p.errors()
    finally:
        p.close()
    d = {'주인 문항': owner, '검색어': term, '기대': len(exp), '🔍 톡': [bool(at and at.get('on')), lens_tap, lens_open], '셈': first['cnt'], '처음 줄': first['rows'],
         '굴린 뒤 줄': n, '굴림(번 · 길)': [rounds, how], '차례 = 기대': got == exp, '겹침(같은 ID · 줄 네모)': [len(got) - len(set(got)), geo['ov']],
         '칸 다시 톡(줄 · 자리 앞 → 뒤 · 포커스)': [again['rows'], st0, again['st'], again_tap, again['foc']], '찾기 칸': tin, '결과 통 CSS': first['css'], '오류': errs[:3]}
    ok = (len(exp) > 100 and first['cnt'] == '%d건' % len(exp) and first['rows'] == 100 and n == len(exp) and got == exp and len(got) == len(set(got)) and geo['ov'] == 0
          and again_tap and again['rows'] == n and abs(again['st'] - st0) <= 2 and lens_open and tin['톡 자리'] and tin['값 = 친 말'] and not errs)
    return ok, d


# ---------- W4 — ⚡ 채점 창 실데이터 ----------
def dnum(s):
    n = re.findall(r'\d+', s or '')
    if len(n) < 3:
        return 0
    if len(n[0]) == 4:
        return int(n[0]) * 10000 + int(n[1]) * 100 + int(n[2])
    if len(n[2]) == 4:
        return int(n[2]) * 10000 + int(n[0]) * 100 + int(n[1])
    return 0


def rec_bytes():
    QC.sub('git:show-rec')
    r = subprocess.run(['git', '-C', OL.CONF['spd'], 'show', REC_REV + ':minbeop/기록.json'], capture_output=True)
    return r.stdout if r.returncode == 0 and r.stdout else None


def w4_expect(rec_b):
    """하네스 따로 셈 — 기록의 모든 열쇠 · 모든 회독(⚡ 약점 마지막 회독 = 이번 뺌)을 날짜 차례(같은 날 = 쌓인 차례)로 훑어 문항마다 마지막 결과 → 지시서 값과 맞댐"""
    rec = json.loads(rec_b.decode('utf-8'))
    ch = (rec.get('data') or {}).get('ox_chap_history') or {}
    ch = json.loads(ch) if isinstance(ch, str) else ch
    L = ch.get(QK) or []
    if not L:
        return False, {'까닭': '⚡ 약점 열쇠 회독 없음'}
    rows = []
    for k, LL in ch.items():
        for i, a in enumerate(LL if isinstance(LL, list) else []):
            if k == QK and i == len(L) - 1:
                continue
            for qid, val in ((a or {}).get('marks') or {}).items():
                if val is True or val is False:
                    rows.append((dnum(a.get('date')), qid, val))
    rows.sort(key=lambda r: r[0])   # 안정 정렬 — 같은 날은 쌓인 차례
    last = {}
    for _, qid, val in rows:
        last[qid] = val
    mk = L[-1].get('marks') or {}
    red = [i for i in mk if last.get(i) is False]
    green = [i for i in mk if last.get(i) is True]
    al = [i for i in mk if mk[i] is False and last.get(i) is False]
    fx = [i for i in mk if mk[i] is True and last.get(i) is False]
    nb = EXP2['neither']
    ok = (len(mk) == EXP2['n'] and red == EXP2['red'] and len(green) == EXP2['green'] and al == EXP2['always'] and fx == EXP2['fixed']
          and mk.get(nb) is False and last.get(nb) is True)
    return ok, {'문항': len(mk), '빨강': red, '초록 수': len(green), '계속 틀림': al, '극복함': fx, '148(Q0695) 이번 · 지난': [mk.get(nb), last.get(nb)]}


READ_JS = r"""(()=>{const col=e=>/(^|\s)bg-red-100(\s|$)/.test(e.className)?'R':/(^|\s)bg-green-50(\s|$)/.test(e.className)?'G':/(^|\s)bg-gray-50(\s|$)/.test(e.className)?'-':'?';
 const idOf=e=>{const m=/\('([^']+)'\)/.exec(e.getAttribute('onclick')||'');return m?m[1]:null};
 const chips=box=>box?[...box.querySelectorAll('[style*="min-width:1.6rem"]')].map(e=>({id:idOf(e),l:__H.tx(e),c:col(e)})):null;
 const lab=(b,t)=>{const s=[...b.querySelectorAll('span')].find(x=>__H.tx(x)===t);return s?chips(s.nextElementSibling):null};
 const out={};
 const w=document.getElementById('oxwin-grade');
 if(w&&__H.vis(w)){const b=w.querySelector('.oxwin-body');const pl=b.querySelector('[data-prior-last]');
   out.grade={prior:pl?chips(pl):null,always:lab(b,'계속 틀림'),fixed:lab(b,'극복함'),
     heads:[...b.querySelectorAll('div')].filter(d=>/text-\[10px\]/.test(d.className)&&/(회독|지난 결과)/.test(__H.tx(d))&&!d.querySelector('div')).map(d=>__H.tx(d).replace(/\d{4}\. \d+\. \d+\./,'(날짜)'))}}
 const m=document.getElementById('compare-modal');
 if(m&&!m.classList.contains('hide')){const b=document.getElementById('compare-body');
   out.cmp={prior:lab(b,'지난 결과'),always:lab(b,'계속 틀림'),fixed:lab(b,'극복함')}}
 return out})()"""
RERENDER_JS = r"""([qs,qn,qk])=>{document.getElementById('source-filter').value='all';document.getElementById('review-filter').value='all';
 const L=(JSON.parse(localStorage.getItem('ox_chap_history')||'{}')[qk])||[];const h=L[L.length-1];if(!h)return null;
 const items=Object.keys(h.marks||{}).map(id=>quizData.find(q=>String(q.id)===String(id))).filter(Boolean);
 startVirtualQuiz(qn,items);
 const results=items.map(it=>({item:it,picked:null,isCorrect:h.marks[it.id]===true}));
 chapterSaved=qk;
 const sc=results.filter(r=>r.isCorrect).length;lastGradeResults={results,score:sc,total:results.length};showGradeModal(results,sc,results.length);
 return {n:results.length,hist:L.length,ids:items.map(q=>String(q.id))}}"""
SWEEP_JS = r"""(sel)=>{const out=[];const R=document.querySelector(sel);if(!R||!__H.vis(R))return ['(없음) '+sel];
 const rb=R.getBoundingClientRect();if(rb.left<-1||rb.right>innerWidth+1)out.push('화면 밖 '+[Math.round(rb.left),Math.round(rb.right)]);
 if(document.scrollingElement.scrollWidth>innerWidth+1)out.push('page-hscroll');
 [R,...R.querySelectorAll('*')].forEach(e=>{if(!__H.vis(e))return;const cs=getComputedStyle(e),b=e.getBoundingClientRect();
   if((cs.overflowX==='auto'||cs.overflowX==='scroll'||cs.overflowX==='hidden')&&e.scrollWidth>e.clientWidth+1&&e.clientWidth>0)out.push('가로 넘침:'+e.tagName+'.'+String(e.className).slice(0,24));
   if(b.width>0&&(b.right>rb.right+1||b.left<rb.left-1))out.push('밖:'+e.tagName+'.'+String(e.className).slice(0,24))});
 return [...new Set(out)].slice(0,8)}"""


def cmap(L):
    return {c['id']: c['c'] for c in (L or [])}


def ids(L):
    return None if L is None else [c['id'] for c in L]


def w4(br, v, dev, rec_b, exp_py):
    if not rec_b:
        return False, {'까닭': '기록 %s 판을 못 읽음(studyplandata 클론에 그 판이 있어야)' % REC_REV}
    p = WL(br, v, dev, 'W4', remote=DRemote({'minbeop/기록.json': rec_b}))
    tap = None
    try:
        rr = p.ev(RERENDER_JS, [QS, QN, QK])
        QC.until(p.pg, "()=>{const w=document.getElementById('oxwin-grade');return !!w&&__H.vis(w)}", 5000, 'W4 채점 창')
        p.wait(500, 'W4 채점 창 그림 가라앉힘')
        r1 = p.ev(READ_JS)
        sw_g = p.ev(SWEEP_JS, '#oxwin-grade')
        # 빨강 칩(3(2) · Q5517) 진짜 톡 → 그 문항 팝업(「지난 결과」 줄 · 바탕엔 그 줄 없음)
        at = p.ev("(i)=>{const e=document.querySelector(`#oxwin-grade [data-prior-last] [onclick=\"openQPopup('${i}')\"]`);return e?__W.safe(e):null}", EXP2['red'][0])
        if at:
            tapped = p.tap(at)
            op = QC.until(p.pg, "(i)=>!!document.getElementById('oxwin-q-'+i)", 5000, 'W4 빨강 칩 톡 → 문항 팝업', arg=EXP2['red'][0]) if tapped else False
            tap = {'자리': bool(at.get('on')), '여백': at.get('margin'), '칩 네모': [at.get('w'), at.get('h')], '팝업': op}
            p.ev("(i)=>{try{oxWinClose('q-'+i)}catch(e){}const w=document.getElementById('oxwin-q-'+i);if(w)w.remove()}", EXP2['red'][0])
        p.ev("([s,l])=>{const g=document.getElementById('oxwin-grade');if(g)g.style.display='none';openCompareModal(s,l)}", [QS, QN])
        QC.until(p.pg, "()=>{const m=document.getElementById('compare-modal');return !!m&&!m.classList.contains('hide')}", 5000, 'W4 회독 비교 창')
        p.wait(400, 'W4 회독 비교 창 그림 가라앉힘')
        r3 = p.ev(READ_JS)
        sw_c = p.ev(SWEEP_JS, '#compare-modal > div')
        p.shot('w4_%s_%s' % (v, dev['name']))
        errs = p.errors()
    finally:
        p.close()
    g, c = r1.get('grade') or {}, r3.get('cmp') or {}
    gi = cmap(g.get('prior'))
    ids17 = (rr or {}).get('ids') or []
    exp_c = {i: ('R' if i in EXP2['red'] else 'G') for i in ids17}
    red_lab = [x['l'] for x in (g.get('prior') or []) if x['c'] == 'R']
    d = {'다시 그린 문항': (rr or {}).get('n'), '⚡ 열쇠 회독': (rr or {}).get('hist'),
         '채점 창 지난 결과': {'빨강': [i for i in ids17 if gi.get(i) == 'R'], '빨강 번호': red_lab, '초록 수': sum(1 for i in ids17 if gi.get(i) == 'G'),
                       '회색 수': sum(1 for i in ids17 if gi.get(i) == '-')},
         '계속 틀림': ids(g.get('always')), '극복함': ids(g.get('fixed')),
         'Q0695(148) 어느 쪽도 아님': EXP2['neither'] not in (ids(g.get('always')) or []) + (ids(g.get('fixed')) or []),
         '빨강 칩 톡': tap, '회독 비교 창': {'지난 결과 = 채점 창': cmap(c.get('prior')) == gi and bool(gi), '계속 틀림': ids(c.get('always')), '극복함': ids(c.get('fixed'))},
         '바탕 꼴(줄 머리)': None if g.get('prior') is not None else g.get('heads'), '하네스 따로 셈 = 지시서 값': exp_py,
         '훑기(INFO)': {'채점 창': sw_g, '회독 비교 창': sw_c}, '오류': errs[:3]}
    ok = ((rr or {}).get('n') == EXP2['n'] and gi == exp_c and red_lab == EXP2['red_lab'] and ids(g.get('always')) == EXP2['always']
          and ids(g.get('fixed')) == EXP2['fixed'] and d['Q0695(148) 어느 쪽도 아님'] and bool(tap) and tap['자리'] and tap['팝업'] is True
          and cmap(c.get('prior')) == exp_c and sorted(ids(c.get('always')) or []) == sorted(EXP2['always'])
          and sorted(ids(c.get('fixed')) or []) == sorted(EXP2['fixed'])   # 회독 비교 창 칩 차례 = 번호 차례(그 창 옛 규칙) → 모임으로 맞댐
          and exp_py is True and not errs)
    return ok, d


# ---------- W5 — 연결한 근거 줄 ----------
PICK_JS = r"""(()=>{const out=[];for(const q of quizData){let us=[];try{us=refOf(q.id,'geunge')}catch(e){us=[]}if(!us.length)continue;
  for(const u of us){if(refTextOf(u,'geunge')===null)continue;const L=ggOf(u).filter(Boolean);if(!L.length)continue;
    out.push([L.reduce((a,g)=>a+(Array.isArray(g.cs)?g.cs.filter(Boolean).length:0),0),L.length,String(q.id),String(u)])}}
  out.sort((a,b)=>b[0]-a[0]||b[1]-a[1]||(a[2]<b[2]?-1:a[2]>b[2]?1:0));const seen=new Set(),pick=[];
  for(const x of out){if(seen.has(x[2]))continue;seen.add(x[2]);pick.push(x);if(pick.length>=3)break}return pick})()"""
ROW_READY = r"""(s)=>{const L=[...document.querySelectorAll(s+' [data-gbbox] > div')].filter(r=>!r.classList.contains('hide')&&r.querySelector(':scope > button[onclick^="ggRefEdit("]'));
 return L.length>0&&L.every(r=>{const cs=getComputedStyle(r);return r.classList.contains('flex-wrap')?cs.flexWrap==='wrap':cs.display==='flex'})}"""   # Tailwind cdn 이 새로 생긴 줄 클래스(flex-wrap 등)를 만든 뒤에 잰다(접힌 고치기 칸 = hide 는 뺌)
MEASURE_JS = r"""(sel)=>{const box=document.querySelector(sel);if(!box||!__H.vis(box))return null;const out={rows:[],over:[]};
 const rows=[...box.querySelectorAll('[data-gbbox] > div')].filter(r=>__H.vis(r)&&r.querySelector(':scope > button[onclick^="ggRefEdit("]'));
 rows.forEach((r,ri)=>{const btn=r.querySelector(':scope > button[onclick^="ggRefEdit("]');btn.scrollIntoView({block:'center'});
   const cs=getComputedStyle(r),rb=r.getBoundingClientRect(),pl=parseFloat(cs.paddingLeft)||0,pr=parseFloat(cs.paddingRight)||0;
   const L=rb.left+(parseFloat(cs.borderLeftWidth)||0)+pl,W=r.clientWidth-pl-pr;
   const kids=[...r.children].filter(k=>k!==btn&&__H.vis(k));const right=Math.max(...kids.map(k=>k.getBoundingClientRect().right));const bb=btn.getBoundingClientRect();
   const inter=kids.some(k=>{const a=k.getBoundingClientRect();return Math.min(a.right,bb.right)-Math.max(a.left,bb.left)>0.5&&Math.min(a.bottom,bb.bottom)-Math.max(a.top,bb.top)>0.5});
   const hb=__W.hitExt(btn),k0=kids[0].getBoundingClientRect(),cx=bb.left+bb.width/2,cy=bb.top+bb.height/2;
   const bcs=getComputedStyle(btn),bf=getComputedStyle(btn,'::before'),kcs=getComputedStyle(kids[0]);
   out.rows.push({kind:r.classList.contains('pl-3')?'댓글':'본문',ratio:+((right-L)/W).toFixed(3),W:Math.round(W),btn:[+bb.width.toFixed(1),+bb.height.toFixed(1)],
     hit:[hb.w,hb.h],cut:[hb.cutUp,hb.cutDown],sameLine:bb.top<k0.top+6,atRight:Math.abs((rb.right-pr-(parseFloat(cs.borderRightWidth)||0))-bb.right)<=1.5,inter,
     up13:{own:__W.own(btn,cx,cy-13),outPx:+(bb.top-(cy-13)).toFixed(1)},
     rowH:+rb.height.toFixed(1),
     css:ri===0?{row:cs.display+' '+cs.flexWrap+' · overflow-y '+cs.overflowY,text:kcs.flexGrow+' '+kcs.flexShrink+' '+kcs.flexBasis+' min-w '+kcs.minWidth,btnML:bcs.marginLeft,before:{c:bf.content,h:bf.height,top:bf.top,pos:bf.position}}:undefined})});
 /* ✎ 끼리 침범 — 줄 i 의 겨냥 자리(그 줄 상자 안 · ✎ 가운데 ±18 · ✎ 가운데 · 왼끝 +2 · 오른끝 −2 세 세로줄)를 1px 마다 찔러 맨 위가 다른 ✎ 인 데(그 ✎ 줄 번호)
    · ✎ 가운데 사이(세로) — 띠 높이 계산 꼴 무관(겹침은 맨 위로만 잰다 · 옛 셈 = ::before 높이 가운데 맞춤 기하 짝은 걷음: 띠를 줄 상자로 자르면 기하가 거짓) */
 const eds=rows.map(r=>r.querySelector(':scope > button[onclick^="ggRefEdit("]'));
 rows.forEach((r,i)=>{const b=eds[i];b.scrollIntoView({block:'center'});const bb=b.getBoundingClientRect(),rb=r.getBoundingClientRect(),cy=bb.top+bb.height/2;
   /* 줄 경계 1.5px 는 뺌 — 잘림 네모는 화소에 맞춰 붙어 경계 한 줄은 이웃 줄 몫으로 잡힐 수 있다(분수 좌표) */
   const y0=Math.max(cy-18,rb.top+1.5),y1=Math.min(cy+18,rb.bottom-1.5),xs=[bb.left+bb.width/2,bb.left+2,bb.right-2],hit=new Set();let n=0,lo=null,hi=null;
   for(let y=y0;y<=y1;y+=1)for(const x of xs){n++;const a=document.elementsFromPoint(x,y)[0];const e=a&&a.closest&&a.closest('button[onclick^="ggRefEdit("]');
     if(e&&e!==b){const j=eds.indexOf(e);hit.add(j>=0?j+1:'?');const o=+(y-rb.top).toFixed(1);lo=lo===null?o:Math.min(lo,o);hi=hi===null?o:Math.max(hi,o)}}
   out.rows[i].conf=[...hit];out.rows[i].confN=n;if(hit.size)out.rows[i].confAt=[lo,hi,+rb.height.toFixed(1)]});
 if(eds.length)eds[0].scrollIntoView({block:'center'});const R=eds.map(b=>b.getBoundingClientRect());
 out.band={h:eds.length?getComputedStyle(eds[0],'::before').height:null,gaps:R.slice(1).map((b,i)=>+((b.top+b.height/2)-(R[i].top+R[i].height/2)).toFixed(1))};
 [...box.querySelectorAll('button,[onclick]')].filter(__H.vis).forEach(e=>{e.scrollIntoView({block:'center'});const b=e.getBoundingClientRect(),x=b.left+b.width/2,y=b.top+b.height/2;
   if(!__W.own(e,x,y))out.over.push((e.tagName+'.'+String(e.className).slice(0,18))+' → '+__W.sig(document.elementsFromPoint(x,y)[0]))});
 out.coarse=matchMedia('(pointer:coarse)').matches;return out}"""
ED_JS = r"""(sel)=>[...document.querySelectorAll(sel+' button[onclick^="ggRefEdit("]')].filter(b=>__H.vis(b)&&/고치기/.test(b.textContent))"""   # 「✎ 여기서 고치기」 만(칸 안 「취소」 도 ggRefEdit)
PRESS_JS = r"""(sel)=>(""" + ED_JS + r""")(sel).map(b=>{const m=/ggRefEdit\(([^)]*)\)/.exec(b.getAttribute('onclick')||'');const a=m?m[1].split(',').map(x=>x.trim().replace(/^'|'$/g,'')):[];
  return {uid:a[0],u:a[1],k:a[2],ck:(a[3]&&a[3]!=='undefined')?a[3]:null}})"""
NTH_SAFE = "([s,i])=>__W.safe((" + ED_JS + ")(s)[i])"
NTH_RECT = "([s,i])=>{const b=(" + ED_JS + r""")(s)[i];if(!b)return null;b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return {cx:r.left+r.width/2,cy:r.top+r.height/2,h:+r.height.toFixed(1)}}"""
OPEN_JS = r"""(e)=>{const b=document.querySelector(e);return !!b&&!b.classList.contains('hide')&&__H.vis(b)}"""
SHUT_JS = r"""(e)=>{const b=document.querySelector(e);return !!b&&b.classList.contains('hide')}"""


def edit_box_sel(t):
    eid = '%s-%s-%s' % (t['uid'], t['u'], t['k']) + ('-' + t['ck'] if t['ck'] is not None else '')
    return ('#qp-refgg-cedit-' if t['ck'] is not None else '#qp-refgg-edit-') + eid, ('#qp-refgg-cein-' if t['ck'] is not None else '#qp-refgg-ein-') + eid


def press_test(p, box, phone=True):
    """✎ 진짜 톡 → 칸 열림 · 글 = 저장된 글 · 「취소」 진짜 톡 → 닫힘 · 단추 네모 위 13px 진짜 톡 → 열림(넓힌 누를 자리 · 폰만 잣대 —
    iPad 한 줄 꼴은 13px 위가 윗줄 자리라 INFO: ox_fix 뒤엔 윗줄 칸이 열리는 게 맞다)"""
    out = []
    for i, t in enumerate(p.ev(PRESS_JS, box)[:3]):
        esel, isel = edit_box_sel(t)
        row = '댓글' if t['ck'] is not None else '본문'
        at = p.ev(NTH_SAFE, [box, i])
        if not at or not at.get('on'):
            out.append({'줄': row, '톡 → 열림': False, '까닭': '단추 누를 점 없음 ' + _s(at)[:80]})
            continue
        p.tap(at)
        op = QC.until(p.pg, OPEN_JS, 3000, 'W5 ✎ 톡 → 고치기 칸', arg=esel)
        same = p.ev("""([i,u,k,ck])=>{const inp=document.querySelector(i);const g=ggItem(u,k);const c=(g&&ck!==null)?ggCsOf(g,ck):null;
          return !!inp&&!!g&&inp.value===(ck!==null?((c&&c.t)||''):(g.t||''))}""", [isel, t['u'], t['k'], t['ck']])
        cancel = p.ev("(e)=>{const b=document.querySelector(e);const x=b?[...b.querySelectorAll('button')].find(z=>/취소/.test(z.textContent)):null;return x?__W.safe(x):null}", esel)
        closed = None
        if cancel and cancel.get('on'):
            p.tap(cancel)
            closed = QC.until(p.pg, SHUT_JS, 3000, 'W5 취소 톡 → 닫힘', arg=esel)
        r2 = p.ev(NTH_RECT, [box, i])
        edge = None
        if r2:
            pt = p.ev("([s,i,x,y])=>{const b=(" + ED_JS + ")(s)[i];return {own:!!b&&__W.own(b,x,y),top:__W.sig(document.elementsFromPoint(x,y)[0])}}", [box, i, r2['cx'], r2['cy'] - 13])
            own = pt['own']
            if own:   # 그 점 맨 위가 이 ✎ 일 때만 진짜 톡 — 남의 자리(윗줄 ✎ · 상자 머리 「× 연결 끊기」 등)를 누르면 상자가 바뀐다(10/10 iPad 잼)
                p.tap_xy(r2['cx'], r2['cy'] - 13)
                eo = QC.until(p.pg, OPEN_JS, 3000, 'W5 단추 네모 위 13px 톡 → 고치기 칸', arg=esel)
            else:
                eo = False
            edge = {'단추 높이': r2['h'], '네모 밖(px)': round(13 - r2['h'] / 2, 1), '그 점 맨 위 = 단추': own, '열림': eo} if own else \
                   {'단추 높이': r2['h'], '네모 밖(px)': round(13 - r2['h'] / 2, 1), '그 점 맨 위 = 단추': False, '그 점 맨 위': pt['top'], '톡': '안 함(남의 자리)', '열림': False}
            p.ev(CLOSE_ALL, p.ev(EDS_JS, box))   # 뒷정리
            p.wait(200, 'W5 고치기 칸 닫음(뒷정리)')
        out.append({'줄': row, '톡 → 열림': op, '글 = 저장된 글': same, '취소 톡 → 닫힘': closed, '네모 위 13px' + ('' if phone else '(INFO)'): edge, '톡 여백': at.get('margin')})
    ok = bool(out) and all(x.get('톡 → 열림') and x.get('글 = 저장된 글') and x.get('취소 톡 → 닫힘') and (not phone or (x.get('네모 위 13px') or {}).get('열림')) for x in out)
    return ok, out


OPEN_IDX = r"""(L)=>L.findIndex(e=>{const b=document.querySelector(e);return !!b&&!b.classList.contains('hide')})"""
CLOSE_ALL = r"""(L)=>L.forEach(e=>{const b=document.querySelector(e);if(b&&!b.classList.contains('hide')){const x=[...b.querySelectorAll('button')].find(z=>/취소/.test(z.textContent));if(x)x.click()}})"""
EDS_JS = r"""(sel)=>(""" + ED_JS + r""")(sel).map(b=>{const m=/ggRefEdit\(([^)]*)\)/.exec(b.getAttribute('onclick')||'');const a=m?m[1].split(',').map(x=>x.trim().replace(/^'|'$/g,'')):[];
  const ck=(a[3]&&a[3]!=='undefined')?a[3]:null,eid=a[0]+'-'+a[1]+'-'+a[2]+(ck!==null?'-'+ck:'');return (ck!==null?'#qp-refgg-cedit-':'#qp-refgg-edit-')+eid})"""   # ✎ 차례대로 그 줄 고치기 칸 자리


def tap3(p, box):
    """✎ 마다 가운데 위 3px · 아래 3px 진짜 톡 → 열린 고치기 칸 = 그 줄인가(10/10 [채팅] 03:50 ㉠ 관문 · 56836b8 iPad = 본문 ✎ +3px 에 아랫줄 칸)"""
    eds = p.ev(EDS_JS, box)
    out = []
    for i in range(len(eds)):
        for dy in (-3, 3):
            p.ev(CLOSE_ALL, eds)
            rc = p.ev(NTH_RECT, [box, i])
            if not rc:
                out.append({'줄': i + 1, 'dy': dy, '열린 칸': '단추 없음'})
                continue
            p.tap_xy(rc['cx'], rc['cy'] + dy)
            QC.until(p.pg, "(L)=>L.some(e=>{const b=document.querySelector(e);return !!b&&!b.classList.contains('hide')})", 1500, 'W5 ±3px 톡 → 고치기 칸', arg=eds)
            j = p.ev(OPEN_IDX, eds)
            out.append({'줄': i + 1, 'dy': dy, '열린 칸': ('제 줄' if j == i else ('%d번 줄' % (j + 1)) if j >= 0 else '없음')})
        p.ev(CLOSE_ALL, eds)
        p.wait(150, 'W5 ±3px 톡 뒷정리')
    return out


def box_png(p, box):
    """상자 그림(겉모양 무변 맞댐 · 출력 안 함) — 상자를 가운데로 · 0.7 초 가라앉힘(Tailwind cdn 이 새로 생긴 클래스를 늦게 만든다) ·
    0.25 초 사이 두 번 같을 때까지(최대 8 번)"""
    try:
        p.ev("(s)=>{const b=document.querySelector(s);if(b)b.scrollIntoView({block:'center'})}", box)
    except Exception:
        return None
    p.wait(700, 'W5 상자 그림 전 가라앉힘(늦게 생기는 Tailwind 클래스 · 10/10 웹킷 iPad 그림 흔들림 1 번)')
    last = None
    for _ in range(8):
        try:
            b = p.pg.locator(box).screenshot(animations='disabled')
        except Exception:
            return None
        if b == last:
            return b
        last = b
        p.pg.wait_for_timeout(250)
    return last


PNG_TOL = (4, 64)   # 겉모양 무변 허용 — 화소 값 차 ≤ 4(256 단계) · 다른 화소 ≤ 64(DPR 2) = 눈에 안 보이는 앤티앨리어싱만 —
                    # 10/10 잼: Chromium 폰 점선 테두리 끝 8 화소 · 차 1(늘 같음) · 웹킷 iPad 상자 둥근 모서리 4 화소 · 차 4(흔들림 — 같은 판끼리 다시 재면 0) · 글자 잘림 · 줄 밀림은 이보다 훨씬 큼


def png_same(a, b):
    """같음 = True(바이트 같음 또는 허용 안) · 다름 = False · 잰 값 = (판정, {다른 화소 · 최대 차 · 네모})"""
    if a is None or b is None:
        return None, {'그림': '없음'}
    if a == b:
        return True, {'다른 화소': 0}
    try:
        from PIL import Image, ImageChops
        import io
        ia, ib = Image.open(io.BytesIO(a)).convert('RGB'), Image.open(io.BytesIO(b)).convert('RGB')
        if ia.size != ib.size:
            return False, {'크기': [ia.size, ib.size]}
        d = ImageChops.difference(ia, ib)
        bb = d.getbbox()
        if not bb:
            return True, {'다른 화소': 0}
        dc = d.crop(bb)
        px = [q for q in (dc.get_flattened_data() if hasattr(dc, 'get_flattened_data') else dc.getdata()) if q != (0, 0, 0)]   # Pillow 14 에서 getdata 걷힘
        mx = max(max(q) for q in px)
        return (mx <= PNG_TOL[0] and len(px) <= PNG_TOL[1]), {'다른 화소': len(px), '최대 차': mx, '네모(DPR2)': list(bb)}
    except Exception as e:
        return False, {'오류': str(e)[:80]}


def w5(br, v, dev, eng='webkit'):
    p = WL(br, v, dev, 'W5' + ('' if eng == 'webkit' else '·' + eng))
    res = []
    try:
        picks = p.ev(PICK_JS)
        for ncs, ngg, uid, u in picks:
            p.ev("(o)=>{openQPopup(o)}", uid)
            QC.until(p.pg, "(o)=>!!document.getElementById('oxwin-q-'+o)", 5000, 'W5 문항 팝업', arg=uid)
            p.wait(500, 'W5 팝업 그림 가라앉힘')
            chip = '#qp-gg-refchip-%s-%s' % (uid, u)
            at = p.ev("(s)=>__W.safe(document.querySelector(s))", chip)
            if at and at.get('on'):
                p.tap(at)
            else:
                p.ev("([o,u])=>{ggRefToggle(o,u,'qp-')}", [uid, u])
            box = '#qp-refgg-box-%s-%s' % (uid, u)
            vis = QC.until(p.pg, "(s)=>{const b=document.querySelector(s);return !!b&&__H.vis(b)}", 3000, 'W5 🔗 칩 톡 → 연결 상자', arg=box)
            ready = QC.until(p.pg, ROW_READY, 4000, 'W5 줄 꼴(Tailwind 클래스 생김)', arg=box) if vis else False
            m = p.ev(MEASURE_JS, box) if vis else None
            sw = p.ev(SWEEP_JS, box) if vis else ['상자 안 펴짐']
            png = box_png(p, box) if (vis and GATE) else None   # 겉모양 무변 맞댐(누르기 전 · gate 만)
            p.shot('w5_%s_%s_%s_%s' % (eng, v, dev['name'], uid))
            pr = press_test(p, box, dev['name'] == '폰') if vis else (False, [])
            t3 = tap3(p, box) if vis else []
            res.append({'문항': uid, '연결': u, '댓글': ncs, '칩 톡 자리': bool(at and at.get('on')), '펴짐': vis, '줄 꼴 준비': ready, '잼': m, '훑기': sw, '누름': pr, '±3px': t3, 'png': png})
            p.ev("(o)=>{try{oxWinClose('q-'+o)}catch(e){}const w=document.getElementById('oxwin-q-'+o);if(w)w.remove()}", uid)
            p.wait(300, 'W5 팝업 닫음')
        errs = p.errors()
    finally:
        p.close()
    phone = dev['name'] == '폰'
    rows = [(x['문항'], r) for x in res for r in ((x['잼'] or {}).get('rows') or [])]
    bad = [(q, r['kind'], r['ratio'], r['inter'], r['atRight']) for q, r in rows
           if not ((r['ratio'] >= 0.9 or not phone) and not r['inter'] and r['atRight'])]
    over = [(x['문항'], x['잼']['over']) for x in res if x['잼'] and x['잼']['over']]
    coarse = all((x['잼'] or {}).get('coarse') for x in res if x['잼'])
    d = {'표본(문항 · 연결 · 댓글)': [(x['문항'], x['연결'], x['댓글']) for x in res], '줄': len(rows),
         '글 폭 / 줄 폭(최소)' + ('' if phone else ' · INFO'): min((r['ratio'] for _, r in rows), default=None),
         '한 줄(단추 = 글 첫 줄)': sum(1 for _, r in rows if r['sameLine']),
         '단추 네모(첫 줄)': rows[0][1]['btn'] if rows else None, '줄 폭': sorted({r['W'] for _, r in rows}), '(pointer:coarse)': coarse,
         '칩 톡 · 펴짐 · 줄 꼴': [(x['칩 톡 자리'], x['펴짐'], x['줄 꼴 준비']) for x in res], '계산 꼴(첫 줄)': rows[0][1].get('css') if rows else None,
         '네모 위 13px 점 맨 위 = 단추' + ('' if phone else '(INFO)'): [r['up13'] for _, r in rows][:7], '어긋난 줄(글 폭 · 겹침 · 오른끝)': bad[:6], '가려진 누를 것': over[:4],
         '누름': [{'문항': x['문항'], '줄': x['누름'][1]} for x in res], '훑기(INFO)': [(x['문항'], x['훑기']) for x in res if x['훑기']], '오류': errs[:3]}
    ok = (len(res) == 3 and bool(rows) and all(x['펴짐'] and x['칩 톡 자리'] for x in res) and not bad and not over and coarse
          and all(x['누름'][0] for x in res) and not errs)
    # ② 누를 자리 — 폭 ≥ 36 · 높이 폰 ≥ 36 · iPad ≥ min(36, 그 줄 높이) − 2(줄 사이만큼 · [채팅] 03:50 ㉠) · ✎ 끼리 침범 0 · ±3px 톡 = 그 줄 칸
    need = (lambda r: 36) if phone else (lambda r: min(36.0, r.get('rowH') or 0) - 2)
    small = [(q, r['kind'], r['hit'], r.get('rowH'), r['cut']) for q, r in rows if r['hit'][0] < 36 or r['hit'][1] < need(r)]
    conf = [(q, i + 1, r['kind'], r.get('conf'), r.get('confAt')) for q, rr in [(x['문항'], (x['잼'] or {}).get('rows') or []) for x in res] for i, r in enumerate(rr) if r.get('conf')]
    t3bad = [(x['문항'], t) for x in res for t in x['±3px'] if t['열린 칸'] != '제 줄']
    t3n = sum(len(x['±3px']) for x in res)
    dh = {'줄': len(rows), '누를 자리 폭 · 높이(최소)': [min((r['hit'][0] for _, r in rows), default=None), min((r['hit'][1] for _, r in rows), default=None)],
          '줄마다(문항 · 줄 · 폭×높이 · 줄 높이)': [(q, r['kind'], r['hit'], r.get('rowH')) for q, r in rows][:7],
          '못 미친 줄(문항 · 줄 · 폭×높이 · 줄 높이 · 막은 것 위/아래)': small[:7], '띠(::before 높이 · ✎ 가운데 사이 px)': [(x['문항'], ((x['잼'] or {}).get('band') or {}).get('h'), ((x['잼'] or {}).get('band') or {}).get('gaps')) for x in res],
          '✎ 끼리 침범(문항 · 줄 · 덮은 ✎ 줄)': conf, '±3px 톡(톡 수 · 그 줄 아님)': [t3n, t3bad[:6]], '(pointer:coarse)': coarse,
          '잣대': '폭 ≥ 36 · 높이 ' + ('≥ 36' if phone else '≥ min(36, 줄 높이) − 2(줄 사이만큼)') + ' · 침범 0 · ±3px 톡 = 그 줄'}
    ok_h = bool(rows) and not small and not conf and t3n == 2 * len(rows) and not t3bad and coarse
    pngs = {x['문항']: x['png'] for x in res}
    return (ok, d), (ok_h, dh), pngs


# ---------- W6 — 「× 연결 끊기」 되묻기(사용자 10/10 08:3x 「더하기」 · ox_del) ----------
NAT_CONFIRM = "window.__natConfirm = window.confirm;"   # OL.INIT 가 confirm 을 「늘 참」 으로 갈기 전 진짜 것을 잡아 둠 → 칸에서 되돌려 진짜 되묻기 창(page.on('dialog'))
LINKED_JS = r"""([o,u])=>refOf(o,'geunge').map(x=>String(x).toUpperCase()).includes(String(u).toUpperCase())"""
XBTN_JS = r"""(box)=>{const b=document.querySelector(box);if(!b||!__H.vis(b))return null;const x=[...b.querySelectorAll('button')].find(z=>/연결 끊기/.test(z.textContent));return x?__W.safe(x):null}"""
STAMP_JS = r"""(o)=>{try{stampAll()}catch(e){}const u=JSON.parse(localStorage.getItem('ox_sync_u')||'{}'),g=JSON.parse(localStorage.getItem('ox_sync_gone')||'{}'),k='ox_q_reflinks|'+o;
 return {u:u[k]||null,gone:g[k]||null,now:Date.now()}}"""   # 앱 도장(stampAll · 10 초마다 도는 것)을 지금 한 번 — 그 칸 도장 · 묘비
MISS_JS = r"""(box)=>{const b=document.querySelector(box);if(!b)return null;
 const ed=[...b.querySelectorAll('button[onclick^="ggRefEdit("]')].find(x=>__H.vis(x)&&/고치기/.test(x.textContent));const xb=[...b.querySelectorAll('button')].find(x=>/연결 끊기/.test(x.textContent));
 if(!ed||!xb)return null;ed.scrollIntoView({block:'center'});const r=ed.getBoundingClientRect(),cx=r.left+r.width/2,xr=xb.getBoundingClientRect();
 for(let dy=1;dy<=24;dy++){const y=r.top-dy,a=document.elementsFromPoint(cx,y)[0];if(a&&(a===xb||xb.contains(a)))return {x:cx,y:y,dy:dy,gap:+(r.top-xr.bottom).toFixed(1)}}
 return {none:true,gap:+(r.top-xr.bottom).toFixed(1)}}"""   # 본문 ✎ 위로 1~24px 찔러 맨 위가 「× 연결 끊기」 인 첫 점(iPad 한 줄 꼴 = 빗누름 자리 · 폰 = 없음)
CLOSE_WINS = r"""(()=>{document.querySelectorAll('[id^="oxwin-"]').forEach(w=>{try{oxWinClose(w.id.slice(6))}catch(e){}if(w.isConnected)w.remove()})})()"""


def w6(br, v, dev, eng='webkit'):
    """× 진짜 톡 → 되묻기 창(진짜 confirm · page.on('dialog') · 한 번 · 글) · 「취소」 = 연결 그대로(기록 · 화면 · 도장) · 「확인」 = 끊김(기록 · 화면 · 도장 · 원격 PUT) ·
    (iPad) 본문 ✎ 위 빗누름 = 되묻기만 · 쓰임 창(useWin → useUnlink) 끊기 = 되묻기 없이 끊김"""
    p = WL(br, v, dev, 'W6' + ('' if eng == 'webkit' else '·' + eng), pre_init=NAT_CONFIRM)
    DLG, ANS = [], {'v': False}

    def on_dlg(dg):
        DLG.append({'종류': dg.type, '글': dg.message})
        try:
            dg.accept() if ANS['v'] else dg.dismiss()
        except Exception:
            pass
    p.pg.on('dialog', on_dlg)
    out = {}
    try:
        p.ev("()=>{if(window.__natConfirm)window.confirm=window.__natConfirm}")   # OL.INIT 의 「늘 참」 걷음 — 진짜 되묻기 창
        picks = p.ev(PICK_JS)
        if len(picks) < 2:
            return False, {'까닭': '연결한 근거 표본 둘 못 고름', '표본': picks}
        _n, _g, uid, u = picks[0]
        _n2, _g2, uid2, u2 = picks[1]
        out['표본(톡 · 쓰임 창)'] = [[uid, u], [uid2, u2]]
        p.ev("(o)=>{openQPopup(o)}", uid)
        QC.until(p.pg, "(o)=>!!document.getElementById('oxwin-q-'+o)", 5000, 'W6 문항 팝업', arg=uid)
        p.wait(500, 'W6 팝업 그림 가라앉힘')
        at = p.ev("(s)=>__W.safe(document.querySelector(s))", '#qp-gg-refchip-%s-%s' % (uid, u))
        if at and at.get('on'):
            p.tap(at)
        else:
            p.ev("([o,u])=>{ggRefToggle(o,u,'qp-')}", [uid, u])
        box = '#qp-refgg-box-%s-%s' % (uid, u)
        QC.until(p.pg, "(s)=>{const b=document.querySelector(s);return !!b&&__H.vis(b)}", 3000, 'W6 연결 상자', arg=box)
        st0 = p.ev(STAMP_JS, uid)
        # A — × 진짜 톡 · 「취소」
        ANS['v'] = False
        n0 = len(DLG)
        xa = p.ev(XBTN_JS, box)
        if xa and xa.get('on'):
            p.tap(xa)
        p.wait(500, 'W6 × 톡 뒤')
        stA = p.ev(STAMP_JS, uid)
        out['A × 톡 · 취소'] = {'톡 자리': bool(xa and xa.get('on')), '되묻기 수': len(DLG) - n0, '글': [d['글'] for d in DLG[n0:]][:2], '종류': [d['종류'] for d in DLG[n0:]][:2],
                              '연결 그대로(기록)': p.ev(LINKED_JS, [uid, u]), '상자 그대로(화면)': p.ev("(s)=>{const b=document.querySelector(s);return !!b&&__H.vis(b)}", box),
                              '도장 무변': [stA['u'], stA['gone']] == [st0['u'], st0['gone']]}
        # B — (iPad 한 줄 꼴) 본문 ✎ 조금 위 빗누름 · 「취소」
        mp = p.ev(MISS_JS, box)
        if mp and not mp.get('none'):
            ANS['v'] = False
            n0 = len(DLG)
            p.tap_xy(mp['x'], mp['y'])
            p.wait(500, 'W6 빗누름 톡 뒤')
            out['B ✎ 위 빗누름 · 취소'] = {'점(✎ 위 px)': mp['dy'], '✎ ↔ × 틈(px)': mp['gap'], '되묻기 수': len(DLG) - n0, '연결 그대로(기록)': p.ev(LINKED_JS, [uid, u]),
                                      '상자 그대로(화면)': p.ev("(s)=>{const b=document.querySelector(s);return !!b&&__H.vis(b)}", box)}
        else:
            out['B ✎ 위 빗누름 · 취소'] = {'없음(✎ 위 24px 안에 × 없음)': True, '✎ ↔ × 틈(px)': (mp or {}).get('gap')}
        # C — × 진짜 톡 · 「확인」
        ANS['v'] = True
        n0 = len(DLG)
        xc = p.ev(XBTN_JS, box)
        if xc and xc.get('on'):
            p.tap(xc)
        p.wait(600, 'W6 × 톡 · 확인 뒤')
        stC = p.ev(STAMP_JS, uid)
        okst = bool((stC['u'] and stC['u'] >= st0['now']) or (stC['gone'] and stC['gone'] >= st0['now']))
        p.ev("async()=>{try{await syncRecords(true)}catch(e){}}")
        rb = p.remote.files.get('minbeop/기록.json')
        rem = None
        if rb:
            try:
                rd = json.loads(rb.decode('utf-8'))
                rl = (rd.get('data') or {}).get('ox_q_reflinks') or {}
                rl = json.loads(rl) if isinstance(rl, str) else rl
                rem = str(u).upper() not in [str(x).upper() for x in ((rl.get(uid) or {}).get('geunge') or [])]
            except Exception as e:
                rem = '읽기 오류 ' + str(e)[:60]
        out['C × 톡 · 확인'] = {'톡 자리': bool(xc and xc.get('on')), '되묻기 수': len(DLG) - n0, '끊김(기록)': not p.ev(LINKED_JS, [uid, u]),
                              '상자 없음(화면)': not p.ev("(s)=>{const b=document.querySelector(s);return !!b&&__H.vis(b)}", box),
                              '도장 · 묘비(동기화 칸)': okst, '원격 기록에서 빠짐(syncRecords)': rem}
        # D — 쓰임 창 켜고 끄기 길(useUnlink) — 되묻지 않음
        p.ev(CLOSE_WINS)
        p.wait(300, 'W6 창 닫음')
        ANS['v'] = False
        n0 = len(DLG)
        p.ev("([t,m])=>{useWin('geunge',t,m)}", [u2, uid2])
        QC.until(p.pg, "(t)=>!!document.getElementById('oxwin-use-geunge-'+t)", 4000, 'W6 쓰임 창', arg=u2)
        p.wait(400, 'W6 쓰임 창 그림')
        ua = p.ev("(t)=>{const w=document.getElementById('oxwin-use-geunge-'+t);const b=w?w.querySelector('button[onclick^=\"useUnlink(\"]'):null;return b?__W.safe(b):null}", u2)
        if ua and ua.get('on'):
            p.tap(ua)
        p.wait(500, 'W6 쓰임 창 끊기 톡 뒤')
        out['D 쓰임 창 끊기(useUnlink)'] = {'톡 자리': bool(ua and ua.get('on')), '되묻기 수': len(DLG) - n0, '끊김(기록)': not p.ev(LINKED_JS, [uid2, u2])}
        errs = p.errors()
        out['오류'] = errs[:3]
    finally:
        p.close()
    phone = dev['name'] == '폰'
    a, b_, c, d4 = out.get('A × 톡 · 취소') or {}, out.get('B ✎ 위 빗누름 · 취소') or {}, out.get('C × 톡 · 확인') or {}, out.get('D 쓰임 창 끊기(useUnlink)') or {}
    u_ = (out.get('표본(톡 · 쓰임 창)') or [[None, '']])[0][1]
    msg_ok = len(a.get('글') or []) == 1 and '연결을 끊' in a['글'][0] and str(u_) in a['글'][0] and (a.get('종류') or [''])[0] == 'confirm'
    b_ok = (('없음(✎ 위 24px 안에 × 없음)' in b_) if phone else False) or (b_.get('되묻기 수') == 1 and b_.get('연결 그대로(기록)') is True and b_.get('상자 그대로(화면)') is True)
    ok = (a.get('톡 자리') and a.get('되묻기 수') == 1 and msg_ok and a.get('연결 그대로(기록)') is True and a.get('상자 그대로(화면)') is True and a.get('도장 무변') is True
          and b_ok and c.get('톡 자리') and c.get('되묻기 수') == 1 and c.get('끊김(기록)') is True and c.get('상자 없음(화면)') is True and c.get('도장 · 묘비(동기화 칸)') is True
          and c.get('원격 기록에서 빠짐(syncRecords)') is True and d4.get('톡 자리') and d4.get('되묻기 수') == 0 and d4.get('끊김(기록)') is True and not out.get('오류'))
    out['잣대'] = '× 톡 = 되묻기 한 번(confirm · 글에 「연결을 끊」 · 그 문항 ID) · 취소 = 그대로 · 확인 = 끊김 · ' + ('폰 = 빗누름 자리 없음' if phone else 'iPad = ✎ 위 빗누름 = 되묻기만') + ' · 쓰임 창 = 되묻기 없이 끊김'
    return bool(ok), out


# ---------- 차례 ----------
def main():
    os.makedirs(TMPD, exist_ok=True)
    R('W0', '판 · 자리', None, None, {'NEW': NEWF, 'md5(LF)': {k: OL.md5lf(s) for k, s in SRC.items()}, 'BASE': BASE, 'SPD': OL.CONF['spd'],
                                     '데이터 판': DREV or '(작업트리)', 'W4 기록': REC_REV, 'tw': OL.CONF['tw'], '모드': QC.MODE, '기기': [x['name'] for x in DEVS]})
    rec_b, exp_py = None, None
    if want('W4'):
        rec_b = rec_bytes()
        if rec_b:
            exp_py, ed = w4_expect(rec_b)
            R('W4', '하네스 따로 셈(기록 %s · 모든 열쇠 · 문항마다 마지막) = 지시서 값' % REC_REV, None, None, dict(ed, 맞음=exp_py))
    plan = [('W1', '첫 화면 검색 「%s」 — 칸 톡 · 셈 = 기대 · 처음 100 · 「상위 N건만」 0 · 끝까지 굴려 다(모바일 웹킷 = scrollTop) · 차례 · 겹침 0 · 끝 줄 톡 = 그 문항 팝업' % TERM, w1, True),
            ('W1', '같은 칸 휠 굴림(비모바일 웹킷 · has_touch · 같은 크기 — 믿는 입력 굴림 길) — 끝까지 다 · 차례 · 끝 줄 톡 = 팝업' , lambda br, v, dev: w1(br, v, dev, mobile=False), True),
            ('W2', '연결 창 찾기(lwOpen) — 100 넘는 말 · 셈 보임 · 처음 100 · 끝까지 굴려 다 붙음 · 차례', w2_link, True),
            ('W2', '근거 창 찾기(문항 팝업 🔍 톡 · linkSearch) — 100 넘는 말 · 셈 · 처음 100 · 끝까지 다 · 차례 · 칸 다시 톡 = 줄 · 자리 그대로', w2_geunge, True),
            ('W3', '「%s」 굴리는 중 검색 칸 톡 → 「%s」 — 옛 줄 0 · 첫 100 = 기대 앞 100 · 맨 위 · 끝까지 = 기대' % (TERM, TERM2), w3, None),
            ('W4', '⚡ 채점 창 실데이터 %s — 빨강 3(2) · 5 · 158 · 83 · 초록 13 · 계속 틀림 3(2) · 극복함 5 · 158 · 83 · 빨강 칩 톡 = 팝업 · 회독 비교 창 같음' % REC_REV, None, True)]
    W5N = ['연결한 근거 펼침(🔗 칩 톡) — 줄 오른끝 · 글 ↔ 단추 겹침 0 · 누를 것 가운데 = 제 것 · 톡 = 고치기 칸(글 = 저장된 글) · 취소 = 닫힘 · (폰) 네모 위 13px 톡 = 열림 · 글 폭 ≥ 0.90'
           + (' · 그림 = %s(겉모양 무변)' % BASE2 if GATE else ''),
           '연결한 근거 ✎ 누를 자리 — 폭 ≥ 36 · 높이 폰 ≥ 36 · iPad 줄 사이만큼 · ✎ 끼리 침범 0 · ✎ 가운데 ±3px 톡 = 그 줄 칸']

    def run_w5(br, eng, dev):
        """W5 — 새 판 · 바탕(7299ec3) · 56836b8(gate) 을 한 엔진 · 한 기기로 · 줄 둘(① 꼴 · 누름 / ② 누를 자리)"""
        t1 = time.time()
        res = {}
        for v in VERS5:
            try:
                res[v] = w5(br, v, dev, eng)
            except Exception as e:
                bad = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-700:]})
                res[v] = (bad, bad, {})
        if 'B2' in res:   # gate — 상자 그림 새 판 = 56836b8(투명 띠 · 줄 clip 은 그림을 안 바꿔야 · 허용 = PNG_TOL)
            cmp = {u: png_same(res['NEW'][2].get(u), res['B2'][2].get(u)) for u in (res['NEW'][2] or {})}
            ok1, d1 = res['NEW'][0]
            okp = bool(cmp) and all(x[0] is True for x in cmp.values())
            if not okp and OL.CONF['shots']:   # 다르면 두 그림을 남김(--shots · 글이 든 그림이라 출력 안 함)
                try:
                    os.makedirs(OL.CONF['shots'], exist_ok=True)
                    for u in cmp:
                        for tg in ('NEW', 'B2'):
                            bb = res[tg][2].get(u)
                            if bb:
                                open(os.path.join(OL.CONF['shots'], 'w5png_%s_%s_%s_%s.png' % (eng, dev['name'], u, tg)), 'wb').write(bb)
                except Exception:
                    pass
            res['NEW'] = ((ok1 and okp, dict(d1, **{'그림 = %s(겉모양 무변 · 허용 차 ≤ %d · 화소 ≤ %d)' % ((BASE2,) + PNG_TOL): {u: x[1] for u, x in cmp.items()}})),
                          res['NEW'][1], res['NEW'][2])
        phone = dev['name'] == '폰'
        devn = dev['name'] + ('' if eng == 'webkit' else '·' + {'chromium': 'Chromium'}.get(eng, eng))
        for ni, nm in enumerate(W5N):
            b = res['BASE'][ni][0] if 'BASE' in res else None
            b2 = res['B2'][ni][0] if 'B2' in res else None
            if ni == 1 and not phone:   # ② iPad — 헛잣대 = 56836b8(7299ec3 은 띠가 없어 「잘못 열림 0」 = 이 칸 헛잣대가 못 됨)
                ycol, y = 'B2', True
            else:
                ycol, y = 'BASE', (True if phone else (b is False))   # ① iPad 는 바탕도 같으면 「바탕 = 기준」
            dd = {k: x[ni][1] for k, x in res.items()}
            if ni == 1 and not phone and GATE:
                dd['헛잣대 열'] = '%s — 7299ec3 은 ✎ 띠가 없어 이 칸(잘못 열림 · 침범)이 늘 0 · 56836b8 = 띠 겹침 판([채팅] 03:50 ㉠)' % BASE2
            R('W5', '%s %s' % (devn, nm), res['NEW'][ni][0], b, dd, yard=y, b2=b2, ycol=ycol)
        k = 'W5·%s' % devn
        STEP[k] = round(STEP.get(k, 0) + (time.time() - t1) / 60, 2)

    W6N = '「× 연결 끊기」 되묻기 — × 톡 = 되묻기 한 번(글) · 취소 = 그대로(기록 · 화면 · 도장) · 확인 = 끊김(기록 · 화면 · 도장 · 원격) · iPad ✎ 위 빗누름 = 되묻기만 · 쓰임 창 끊기 = 되묻기 없이'

    def run_w6(br, eng, dev):
        """W6 — 새 판 · d48e4a8(gate · 헛잣대 = 되묻기 없이 바로 끊김) 을 한 엔진 · 한 기기로"""
        t1 = time.time()
        res = {}
        for v in VERS6:
            try:
                res[v] = w6(br, v, dev, eng)
            except Exception as e:
                res[v] = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-700:]})
        devn = dev['name'] + ('' if eng == 'webkit' else '·' + {'chromium': 'Chromium'}.get(eng, eng))
        dd = {k: x[1] for k, x in res.items()}
        if 'B3' in res:
            dd['헛잣대 열'] = '%s(main · ox_fix 들어간 판) — 「× 연결 끊기」 가 되묻지 않고 바로 끊음' % BASE3
        R('W6', '%s %s' % (devn, W6N), res['NEW'][0], None, dd, yard=True, b3=(res['B3'][0] if 'B3' in res else None), ycol='B3')
        k = 'W6·%s' % devn
        STEP[k] = round(STEP.get(k, 0) + (time.time() - t1) / 60, 2)

    with sync_playwright() as pw:
        br = pw.webkit.launch()
        ENV['webkit'] = br.version
        for dev in DEVS:
            for cid, name, fn, yard in plan:
                if not want(cid) or (QC.SMOKE and cid == 'W1' and fn is not w1):   # smoke = 모바일 W1 만(휠 갈래 뺌)
                    continue
                t1 = time.time()
                res = {}
                for v in VERS:
                    try:
                        res[v] = w4(br, v, dev, rec_b, exp_py) if cid == 'W4' else fn(br, v, dev)
                    except Exception as e:
                        res[v] = (False, {'하네스 오류': str(e)[:300], 'tb': traceback.format_exc()[-700:]})
                b = res['BASE'][0] if 'BASE' in res else None
                y = yard if yard is not None else (b is False)   # W3 = 바탕도 같으면 「바탕 = 기준」(헛잣대 셈 밖)
                R(cid, '%s %s' % (dev['name'], name), res['NEW'][0], b, {k: x[1] for k, x in res.items()}, yard=y)
                k = '%s·%s' % (cid, dev['name'])
                STEP[k] = round(STEP.get(k, 0) + (time.time() - t1) / 60, 2)
            if want('W5') and 'webkit' in W5ENG:
                run_w5(br, 'webkit', dev)
            if want('W6') and 'webkit' in W6ENG:
                run_w6(br, 'webkit', dev)
        br.close()
        c5, c6 = want('W5') and 'chromium' in W5ENG, want('W6') and 'chromium' in W6ENG and not QC.SMOKE
        if c5 or c6:   # 같은 W5 · W6 코드를 Chromium(coarse · has_touch · is_mobile)으로 — 웹킷을 닫은 뒤(브라우저 하나씩)
            brc = pw.chromium.launch()
            ENV['chromium'] = brc.version
            for dev in DEVS:
                if c5:
                    run_w5(brc, 'chromium', dev)
                if c6:
                    run_w6(brc, 'chromium', dev)
            brc.close()
    bN = (not ERRS['BASE']) if 'BASE' in ERRS else None
    R('W0', '페이지 오류 0(칸마다 띄운 쪽 모두 · pageerror · error · unhandledrejection)', not ERRS['NEW'], bN,
      {k: (e or '0') for k, e in ERRS.items()}, yard=(bN is False))
    ENV['부팅(초 · 가운데 · 수)'] = [sorted(BOOTS)[len(BOOTS) // 2] if BOOTS else None, len(BOOTS)]
    ev = ENV.get('env') or {}
    if ev:   # 도구 환경 — Tailwind 가 안 실리면 W1 처음 100 · W5 줄 꼴이 거짓으로 갈린다(10/10 OL.route cdn 끊김 사고)
        R('W0', '도구 환경 — Tailwind 실림(검색 결과 통 max-h · overflow 가 섬)', bool(ev.get('tailwind')) and (ev.get('searchBoxCss') or {}).get('ovY') == 'auto', None,
          {'tailwind': ev.get('tailwind'), '검색 결과 통': ev.get('searchBoxCss'), 'tw': OL.CONF['tw']}, yard=False)
    R('WK', '환경(INFO)', None, None, ENV)
    nf = [r for r in RES if r['new'] is False]
    yd = [r for r in RES if r['yard'] and r['ybase'] is not None and r['new'] is not None]
    R('합계', '합계', None, None, {'PASS': sum(1 for r in RES if r['new'] is True), 'FAIL': len(nf), 'FAIL 칸': [r['g'] + ' ' + r['name'][:28] for r in nf],
                                  '헛잣대(헛잣대 열 FAIL · W5 ② iPad = %s)' % BASE2: '%d/%d' % (sum(1 for r in yd if r['ybase'] is False), len(yd)),
                                  '단계(분)': STEP, '전체(분)': round((time.time() - T0) / 60, 1)})
    try:
        os.makedirs(os.path.dirname(os.path.abspath(OUTF)), exist_ok=True)
        with open(OUTF, 'w', encoding='utf-8') as f:
            f.write('\n'.join(LINES) + '\n')
        with open(os.path.splitext(OUTF)[0] + '_detail.json', 'w', encoding='utf-8') as f:   # 줄에서 잘린 잰 값 전부(ID · 수 · 폭만)
            json.dump(RES, f, ensure_ascii=False, indent=1, default=str)
    except Exception:
        pass
    sys.exit(1 if nf else 0)


if __name__ == '__main__':
    main()
