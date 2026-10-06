# -*- coding: utf-8 -*-
r"""_task_ox_gg_phone §B 관문 — 민법OX 근거 칸(ggPanelHTML) 폰 머리줄 줄바꿈 · 고치기 줄 저장/취소 자리 · 탭 폭 2 · 문항 팝업 「정답·해설」 · 「🃏 N」

  python _harness_ox_gg_phone.py [--new <앱 파일 | genie 판>] [--base <판 = 65dd4db>] [--only G1,G2,..] [--tw <Tailwind CSS 사본>] [--res <결과 파일>] [--shots <그림 폴더>]

  NEW  = genie 작업트리 minbeop/index.html(고친 판) · BASE = 바탕 65dd4db(헛잣대 — 바뀐 칸은 바탕에서 FAIL 이어야 함) — 두 판을 같은 기기 · 같은 차례로 늘 같이 돌림
  틀 = _harness_gg_popup_rec.py 의 SEED(fetch 가짜 404 · localStorage 비움 · alert/confirm 막음) · window.onload 끔 · 합성 문항 · resetLS · openQuiz · btnIn 그대로 빌림
       (그 하네스는 본 PC 크롬 --dump-dom · 이 판은 기기 폭이 관문이라 Playwright Chromium 쪽으로 같은 틀을 띄운다)
  합성 기록(지어냄 · 쪽 안에서만) = 근거 한 줄(197번 꼴 — 긴 글 + 줄 앞 탭 「\t     」 · 「\t\t」 · 맞음) · 암기카드 1 장(ox_mem_cards · svg) · 연결(내가 1 · 나를 1)
  기기 = 폰 390×844(is_mobile · DPR 2) · PC 1280×900 · 누름 = 마우스(진짜 누름 · 터치 칸 아님)
  관문:
    G1 폰 머리줄 — 문항 팝업 근거 펼침: 글 span 폭 ≥ 머리줄 안쪽 폭 90% · 「맞음 · 날짜」 묶음 top ≥ 글 bottom − 1 · 묶음 right = 안쪽 right(±2) · 헛잣대 = 바탕 FAIL
    G2 PC 머리줄 — 같은 근거: 묶음 top = 글 첫 줄 top(±4 · 한 줄) · 무변 확인 칸(헛잣대 아님 · 바탕 값만)
    G3 고치기 줄 — 폰: 저장 · 취소 높이 ≤ 32 · top ≥ textarea bottom − 1 · 오른쪽 맞춤(±2) / PC: 높이 ≤ 32 · top = textarea top(±2) · 헛잣대 = 바탕 FAIL(저장 높이 = textarea 높이)
    G4 동작 무변 — 고치기 → 저장 · Enter 저장 · 취소 · 「!」 켜고 끄기 · 지우기(되묻기 창 → 지우기) — 칸 글 · 저장소(ox_q_geunge) = 바탕과 글자까지 같음(시계 · 난수 고정)
    G5 탭 폭 — .ggb-t · 고치기 textarea computed tab-size = 2 · 헛잣대 = 바탕 8
    G6 팝업 맨 아랫줄 — 「정답·해설」(펼쳐도 그대로 · 펼침/접힘 = 바탕) · 🃏 칩 「🃏 1」 · title 「암기카드」 · 누르면 암기카드 창(= 바탕) · 0 장 문항 「🃏」 ·
       「↩링크1」「↩백링크1」「Claude」「✏️ 연결」「↪ 이동」 글자 = 바탕 · 헛잣대 = 바탕 「정답·해설 보기」 · 「🃏 암기카드 1」
    G7 다른 자리 같은 꼴 — 카드 근거 줄에서 펼친 근거 칸(범위 없음)도 G1 · G3 같은 값(폰) · 헛잣대 = 바탕 FAIL
    G8 페이지 오류 0(pageerror · window error · unhandledrejection)
    G9 화면 훑기(규칙 60) — 폰 · PC × 팝업 근거 칸 · 카드 근거 칸 고치기 상태 그림 넷(--shots · _qa 밖) · 가로 넘침 0(scrollWidth ≤ clientWidth) · 단추 rect 화면 안
  엔진 = Chromium · 클라우드 = cdn 막힘 → --tw(민법 Tailwind v3 로 미리 구운 CSS) · 본 PC = cdn 그대로
  결과 = 화면 PASS/FAIL 줄 · --res(기본 = 임시 폴더 · _qa 에 결과를 쓰지 않는다)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, json, os, subprocess, sys, tempfile, threading, time, traceback, urllib.parse   # noqa: E402
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer   # noqa: E402
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from playwright.sync_api import sync_playwright   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


NEW = ARG('--new', _roots.genie('minbeop', 'index.html'))
BASE = ARG('--base', '65dd4db')   # genie main 65dd4db = 이 판의 바탕
ONLY = [x.strip().upper() for x in (ARG('--only', '') or '').split(',') if x.strip()]
TWCSS = ARG('--tw')
TMPD = os.path.join(tempfile.gettempdir(), 'h_ox_gg_phone')
OUTF = ARG('--res', os.path.join(TMPD, '_harness_ox_gg_phone_result.txt'))
SHOTS = ARG('--shots', os.path.join(TMPD, 'shots'))
REL = 'minbeop/index.html'
IPHONE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
DEV = {'폰390': dict(W=390, H=844, mob=True), 'PC1280': dict(W=1280, H=900, mob=False)}

RES = []    # (관문, 이름, 새 판 판정 True/False/None(INFO), 값)
YARD = []   # (관문, 이름, 바탕 판정) — 같은 잣대를 바탕 값에(헛잣대 칸만 · 다 FAIL 이어야 함)
ERRS = {}
STEP = []
T0 = time.time()


def _s(v):
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def T(g, name, ok, detail=''):
    RES.append((g, name, bool(ok), detail))
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', g, name, _s(detail)[:900]), flush=True)
    return bool(ok)


def N(g, name, detail=''):
    RES.append((g, name, None, detail))
    print('INFO | %s · %s | %s' % (g, name, _s(detail)[:900]), flush=True)


def TB(g, name, ok_fn, vn, vb, yard=True):
    """새 판 판정 · 같은 잣대로 바탕 판정(yard = 헛잣대 칸이면 YARD 에)"""
    try:
        okn = bool(ok_fn(vn))
    except Exception:
        okn = False
    T(g, name, okn, {'new': vn, 'base': vb})
    if vb is not None and yard:
        try:
            okb = bool(ok_fn(vb))
        except Exception:
            okb = False
        YARD.append((g, name, okb))
    return okn


def want(k):
    return not ONLY or k in ONLY


def git(*a):
    return subprocess.run(['git', '-C', _roots.genie(), '-c', 'core.quotepath=false'] + list(a), capture_output=True).stdout


def app_src(x):
    if os.path.isfile(x):
        return open(x, 'rb').read().decode('utf-8')
    b = git('show', x + ':' + REL)
    return b.decode('utf-8') if b else None


def md5lf(s):
    return hashlib.md5(s.replace('\r\n', '\n').encode('utf-8')).hexdigest()


# ════════════════════════ 틀 — _harness_gg_popup_rec.py 의 SEED 그대로(+ pageerror 는 Playwright 가 받는다) ════════════════════════
SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CERR=[];(function(){var ce=console.error.bind(console);console.error=function(){try{__CERR.push(Array.prototype.map.call(arguments,function(x){return typeof x==='string'?x:(x&&x.message)||JSON.stringify(x)}).join(' '))}catch(e){}return ce.apply(null,arguments);};})();
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};window.confirm=function(){return true;};window.prompt=function(){return null;};
window.fetch=function(){return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));};
localStorage.clear();
</script>"""

# 합성 근거 글 — 197번 꼴(줄 앞 탭 「\t     」 · 「\t\t」 · 긴 글) · 민법 제125조 글을 빌린 지어낸 근거
GT = ('\t     본인이 제3자에 대하여 타인에게 대리권을 수여함을 표시한 자는 그 대리권의 범위 내에서 행한 그 타인과 그 제3자 간의 법률행위에 대하여 책임이 있다.\n'
      '\t\t(다만 제3자가 대리권 없음을 알았거나 알 수 있었을 때에는 그러하지 아니하다.)\n'
      '\t     표시는 묵시적으로도 할 수 있다.')
UID, GK = 'Q9911', 'g_Q9911_a'
SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 40"><text x="4" y="24" font-size="14">카드</text></svg>'

TOOLS = r"""<script>
window.onload=null;   /* ★ 틀(gg_popup_rec) — 앱 시동(IndexedDB · 서버 받기)은 끄고 화면 함수를 직접 부른다 */
(function(){
const P=__P__;
const txt=e=>e?(e.textContent||'').replace(/\s+/g,' ').trim():'';
const BASEK={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const resetLS=o=>{ localStorage.clear(); for(const k in BASEK) localStorage.setItem(k,BASEK[k]); for(const k in (o||{})) localStorage.setItem(k,typeof o[k]==='string'?o[k]:JSON.stringify(o[k]));
  try{useIdxDrop()}catch(e){} try{mcInvalidate()}catch(e){} };
const loadQuiz=()=>{ quizData.length=0; P.quiz.forEach(q=>quizData.push(JSON.parse(JSON.stringify(q)))); };
const closeAllWins=()=>document.querySelectorAll('.oxwin').forEach(w=>w.remove());
const showHome=()=>{ const h=document.getElementById('home-screen'), q=document.getElementById('quiz-screen'); if(h) h.classList.remove('hide'); if(q) q.classList.add('hide'); };
const openQuiz=(ids,subject,chap)=>{
  loadQuiz();
  currentSubject=subject; currentChapterLabel=chap; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={}; currentSessionScore=0; lastGradeResults=null;
  currentFilteredData=ids.map(id=>quizData.find(q=>q.id===id));
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  renderQuizPage();
};
const btnIn=(root,text)=>root?[...root.querySelectorAll('button')].find(b=>b.textContent.trim()===text):null;
const R=e=>{ const r=e.getBoundingClientRect(); return {l:+r.left.toFixed(1),t:+r.top.toFixed(1),r:+r.right.toFixed(1),b:+r.bottom.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)}; };
const inner=e=>{ const r=e.getBoundingClientRect(), s=getComputedStyle(e);
  return {l:r.left+parseFloat(s.paddingLeft)+parseFloat(s.borderLeftWidth), r:r.right-parseFloat(s.paddingRight)-parseFloat(s.borderRightWidth)}; };
const hit=e=>{ if(!e) return null; try{ e.scrollIntoView({block:'center',inline:'nearest'}); }catch(x){} const r=e.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2, a=document.elementFromPoint(cx,cy);
  return {cx:+cx.toFixed(1),cy:+cy.toFixed(1),on:!!a&&(a===e||e.contains(a))&&cx>0&&cy>0&&cx<innerWidth&&cy<innerHeight,t:txt(e).slice(0,30)}; };
const pan=sc=>document.getElementById(sc+'gg-pan-'+P.uid+'-'+P.gk);
window.__GP={
  W:ms=>new Promise(r=>setTimeout(r,ms)),
  errs:()=>({err:(window.__ERR||[]).slice(),cerr:(window.__CERR||[]).slice(),alerts:(window.__ALERTS||[]).slice()}),
  /* 합성 기록 — 근거 한 줄(197번 꼴) · 암기카드 1 장 · 연결(내가 Q9912 · Q9913 이 나를) */
  prep(){ resetLS({ox_q_geunge:{[P.uid]:[{k:P.gk,i:1,t:P.gt,ok:true,ts:1789000000000,cs:[]}]},ox_mem_cards:{[P.uid]:[{k:'mc_h1',kind:'svg',svg:P.svg,ts:1789000000000}]},
      ox_q_links:{[P.uid]:['Q9912'],Q9913:[P.uid]}});
    loadQuiz(); closeAllWins(); showHome(); return {q:quizData.length,cards:mcCount(P.uid),cards2:mcCount('Q9912'),gg:(ggOf(P.uid)||[]).length}; },
  popup(id){ closeAllWins(); showHome(); openQPopup(id||P.uid); return !!document.getElementById('oxwin-q-'+(id||P.uid)); },
  card(){ closeAllWins(); openQuiz([P.uid,'Q9912'],'민법총칙',P.ch); return !!document.getElementById('gg-chip-'+P.uid+'-'+P.gk); },
  chipAt(sc){ return hit(document.getElementById(sc+'gg-chip-'+P.uid+'-'+P.gk)); },
  btnAt(sc,where,text){ const p=pan(sc); if(!p) return null; const root=where==='edit'?document.getElementById(sc+'gg-edit-'+P.uid+'-'+P.gk):p.firstElementChild; return hit(btnIn(root,text)); },
  bangAt(sc){ const p=pan(sc); return p?hit(p.querySelector('.ggbang')):null; },
  /* 머리줄 — 글 span · 「맞음 · 날짜」 묶음(새 판 = ml-auto span · 바탕 = 날짜 span 자체) · 지우기 단추 */
  head(sc){ const p=pan(sc); if(!p||p.classList.contains('hide')) return {err:'접힘'}; const row=p.firstElementChild, t=document.getElementById(sc+'gg-t-'+P.uid+'-'+P.gk);
    const date=[...row.querySelectorAll('span')].find(s=>!s.children.length&&/^(맞음|틀림|안 품) · \d+\/\d+$/.test(txt(s)));
    const grp=date&&date.parentElement!==row?date.parentElement:date, del=btnIn(row,'지우기'), I=inner(row), tr=R(t), gr=R(grp), dr=R(del);
    return {inW:+(I.r-I.l).toFixed(1),tW:tr.w,ratio:+(tr.w/(I.r-I.l)).toFixed(3),tTop:tr.t,tBot:tr.b,gTop:gr.t,gRight:+Math.max(gr.r,dr.r).toFixed(1),inR:+I.r.toFixed(1),
      lines:Math.round(tr.h/parseFloat(getComputedStyle(t).lineHeight||'18')),date:txt(date),grpIsSpan:grp!==date}; },
  /* 고치기 줄 — textarea · 저장 · 취소 */
  edit(sc){ const row=document.getElementById(sc+'gg-edit-'+P.uid+'-'+P.gk); if(!row||row.classList.contains('hide')) return {err:'닫힘'};
    const ta=document.getElementById(sc+'gg-ein-'+P.uid+'-'+P.gk), sv=btnIn(row,'저장'), cc=btnIn(row,'취소'), I=inner(row), a=R(ta), s=R(sv), c=R(cc);
    return {taTop:a.t,taBot:a.b,taH:a.h,svH:s.h,ccH:c.h,svTop:s.t,ccTop:c.t,ccRight:c.r,inR:+I.r.toFixed(1)}; },
  tab(sc){ const t=document.getElementById(sc+'gg-t-'+P.uid+'-'+P.gk), ta=document.getElementById(sc+'gg-ein-'+P.uid+'-'+P.gk);
    return {span:t?getComputedStyle(t).tabSize:null,ta:ta?getComputedStyle(ta).tabSize:null,taShown:!!ta&&!!ta.getClientRects().length}; },
  /* G4 — 같은 조작(시계 · 난수 고정) · 칸 글과 저장소 글자 */
  fix(){ window.__clk=1789000100000; window.__seed=12345; window.__realNow=window.__realNow||Date.now; window.__realRnd=window.__realRnd||Math.random;
    Date.now=()=>(window.__clk+=1000); Math.random=()=>{ window.__seed=(window.__seed*16807)%2147483647; return (window.__seed-1)/2147483646; }; return true; },
  unfix(){ if(window.__realNow) Date.now=window.__realNow; if(window.__realRnd) Math.random=window.__realRnd; return true; },
  setEin(sc,v){ const ta=document.getElementById(sc+'gg-ein-'+P.uid+'-'+P.gk); if(!ta) return false; ta.focus(); ta.value=v; ta.dispatchEvent(new Event('input',{bubbles:true})); return true; },
  enter(sc){ const ta=document.getElementById(sc+'gg-ein-'+P.uid+'-'+P.gk); if(!ta) return false; ta.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',bubbles:true,cancelable:true})); return true; },
  state(sc){ const p=pan(sc), e=document.getElementById(sc+'gg-edit-'+P.uid+'-'+P.gk), t=document.getElementById(sc+'gg-t-'+P.uid+'-'+P.gk);
    return {span:t?t.textContent:null,editOpen:!!e&&!e.classList.contains('hide'),panOpen:!!p&&!p.classList.contains('hide'),on:!!p&&p.classList.contains('gg-on'),store:localStorage.getItem('ox_q_geunge'),
      delWin:!!document.querySelector('[id^="oxwin-ggdel-"]')}; },
  delGoAt(){ return hit(document.getElementById('ggdel-go-'+P.uid)); },
  /* G6 — 팝업 맨 아랫줄 */
  bottom(id){ const w=document.getElementById('oxwin-q-'+id); if(!w) return null; const go=w.querySelector('button.qpgo'), row=go&&go.parentElement;
    const bs=row?[...row.querySelectorAll('button')]:[], mc=bs.find(b=>/openMemCard/.test(b.getAttribute('onclick')||'')), ans=bs.find(b=>/qPopToggleAns/.test(b.getAttribute('onclick')||''));
    const a=document.getElementById('qpop-ans-'+id);
    return {texts:bs.map(txt),mc:mc?txt(mc):null,mcTitle:mc?(mc.getAttribute('title')||''):null,ans:ans?txt(ans):null,ansOpen:a?a.style.display:null}; },
  ansAt(id){ const w=document.getElementById('oxwin-q-'+id); const b=w&&[...w.querySelectorAll('button')].find(x=>/qPopToggleAns/.test(x.getAttribute('onclick')||'')); return hit(b); },
  mcAt(id){ const w=document.getElementById('oxwin-q-'+id); const b=w&&[...w.querySelectorAll('button')].find(x=>/openMemCard/.test(x.getAttribute('onclick')||'')); return hit(b); },
  mcWin(id){ return !!document.getElementById('oxwin-mc-'+id); },
  /* G9 — 넘침 · 단추 화면 안 */
  over(sc){ const p=pan(sc); if(!p) return null; const host=p.closest('.oxwin')||p.closest('.question-box')||p.parentElement;
    const els=[p,p.firstElementChild,document.getElementById(sc+'gg-edit-'+P.uid+'-'+P.gk)].filter(e=>e&&e.getClientRects().length);
    const ov=els.map(e=>e.scrollWidth-e.clientWidth), bs=[...p.querySelectorAll('button,.ggbang')].filter(e=>e.getClientRects().length).map(e=>({t:txt(e),r:R(e)}));
    const out=bs.filter(b=>b.r.l<-0.5||b.r.r>innerWidth+0.5||b.r.t<-0.5||b.r.b>innerHeight+0.5).map(b=>b.t);
    return {over:Math.max(...ov),hostOver:host?host.scrollWidth-host.clientWidth:null,docOver:document.documentElement.scrollWidth-innerWidth,btns:bs.length,offscreen:out}; },
  scrollTo(sc){ const p=pan(sc); if(p) try{ p.scrollIntoView({block:'center'}); }catch(e){} return !!p; }
};
})();
</script>"""


def quiz():
    """합성 문항 — _harness_gg_popup_rec 의 문항 꼴 그대로(값 지어냄)"""
    base = {'a': 'O', 'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'pending': False,
            'examMeta': [], 'caseText': '', 'stem': '', 'status': '', 'excelLogic': ''}
    out = []
    for i, u in enumerate((UID, 'Q9912', 'Q9913')):
        q = dict(base, id=u, q='더미 지문 ' + u + ' — 본인이 대리권 수여를 표시한 경우의 책임 가나다라마바사', exp='더미 해설 ' + u, displayNo=197 + i, probNum=197 + i,
                 source='변리사 20')
        out.append(q)
    return out


def inject(src):
    src = src.replace('\r\n', '\n')
    TW = '<script src="https://cdn.tailwindcss.com"></script>'
    if TWCSS and TW in src:
        src = src.replace(TW, '<style>/* harness: Tailwind v3 사본(--tw) */\n' + open(TWCSS, encoding='utf-8').read() + '\n</style>', 1)
    P = {'quiz': quiz(), 'uid': UID, 'gk': GK, 'gt': GT, 'svg': SVG, 'ch': '1. 총칙 > 1.1 민법의 법원'}
    tools = TOOLS.replace('__P__', json.dumps(P, ensure_ascii=False).replace('</', '<\\/'))
    b = src.index('<body')
    bb = src.index('>', b) + 1
    html = src[:bb] + SEED + src[bb:]
    e = html.rindex('</body>')   # ⚠ index.html 은 </body> 가 둘이다 — rindex(틀 그대로)
    return html[:e] + tools + html[e:]


SERVERS = {}


def serve(tag, src):
    if tag in SERVERS:
        return SERVERS[tag][1]
    body = inject(src).encode('utf-8')

    class Hd(SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
            data, code, ct = (body, 200, 'text/html; charset=utf-8') if p in ('/minbeop/', '/minbeop/index.html') else (b'{"message":"Not Found"}', 404, 'application/json')
            self.send_response(code)
            self.send_header('Content-Type', ct)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

    srv = ThreadingHTTPServer(('127.0.0.1', 0), Hd)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    SERVERS[tag] = (srv, srv.server_address[1])
    return srv.server_address[1]


class Pg:
    def __init__(self, br, tag, src, dev):
        self.tag, self.dev = tag, dev
        d = DEV[dev]
        kw = dict(viewport={'width': d['W'], 'height': d['H']})
        if d['mob']:
            kw.update(device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=IPHONE_UA)
        self.ctx = br.new_context(**kw)
        self.ctx.route('**/*', lambda r: r.continue_() if (r.request.url.startswith('http://127.0.0.1') or (r.request.url.startswith('https://cdn.tailwindcss.com') and not TWCSS)) else r.abort())
        self.pg = self.ctx.new_page()
        self.pg.set_default_timeout(120000)
        self.errs = []
        self.pg.on('pageerror', lambda e: self.errs.append('page: ' + str(e)[:300]))
        port = serve(tag, src)
        self.pg.goto('http://127.0.0.1:%d/minbeop/index.html' % port, wait_until='load', timeout=120000)
        self.pg.wait_for_function("() => !!window.__GP && typeof openQPopup === 'function' && typeof quizData !== 'undefined'", timeout=120000)
        self.pg.wait_for_timeout(300)

    def ev(self, expr, arg=None):
        return self.pg.evaluate(expr, arg) if arg is not None else self.pg.evaluate(expr)

    def click(self, at, wait=350):
        if not at or not at.get('on'):
            return False
        self.pg.mouse.click(at['cx'], at['cy'])
        self.pg.wait_for_timeout(wait)
        return True

    def shot(self, name):
        try:
            os.makedirs(SHOTS, exist_ok=True)
            f = os.path.join(SHOTS, 'ox_gg_phone_%s_%s_%s.png' % (self.tag, self.dev, name))
            self.pg.screenshot(path=f)
            return f
        except Exception as e:
            return 'shot err ' + str(e)[:80]

    def close(self):
        try:
            e = self.ev("() => __GP.errs()")
            ERRS.setdefault('%s %s' % (self.tag, self.dev), []).extend(self.errs + e['err'])
        except Exception:
            ERRS.setdefault('%s %s' % (self.tag, self.dev), []).extend(self.errs)
        try:
            self.ctx.close()
        except Exception:
            pass


# ════════════════════════ 한 기기 한 판 — 재기(같은 차례) ════════════════════════
def open_panel(p, sc):
    """sc = 'qp-'(문항 팝업) · ''(카드) — 근거 칩을 진짜로 눌러 칸을 편다"""
    p.ev("() => __GP.prep()")
    ok = p.ev("() => __GP.popup()") if sc == 'qp-' else p.ev("() => __GP.card()")
    p.click(p.ev("(s) => __GP.chipAt(s)", sc), 300)
    return ok


def run_one(br, tag, src, dev):
    p = Pg(br, tag, src, dev)
    out = {}
    try:
        for sc, nm in (('qp-', '팝업'), ('', '카드')):
            open_panel(p, sc)
            out[nm] = {'head': p.ev("(s) => __GP.head(s)", sc), 'tab0': p.ev("(s) => __GP.tab(s)", sc)}
            p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'head', '고치기']), 400)
            out[nm]['edit'] = p.ev("(s) => __GP.edit(s)", sc)
            out[nm]['tab'] = p.ev("(s) => __GP.tab(s)", sc)
            out[nm]['over'] = p.ev("(s) => __GP.over(s)", sc)
            if tag == 'NEW':
                p.ev("(s) => __GP.scrollTo(s)", sc)
                if nm == '카드':
                    out[nm]['shot'] = p.shot('card_edit')
                else:
                    p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'edit', '취소']), 300)
                    p.ev("(s) => __GP.scrollTo(s)", sc)
                    out[nm]['shot'] = p.shot('popup')
                    out[nm]['over_closed'] = p.ev("(s) => __GP.over(s)", sc)
        # G4 — 동작(팝업 · 시계 · 난수 고정)
        g4 = []
        open_panel(p, 'qp-')
        p.ev("() => __GP.fix()")
        sc = 'qp-'
        p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'head', '고치기']))
        p.ev("([s, v]) => __GP.setEin(s, v)", [sc, '고친 글 하나 — 저장 단추'])
        p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'edit', '저장']))
        g4.append(['저장', p.ev("(s) => __GP.state(s)", sc)])
        p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'head', '고치기']))
        p.ev("([s, v]) => __GP.setEin(s, v)", [sc, '고친 글 둘 — Enter'])
        p.ev("(s) => __GP.enter(s)", sc)
        p.pg.wait_for_timeout(300)
        g4.append(['Enter', p.ev("(s) => __GP.state(s)", sc)])
        p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'head', '고치기']))
        p.ev("([s, v]) => __GP.setEin(s, v)", [sc, '취소할 글'])
        p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'edit', '취소']))
        g4.append(['취소', p.ev("(s) => __GP.state(s)", sc)])
        p.click(p.ev("(s) => __GP.bangAt(s)", sc))
        g4.append(['! 켬', p.ev("(s) => __GP.state(s)", sc)])
        p.click(p.ev("(s) => __GP.bangAt(s)", sc))
        g4.append(['! 끔', p.ev("(s) => __GP.state(s)", sc)])
        p.click(p.ev("([s, w, t]) => __GP.btnAt(s, w, t)", [sc, 'head', '지우기']))
        g4.append(['지우기 → 되묻기 창', p.ev("(s) => __GP.state(s)", sc)])
        p.click(p.ev("() => __GP.delGoAt()"))
        g4.append(['되묻기 창 지우기', p.ev("(s) => __GP.state(s)", sc)])
        p.ev("() => __GP.unfix()")
        out['G4'] = g4
        # G6 — 팝업 맨 아랫줄
        p.ev("() => __GP.prep()")
        p.ev("() => __GP.popup()")
        b0 = p.ev("(i) => __GP.bottom(i)", UID)
        p.click(p.ev("(i) => __GP.ansAt(i)", UID))
        b1 = p.ev("(i) => __GP.bottom(i)", UID)
        p.click(p.ev("(i) => __GP.ansAt(i)", UID))
        b2 = p.ev("(i) => __GP.bottom(i)", UID)
        p.click(p.ev("(i) => __GP.mcAt(i)", UID), 500)
        mcw = p.ev("(i) => __GP.mcWin(i)", UID)
        p.ev("() => __GP.popup('Q9912')")
        z = p.ev("(i) => __GP.bottom(i)", 'Q9912')
        out['G6'] = {'처음': b0, '한 번 누름': b1, '두 번 누름': b2, '암기카드 창': mcw, '0 장 문항': z}
    except Exception:
        out['err'] = traceback.format_exc()[-1500:]
    p.close()
    return out


# ════════════════════════ 판정 ════════════════════════
def g1_ok(h):
    return bool(h) and not h.get('err') and h['ratio'] >= 0.9 and h['gTop'] >= h['tBot'] - 1 and abs(h['gRight'] - h['inR']) <= 2


def g2_ok(h):
    return bool(h) and not h.get('err') and abs(h['gTop'] - h['tTop']) <= 4


def g3_phone(e):
    return bool(e) and not e.get('err') and e['svH'] <= 32 and e['ccH'] <= 32 and e['svTop'] >= e['taBot'] - 1 and abs(e['ccRight'] - e['inR']) <= 2


def g3_pc(e):
    return bool(e) and not e.get('err') and e['svH'] <= 32 and e['ccH'] <= 32 and abs(e['svTop'] - e['taTop']) <= 2


def tab_ok(t):
    return bool(t) and t.get('span') == '2' and t.get('ta') == '2'


def bottom_ok(x):
    g = x['G6']
    return (g['처음']['ans'] == '정답·해설' and g['한 번 누름']['ans'] == '정답·해설' and g['두 번 누름']['ans'] == '정답·해설'
            and g['처음']['mc'] == '🃏 1' and g['처음']['mcTitle'] == '암기카드' and g['0 장 문항']['mc'] == '🃏' and g['암기카드 창'])


def main():
    os.makedirs(TMPD, exist_ok=True)
    sn, sb = app_src(NEW), app_src(BASE)
    print('INFO | 새 판 md5(LF) %s · %s B · 바탕 %s md5(LF) %s · %s B' % (md5lf(sn), len(sn.encode('utf-8')), BASE, sb and md5lf(sb), sb and len(sb.encode('utf-8'))), flush=True)
    R = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for dev in DEV:
            for tag, src in (('NEW', sn), ('BASE', sb)):
                if src is None:
                    continue
                t1 = time.time()
                R[(tag, dev)] = run_one(br, tag, src, dev)
                STEP.append(('%s %s' % (tag, dev), round(time.time() - t1)))
        br.close()
    for k, v in R.items():
        if v.get('err'):
            T('G0', '%s %s 하네스 실행' % k, False, v['err'])
    nP, bP = R.get(('NEW', '폰390'), {}), R.get(('BASE', '폰390'))
    nC, bC = R.get(('NEW', 'PC1280'), {}), R.get(('BASE', 'PC1280'))
    g = lambda d, nm, k: ((d or {}).get(nm) or {}).get(k)
    if want('G1'):
        TB('G1', '폰 390 문항 팝업 근거 머리줄 — 글 폭 ≥ 안쪽 폭 90% · 「맞음 · 날짜」 묶음 아랫줄(top ≥ 글 bottom − 1) · 묶음 오른쪽 맞춤(±2)', g1_ok, g(nP, '팝업', 'head'), g(bP, '팝업', 'head'))
    if want('G2'):
        TB('G2', 'PC 1280 문항 팝업 근거 머리줄 — 묶음 top = 글 첫 줄 top(±4 · 한 줄 · 무변 확인 칸)', g2_ok, g(nC, '팝업', 'head'), g(bC, '팝업', 'head'), yard=False)
    if want('G3'):
        TB('G3', '폰 390 팝업 고치기 줄 — 저장 · 취소 높이 ≤ 32 · 아랫줄(top ≥ textarea bottom − 1) · 오른쪽 맞춤', g3_phone, g(nP, '팝업', 'edit'), g(bP, '팝업', 'edit'))
        TB('G3', 'PC 1280 팝업 고치기 줄 — 저장 · 취소 높이 ≤ 32 · textarea 와 같은 줄(top ±2)', g3_pc, g(nC, '팝업', 'edit'), g(bC, '팝업', 'edit'))
    if want('G4'):
        for dev, n, b in (('폰390', nP, bP), ('PC1280', nC, bC)):
            a, c = (n or {}).get('G4'), (b or {}).get('G4')
            steps = [s[0] for s in (a or [])]
            same = bool(a) and bool(c) and json.dumps(a, ensure_ascii=False) == json.dumps(c, ensure_ascii=False)
            last = (a or [[None, {}]])[-1][1] if a else {}
            T('G4', '%s 근거 칸 동작 무변 — %s · 칸 글 · 저장소 글자 = 바탕' % (dev, ' → '.join(steps)), same and len(steps) == 7 and a[0][1]['span'] == '고친 글 하나 — 저장 단추'
              and a[1][1]['span'] == '고친 글 둘 — Enter' and not a[2][1]['editOpen'] and a[3][1]['on'] and not a[4][1]['on'] and a[5][1]['delWin'] and json.loads(last.get('store') or '{}').get(UID) in (None, []),
              {'새 판': [[s[0], {k: v for k, v in s[1].items() if k != 'store'}] for s in (a or [])], '저장소 끝': last.get('store'), '바탕과 같음': same})
    if want('G5'):
        TB('G5', '폰 390 팝업 · 카드 — .ggb-t · 고치기 textarea tab-size = 2', lambda x: tab_ok(x[0]) and tab_ok(x[1]),
           [g(nP, '팝업', 'tab'), g(nP, '카드', 'tab')], bP and [g(bP, '팝업', 'tab'), g(bP, '카드', 'tab')])
        TB('G5', 'PC 1280 팝업 · 카드 — tab-size = 2', lambda x: tab_ok(x[0]) and tab_ok(x[1]), [g(nC, '팝업', 'tab'), g(nC, '카드', 'tab')], bC and [g(bC, '팝업', 'tab'), g(bC, '카드', 'tab')])
    if want('G6'):
        for dev, n, b in (('폰390', nP, bP), ('PC1280', nC, bC)):
            TB('G6', '%s 팝업 맨 아랫줄 — 「정답·해설」(펼쳐도 그대로) · 「🃏 1」 title 암기카드 · 누르면 암기카드 창 · 0 장 문항 「🃏」' % dev, bottom_ok,
               n if n.get('G6') else None, b if (b and b.get('G6')) else None)
            if n.get('G6') and b and b.get('G6'):
                gn, gb = n['G6'], b['G6']
                keep = lambda L: [t for t in L if t not in ('정답·해설', '정답·해설 보기', '정답·해설 숨기기') and not t.startswith('🃏')]
                T('G6', '%s 정답·해설 펼침/접힘 = 바탕 · 다른 단추 글자(↩링크 · ↩백링크 · Claude · ✏️ 연결 · ↪ 이동) = 바탕 · 암기카드 창 = 바탕' % dev,
                  [gn['처음']['ansOpen'], gn['한 번 누름']['ansOpen'], gn['두 번 누름']['ansOpen']] == [gb['처음']['ansOpen'], gb['한 번 누름']['ansOpen'], gb['두 번 누름']['ansOpen']] == ['none', 'block', 'none']
                  and keep(gn['처음']['texts']) == keep(gb['처음']['texts']) and keep(gn['0 장 문항']['texts']) == keep(gb['0 장 문항']['texts']) and gn['암기카드 창'] == gb['암기카드 창'] is True
                  and '↩링크1' in gn['처음']['texts'] and '↩백링크1' in gn['처음']['texts'],
                  {'새 판 단추': gn['처음']['texts'], '바탕 단추': gb['처음']['texts'], '펼침 새/바탕': [[gn[k]['ansOpen'] for k in ('처음', '한 번 누름', '두 번 누름')], [gb[k]['ansOpen'] for k in ('처음', '한 번 누름', '두 번 누름')]],
                   '0 장 문항 새/바탕': [gn['0 장 문항']['mc'], gb['0 장 문항']['mc']]})
    if want('G7'):
        TB('G7', '폰 390 카드 근거 칸(범위 없음) 머리줄 = G1 값', g1_ok, g(nP, '카드', 'head'), g(bP, '카드', 'head'))
        TB('G7', '폰 390 카드 고치기 줄 = G3 값', g3_phone, g(nP, '카드', 'edit'), g(bP, '카드', 'edit'))
        TB('G7', 'PC 1280 카드 근거 칸 머리줄 = G2 값 · 고치기 줄 = G3 PC 값', lambda x: g2_ok(x[0]) and g3_pc(x[1]), [g(nC, '카드', 'head'), g(nC, '카드', 'edit')],
           bC and [g(bC, '카드', 'head'), g(bC, '카드', 'edit')], yard=False)
    if want('G9'):
        for dev, n in (('폰390', nP), ('PC1280', nC)):
            for nm in ('팝업', '카드'):
                o = g(n, nm, 'over')
                oc = g(n, nm, 'over_closed')
                T('G9', '%s %s 근거 칸(고치기 열림%s) — 가로 넘침 0 · 단추 rect 화면 안 · 그림 %s' % (dev, nm, ' · 닫힘' if oc else '', os.path.basename(g(n, nm, 'shot') or '')),
                  bool(o) and o['over'] <= 0 and (o['hostOver'] or 0) <= 0 and o['docOver'] <= 0 and not o['offscreen'] and (not oc or (oc['over'] <= 0 and not oc['offscreen'])),
                  {'고치기 열림': o, '닫힘': oc})
    base_msgs = {m for k, v in ERRS.items() if k.startswith('BASE') for m in v}
    for k, v in ERRS.items():
        if k.startswith('NEW'):
            own = [m for m in v if m not in base_msgs]
            T('G8', '%s 페이지 오류 0(pageerror · window error · unhandledrejection · 바탕에도 나는 것 %d)' % (k, len(v) - len(own)), not own, own[:5])
        else:
            N('G8', '%s 페이지 오류' % k, v[:5])
    n_pass = sum(1 for r in RES if r[2] is True)
    n_fail = sum(1 for r in RES if r[2] is False)
    y_bad = [y for y in YARD if y[2]]
    lines = ['', '=' * 100, '_harness_ox_gg_phone — PASS %d · FAIL %d · %d초' % (n_pass, n_fail, round(time.time() - T0)),
             '헛잣대(바탕 %s · 같은 차례 · FAIL 이어야 함): %d 칸 중 바탕이 통과한 칸 %d' % (BASE, len(YARD), len(y_bad))]
    lines += ['  바탕 통과(헛잣대 실패): %s · %s' % (gg, nm) for gg, nm, _ in y_bad]
    lines += ['단계별 초: ' + ' · '.join('%s %d' % s for s in STEP)]
    lines += ['FAIL: %s · %s' % (r[0], r[1]) for r in RES if r[2] is False]
    print('\n'.join(lines), flush=True)
    os.makedirs(os.path.dirname(OUTF), exist_ok=True)
    with open(OUTF, 'w', encoding='utf-8') as f:
        for gg, nm, ok, d in RES:
            f.write('%s | %s · %s | %s\n' % ('INFO' if ok is None else ('PASS' if ok else 'FAIL'), gg, nm, _s(d)))
        f.write('\n'.join(lines) + '\n')
    print('결과 파일: %s · 그림: %s' % (OUTF, SHOTS), flush=True)
    return 0 if not n_fail and not y_bad else 1


if __name__ == '__main__':
    sys.exit(main())
