# -*- coding: utf-8 -*-
"""민법OX 근거 목록 → 문항 팝업 · 팝업 안 근거 줄(범위 qp-) · 출처 칩 풀이 기록 두 줄 검산 (minbeop/task/_task_ox_gg_popup_rec.md §E).

  판 NEW  = genie 작업트리 minbeop/index.html
     HEAD = git HEAD (고치기 전 · 헛잣대)
⚠ 앱 onload(IndexedDB 시동)는 끈다 — 검사가 화면 함수를 직접 부른다(가상 시계와 경합하지 않게).
⚠ fetch 는 통째로 가짜다(진짜 망에 안 나간다) · 토큰을 안 넣어 기록 동기화는 돌지 않는다.
⚠ index.html 은 </body> 가 둘이다 — rindex 로 붙이고 결과는 documentElement 에 붙인다.
⚠ G3 은 두 판에서 **같은 조작**을 하고 저장소 글자를 파이썬이 대조한다(Date.now·Math.random 을 그 구간만 고정).

쓰기 : python _harness_gg_popup_rec.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
REL = 'minbeop/index.html'
OUT = os.path.join(tempfile.gettempdir(), 'h_gg_popup_rec')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11']


def git(*a):
    r = subprocess.run(['git', '-C', GENIE, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def _rg_md5(v):
    """qa_slim2 regress — 기준 칸 값 줄이기(글 · 줄 묶음 → md5) · gate 에서 안 쓴다"""
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def build_and_run(tag, src, tests, budget=90000):
    html = src
    b = html.index('<body')
    bb = html.index('>', b) + 1
    html = html[:bb] + SEED + html[bb:]
    e = html.rindex('</body>')
    html = html[:e] + tests + html[e:]
    app = os.path.join(OUT, 'app_%s.html' % tag)
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    # ⚠ 채점(gradeCurrentPage) 흐름을 돌린 페이지는 시험이 다 끝난 **뒤** 헤드리스 크롬이 죽는다(rc 0xC000001D) —
    #   고치기 전 판(HEAD)에서도 채점만 돌리면 똑같다(2026-09-15 실측). 그래서 결과를 DOM 덤프가 아니라
    #   콘솔 로그(stderr)로 받는다: 시험 끝에 줄마다 console.log('HZR|'+encodeURIComponent(줄)).
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                        '--user-data-dir=' + prof, '--allow-file-access-from-files', '--window-size=1280,900',
                        '--enable-logging=stderr', '--v=0',
                        '--virtual-time-budget=%d' % budget, '--dump-dom', 'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=600)
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'chrome_err_%s.txt' % tag), 'w', encoding='utf-8').write(err)
    hz = []
    for ln in err.split('\n'):
        i = ln.find('"HZR|')
        if i >= 0:
            j = ln.find('"', i + 5)
            hz.append(urllib.parse.unquote(ln[i + 5:j]))
    if os.environ.get('HZ_LOG'):
        print('  [%s] chrome rc %s · HZR 줄 %d' % (tag, r.returncode, len(hz)))
    if hz and hz[-1] == 'END':
        return [x for x in hz[:-1] if x.strip()]
    dom = r.stdout.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'dom_%s.html' % tag), 'w', encoding='utf-8').write(dom)
    m = re.search(r'<pre id="hz-out">(.*?)</pre>', dom, re.S)
    if not m:
        return None
    txt = m.group(1).replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')
    return [ln for ln in txt.split('\n') if ln.strip()]


def gate_of(line):
    try:
        return line.split(' | ')[1].split(' ')[0]
    except Exception:
        return ''


def tally(lines, g):
    ls_ = [x for x in (lines or []) if x.startswith(('PASS', 'FAIL')) and gate_of(x) == g]
    if not ls_:
        return '—'
    p = sum(1 for x in ls_ if x.startswith('PASS'))
    return '%dP/%dF' % (p, len(ls_) - p)


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(os.path.join(GENIE, REL.replace('/', os.sep)), encoding='utf-8', newline='').read()
    if QC.GATE:
        QC.sub('git:show-app')
    head = git('show', 'HEAD:' + REL) if QC.GATE else None   # regress · smoke — 바탕(HEAD) 판을 안 푼다(헛잣대 · 사슬에선 HEAD = 새 판)
    quiz = []
    base = {'a': 'O', 'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'subNum': '', 'pending': False,
            'examMeta': [], 'caseText': '', 'stem': '', 'status': '', 'excelLogic': ''}
    for i, (u, src, extra) in enumerate([('Q9901', '변리사 20', {}), ('Q9902', '', {}), ('Q9903', '변리사 21', {'excelLogic': '논리 글 하나'}),
                                         ('Q9904', '변리사 22', {'subChapter': '1.2 신의칙'})]):
        q = dict(base, id=u, q='더미 지문 ' + u + ' 가나다라마바사', exp='더미 해설 ' + u, displayNo=i + 1, probNum=i + 1, source=src)
        q.update(extra)
        quiz.append(q)
    quiz.append(dict(base, id='Q9905', q='기출 지문 Q9905', exp='기출 해설', displayNo=5, probNum=5, source='변리사 16',
                     examYear='2016', examRound='53', examYears=['2016'], examMeta=[{'year': '2016', 'round': '53', 'no': 1, 'opt': 1}],
                     examNo=1, examOpt=1, examNoBase=1, examOptBase=1, stem='다음 설명 중 옳은 것은?'))
    P = {'quiz': quiz, 'skip': [x for x in os.environ.get('HZ_SKIP', '').split(',') if x], 'gradeOnly': bool(os.environ.get('HZ_GRADEONLY'))}
    if QC.SMOKE:   # smoke(A-4) — G1(근거 목록 → 문항 팝업) 갈래만 + 끝의 「G11 페이지 오류 0」(갈래 밖 · 늘 찍힘) — 나머지 갈래는 건넘(진단용 거름 P.skip 을 그대로 씀)
        P['skip'] = sorted(set(P['skip']) | {'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G11'})
    tests = TESTS.replace('__P__', json.dumps(P, ensure_ascii=False).replace('</', '<\\/'))
    res = {}
    only = os.environ.get('HZ_ONLY')
    for tag, src in ((('NEW', new), ('HEAD', head)) if QC.GATE else (('NEW', new),)):   # regress · smoke — 새 판만
        if only and tag != only:
            continue
        QC.launch('new' if tag == 'NEW' else 'base')
        lines = build_and_run(tag, src, tests)
        res[tag] = lines
        print('=== %s 판 ===' % tag)
        if lines is None:
            print('  결과 줄 없음 → %s' % os.path.join(OUT, 'dom_%s.html' % tag))
            continue
        for ln in lines:
            print('   ' + (ln if len(ln) < 700 else ln[:700] + ' …'))
        print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
        print()

    # G3 — 같은 조작 → 같은 저장소·같은 카드 글자 (NEW vs HEAD)
    def vals(lines, pfx):
        return [x for x in (lines or []) if x.startswith('VAL | ' + pfx)]
    if QC.SMOKE:   # smoke — G3(같은 조작 글자 대조) · G10(소스)는 smoke 칸 아님(건넘)
        g3_ok = g10 = True
    elif QC.GATE:
        g3n, g3h = vals(res.get('NEW'), 'G3.'), vals(res.get('HEAD'), 'G3.')
        print('=== G3 회귀 — 카드 쪽 같은 조작의 저장소·카드 글자 (NEW vs HEAD) ===')
        g3 = []
        for a, b in zip(g3n, g3h):
            name = a.split(' | ')[1]
            ok = a == b
            g3.append(ok)
            print('  %-34s %s' % (name, 'PASS 글자까지 같다' if ok else 'FAIL 다르다'))
        g3_ok = bool(g3) and all(g3) and len(g3n) == len(g3h)
        print('  G3 : %s (%d/%d 걸음)' % ('PASS' if g3_ok else 'FAIL', sum(g3), max(len(g3n), len(g3h))))
        print()
    else:   # regress — 바탕(HEAD) 판을 안 띄운다: 같은 조작(시계 · 난수 고정)의 글자를 기준 스냅샷(앞 인도판 새 판 글자 md5 · 걸음 수)과 맞댄다
        g3n = vals(res.get('NEW'), 'G3.')
        print('=== G3 회귀 — 카드 쪽 같은 조작의 저장소·카드 글자 (NEW vs 기준 스냅샷) ===')
        g3 = []
        for a in g3n:
            name = a.split(' | ')[1]
            ok = QC.same('G3/' + name, _rg_md5(a))
            g3.append(ok)
            print('  %-34s %s' % (name, 'PASS 글자까지 같다' if ok else 'FAIL 다르다'))
        g3_ok = bool(g3) and all(g3) and len(g3n) == QC.base('G3/n', len(g3n))
        print('  G3 : %s (%d/%d 걸음 · %s)' % ('PASS' if g3_ok else 'FAIL', sum(g3), len(g3n), QC.base_note('G3/n')))
        print()

    if not QC.SMOKE:
        # G10 — 소스
        print('=== G10 소스 (NEW vs HEAD) ===')
        if QC.GATE:
            Ln, Lh = new.split('\n'), head.split('\n')
            pb = [s for s in Ln if 'pastBadgeHtml' in s] == [s for s in Lh if 'pastBadgeHtml' in s] and new.count("const pastBadgeHtml = '';") == 1
            lg = [s for s in Ln if len(s) > 3000] == [s for s in Lh if len(s) > 3000]
            l929 = len(Ln) > 928 and len(Lh) > 928 and Ln[928] == Lh[928] and len(Ln[928]) > 60000
            sk = [s for s in Ln if 'const SYNC_KEYS = [' in s] == [s for s in Lh if 'const SYNC_KEYS = [' in s]
        else:   # regress — HEAD 판 대신 기준 스냅샷(앞 인도판 새 판 줄 묶음 md5) · 새 판 조건(pastBadgeHtml = '' 하나 · 929줄 > 60000자)은 그대로
            Ln = new.split('\n')
            pb = QC.same('G10/pastBadgeHtml', _rg_md5([s for s in Ln if 'pastBadgeHtml' in s])) and new.count("const pastBadgeHtml = '';") == 1
            lg = QC.same('G10/long', _rg_md5([s for s in Ln if len(s) > 3000]))
            v929 = _rg_md5(Ln[928]) if len(Ln) > 928 else None
            l929 = v929 is not None and v929 == QC.base('G10/l929', v929) and len(Ln[928]) > 60000
            sk = QC.same('G10/SYNC_KEYS', _rg_md5([s for s in Ln if 'const SYNC_KEYS = [' in s]))
            print('  (기댓값 = %s — 바탕 HEAD 판 대신 앞 인도판 새 판 글자)' % QC.base_note('G10/long'))
        for name, ok in (("pastBadgeHtml = '' 그대로", pb), ('긴 줄(>3000자) 전부 글자까지 같다', lg), ('SheetJS 929줄 바이트 무변', l929), ('SYNC_KEYS 무변', sk)):
            print('  %-36s %s' % (name, 'PASS' if ok else 'FAIL'))
        g10 = pb and lg and l929 and sk
        print()

    print('=== 게이트 표 (NEW / HEAD) ===')
    for g in GATES if not QC.SMOKE else ['G1']:
        if g == 'G3':
            print('  %-4s NEW %-8s HEAD —(대조 기준)' % (g, 'PASS' if g3_ok else 'FAIL'))
        elif g == 'G10':
            print('  %-4s NEW %-8s HEAD —(소스 대조)' % (g, 'PASS' if g10 else 'FAIL'))
        else:
            print('  %-4s NEW %-8s HEAD %s' % (g, tally(res.get('NEW'), g), tally(res.get('HEAD'), g)))
    nf = res.get('NEW') is None or any(x.startswith('FAIL') for x in res['NEW'])
    ok = (not nf) and g3_ok and g10
    print()
    print('종합 : %s' % ('ALL PASS' if ok else 'FAIL 있음'))
    return 0 if ok else 1


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__CERR=[];(function(){var ce=console.error.bind(console);console.error=function(){try{__CERR.push(Array.prototype.map.call(arguments,function(x){return typeof x==='string'?x:(x&&x.message)||JSON.stringify(x)}).join(' '))}catch(e){}return ce.apply(null,arguments);};})();
window.__ALERTS=[];window.alert=function(m){__ALERTS.push(String(m));};window.confirm=function(){return true;};window.prompt=function(){return null;};
window.fetch=function(){return Promise.resolve(new Response('{"message":"harness"}',{status:404,headers:{'Content-Type':'application/json'}}));};
localStorage.clear();
</script>"""

TESTS = r"""<script>
window.onload=null;
(function(){
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,500):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v));   /* 한 줄로 — 여러 줄 글이 줄마다 갈려 대조가 깨졌다 */
const J=v=>JSON.stringify(v);
const lsO=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return {}}};
const BASE={'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const resetLS=o=>{ localStorage.clear(); for(const k in BASE) localStorage.setItem(k,BASE[k]); for(const k in (o||{})) localStorage.setItem(k,typeof o[k]==='string'?o[k]:JSON.stringify(o[k])); try{useIdxDrop()}catch(e){} };
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
const key=(el,k)=>el.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true,cancelable:true}));
const btnIn=(root,text)=>root?[...root.querySelectorAll('button')].find(b=>b.textContent.trim()===text):null;
const rowOf=id=>[...document.querySelectorAll('#search-results > button')].find(b=>b.textContent.indexOf('ID '+id)>=0);
const gItem=(k,i,t)=>({k:k,i:i,t:t,ok:null,ts:1789000000000,cs:[]});
const CH='1. 총칙 > 1.1 민법의 법원';
say('판 = '+(typeof recStripHTML==='function'?'NEW(recStripHTML 있음)':'HEAD'));

async function G1(){
  resetLS({ox_q_geunge:{Q9901:[gItem('g_Q9901_a',1,'첫 근거')],Q9904:[gItem('g_Q9904_a',1,'연결 없는 근거')]},ox_q_reflinks:{Q9901:{geunge:['Q9903','QZZZZ']}}});
  loadQuiz(); showHome(); closeAllWins();
  showFieldDistribution('m');
  const gi=_fieldGroups.indexOf(fieldGroupKey(quizData.find(q=>q.id==='Q9901')));
  showFieldList('m',gi);
  const row=rowOf('Q9901');
  if(!row){ T('G1 근거 목록에 Q9901 행이 있다',false,document.getElementById('search-results').textContent.slice(0,200)); return; }
  row.click();
  const win=document.getElementById('oxwin-q-Q9901');
  const q=quizData.find(x=>x.id==='Q9901');
  const title=win?(win.querySelector('.oxwin-head > div > div')||{}).textContent:null;
  T('G1 근거 목록 행을 누르면 그 문항 팝업(.oxwin)이 뜬다', !!win&&document.querySelectorAll('.oxwin').length===1, 'oxwin '+document.querySelectorAll('.oxwin').length+' · 퀴즈화면 '+!document.getElementById('quiz-screen').classList.contains('hide'));
  T('G1 팝업 제목 = qLabelOf · qWhere', title===qLabelOf(q)+' · '+qWhere(q), title);
  T('G1 첫 화면 그대로(문제 목록으로 자리를 옮기지 않았다)', !document.getElementById('home-screen').classList.contains('hide'));
  closeAllWins(); showHome();
  showFieldDistribution('l');
  const gl=_fieldGroups.indexOf(fieldGroupKey(quizData.find(q=>q.id==='Q9903')));
  showFieldList('l',gl);
  const lrow=rowOf('Q9903');
  if(lrow) lrow.click();
  T('G1 논리 행은 지금처럼 문제로 이동(팝업 없음)', !!lrow&&!document.querySelector('.oxwin')&&!document.getElementById('quiz-screen').classList.contains('hide'), 'row '+!!lrow+' · oxwin '+document.querySelectorAll('.oxwin').length);
  showHome();
}
async function G2(){
  resetLS({ox_q_geunge:{Q9901:[gItem('g_Q9901_a',1,'첫 근거')],Q9904:[gItem('g_Q9904_a',1,'연결 없는 근거')]},ox_q_reflinks:{Q9901:{geunge:['Q9903','QZZZZ']}}});
  loadQuiz(); showHome(); closeAllWins();
  showFieldDistribution('m');
  showFieldList('m',_fieldGroups.indexOf(fieldGroupKey(quizData.find(q=>q.id==='Q9901'))));
  const chipsOf=row=>row?[...row.firstElementChild.querySelectorAll('span')].filter(s=>/^🔗 /.test(s.textContent.trim())):[];
  const c1=chipsOf(rowOf('Q9901'));
  T('G2 연결 둘인 행에 🔗 칩 둘(refOf 만큼)', c1.length===2&&c1[0].textContent.trim()==='🔗 Q9903'&&c1[1].textContent.trim()==='🔗 QZZZZ', J(c1.map(x=>x.textContent)));
  T('G2 지금 데이터에 없는 uid 칩은 opacity-40', c1.length===2&&!c1[0].classList.contains('opacity-40')&&c1[1].classList.contains('opacity-40'), J(c1.map(x=>x.className)));
  T('G2 칩에는 onclick 이 없다(행 전체가 단추)', c1.length>0&&c1.every(x=>!x.getAttribute('onclick')), J(c1.map(x=>x.getAttribute('onclick'))));
  showFieldList('m',_fieldGroups.indexOf(fieldGroupKey(quizData.find(q=>q.id==='Q9904'))));
  T('G2 연결 0 인 행은 칩 0', !!rowOf('Q9904')&&chipsOf(rowOf('Q9904')).length===0, rowOf('Q9904')?rowOf('Q9904').innerHTML.slice(0,200):'행 없음');
}
function G3(){
  const realNow=Date.now, realRnd=Math.random; let clk=1789000000000, seed=12345;
  Date.now=()=>(clk+=1000); Math.random=()=>{ seed=(seed*16807)%2147483647; return (seed-1)/2147483646; };
  try{
    resetLS({ox_q_geunge:{Q9903:[gItem('g_Q9903_a',1,'연결될 근거 글')]},ox_q_reflinks:{}});
    openQuiz(['Q9901','Q9902'],'민법총칙',CH);
    const uid='Q9901';
    const step=n=>V('G3.store.'+n,{gg:localStorage.getItem('ox_q_geunge'),ref:localStorage.getItem('ox_q_reflinks')});
    const inp=document.getElementById('gg-in-'+uid); inp.value='카드에서 적은 근거'; key(inp,'Enter'); step('1적기');
    const k=(ggOf(uid)[0]||{}).k;
    const chip=document.getElementById('gg-chip-'+uid+'-'+k); if(chip) chip.click();
    const pan=document.getElementById('gg-pan-'+uid+'-'+k); const eb=btnIn(pan,'고치기'); if(eb) eb.click();
    const ein=document.getElementById('gg-ein-'+uid+'-'+k); if(ein){ ein.value='카드에서 고친 근거'; const sb=btnIn(document.getElementById('gg-edit-'+uid+'-'+k),'저장'); if(sb) sb.click(); }
    step('2고치기');
    const cin=document.getElementById('gg-cin-'+uid+'-'+k); if(cin){ cin.value='댓글 하나'; key(cin,'Enter'); } step('3댓글');
    const sbtn=[...document.querySelectorAll('#gg-box-'+uid+' button')].find(b=>b.textContent.trim()==='🔍'); if(sbtn) sbtn.click();
    const sin=document.getElementById('link-search-geunge-'+uid); if(sin){ sin.value='연결될'; sin.dispatchEvent(new Event('input',{bubbles:true})); }
    const hit=[...document.querySelectorAll('#link-results-geunge-'+uid+' button')].find(b=>b.textContent.indexOf('Q9903')>=0); if(hit) hit.click();
    step('4연결');
    const rc=document.getElementById('gg-refchip-'+uid+'-Q9903'); if(rc) rc.click();
    const rk=(ggOf('Q9903')[0]||{}).k;
    const rbox=document.getElementById('refgg-box-'+uid+'-Q9903'); const rb=btnIn(rbox,'✎ 여기서 고치기'); if(rb) rb.click();
    const rein=document.getElementById('refgg-ein-'+uid+'-Q9903-'+rk); if(rein){ rein.value='연결 상자에서 고친 글'; const rs=btnIn(document.getElementById('refgg-edit-'+uid+'-Q9903-'+rk),'저장'); if(rs) rs.click(); }
    step('5여기서고치기');
    const cut=btnIn(document.getElementById('refgg-box-'+uid+'-Q9903'),'× 연결 끊기'); if(cut) cut.click(); step('6연결끊기');
    const db=btnIn(document.getElementById('gg-pan-'+uid+'-'+k),'지우기'); if(db) db.click(); step('7지우기');
    V('G3.dom.after', document.getElementById('gg-box-'+uid)?document.getElementById('gg-box-'+uid).outerHTML:'없음');
    resetLS({ox_q_geunge:{Q9901:[{k:'g_Q9901_x',i:1,t:'고정 근거',ok:true,ts:1789000000000,cs:[{k:'c_Q9901_1',t:'고정 댓글',ts:1789000001000}]},{k:'g_Q9901_y',i:2,t:'둘째',ok:false,ts:1789000002000,cs:[]}],Q9903:[gItem('g_Q9903_a',1,'연결될 근거 글')]},ox_q_reflinks:{Q9901:{geunge:['Q9903','QZZZZ']}}});
    V('G3.html.ggLineHTML', ggLineHTML('Q9901'));
  } catch(e){ T('G3 하네스가 죽었다',false,e.message); }
  finally { Date.now=realNow; Math.random=realRnd; }
}
async function G4(){
  resetLS({ox_q_geunge:{},ox_q_reflinks:{}});
  closeAllWins();
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  openQPopup('Q9901');
  const pin=document.getElementById('qp-gg-in-Q9901');
  T('G4 팝업 안에 근거 줄이 있다(범위 qp-)', !!pin&&!!pin.closest('.oxwin'), '팝업 근거 칸 '+!!pin);
  if(!pin) { closeAllWins(); return; }
  pin.value='팝업에서 적은 근거'; key(pin,'Enter');
  const list=ggOf('Q9901'), k=(list[0]||{}).k;
  const pchip=document.getElementById('qp-gg-chip-Q9901-'+k), cchip=document.getElementById('gg-chip-Q9901-'+k), cin=document.getElementById('gg-in-Q9901');
  T('G4 팝업에서 적은 글이 팝업 칩으로 닫힌다', !!pchip&&!!pchip.closest('.oxwin'), '팝업 칩 '+!!pchip);
  T('G4 카드 칸은 비어 있다', !!cin&&cin.value===''&&!cin.closest('.oxwin'), cin?J(cin.value):'없음');
  T('G4 저장소에 1건', list.length===1&&list[0].t==='팝업에서 적은 근거', J(list));
  T('G4 카드 #gg-box 가 새 칩을 보인다', !!cchip&&!cchip.closest('.oxwin'), '카드 칩 '+!!cchip);
  const cin2=document.getElementById('gg-in-Q9901'); cin2.value='카드에서 적은 둘째'; key(cin2,'Enter');
  const k2=(ggOf('Q9901')[1]||{}).k;
  T('G4 (반대) 카드에서 적으면 떠 있는 팝업 상자도 새 칩을 보인다', !!k2&&!!document.getElementById('qp-gg-chip-Q9901-'+k2)&&document.getElementById('qp-gg-in-Q9901').closest('.oxwin')!==null, 'k2 '+k2);
  closeAllWins();
}
async function G5(){
  const t286=('메모에서 옮겨 온 긴 근거 가나다라마바사 ').repeat(20).slice(0,286);
  resetLS({ox_q_geunge:{Q9901:[{k:'g_Q9901_m',i:1,t:t286,ok:null,ts:1,cs:[],src:'memo'}]},ox_q_reflinks:{}});
  loadQuiz(); showHome(); closeAllWins();
  openQPopup('Q9901');
  const chip=document.getElementById('qp-gg-chip-Q9901-g_Q9901_m');
  if(!chip){ T('G5 팝업 안에 근거 칩이 있다',false,'칩 없음'); closeAllWins(); return; }
  chip.click();
  const pan=document.getElementById('qp-gg-pan-Q9901-g_Q9901_m');
  btnIn(pan,'고치기').click();
  const ein=document.getElementById('qp-gg-ein-Q9901-g_Q9901_m');
  ein.value=t286+' — 팝업에서 고침';
  btnIn(document.getElementById('qp-gg-edit-Q9901-g_Q9901_m'),'저장').click();
  T('G5 팝업에서 286자 근거를 고쳐 저장된다', (ggOf('Q9901')[0]||{}).t===t286+' — 팝업에서 고침', ((ggOf('Q9901')[0]||{}).t||'').length);
  btnIn(pan,'고치기').click();
  ein.value='가'.repeat(4001);
  btnIn(document.getElementById('qp-gg-edit-Q9901-g_Q9901_m'),'저장').click();
  const note=document.getElementById('qp-gg-ein-Q9901-g_Q9901_m-over');
  T('G5 4001자 — 「4000자까지 · 지금 4001자」가 팝업 안 칸 아래에', !!note&&!!note.closest('.oxwin')&&/4000자까지 · 지금 4001자/.test(note.textContent), note?note.textContent:'안내 없음');
  T('G5 4001자는 저장되지 않는다', (ggOf('Q9901')[0]||{}).t===t286+' — 팝업에서 고침');
  closeAllWins();
}
async function G6(){
  if(typeof recStripHTML!=='function'){ T('G6 recStripHTML 이 있다',false,'없음'); return; }
  const hist={};
  hist['민법총칙||'+CH+'||all||all']=[{score:1,total:2,date:'2026. 9. 1.',marks:{Q9901:false}},{score:1,total:2,date:'2026. 9. 3.',marks:{Q9901:false}}];
  hist['⚡빠른실행||🔥 약점 다시 풀기 (틀림+헷갈림)||all||all']=[{score:1,total:1,date:'2026. 9. 5.',marks:{Q9901:true},cf:{Q9901:true}}];
  hist['⚡빠른실행||🌤 덜약점 (한 번 더)||all||all']=[{score:0,total:1,date:'2026. 9. 7.',marks:{Q9901:false},cf:{}}];
  resetLS({ox_chap_history:hist,ox_q_tags:{Q9901:{confuse:false}},ox_in_progress:{}});
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  const parse=h=>{ const d=document.createElement('div'); d.innerHTML=h; const w=d.firstElementChild; const rows=w?[...w.children]:[];
    const cells=r=>r?[...r.children].filter(x=>/width:22px/.test(x.getAttribute('style')||'')):[];
    return {w,rows,top:cells(rows[0]).map(x=>x.textContent),bot:cells(rows[1]).map(x=>x.textContent),topEl:cells(rows[0]),last:rows[0]?[...rows[0].children].find(x=>/마지막/.test(x.textContent)):null,text:d.textContent.replace(/\s/g,'')}; };
  const a=parse(recStripHTML('Q9901'));
  V('G6.a',{top:a.top,bot:a.bot,text:a.text});
  T('G6 윗줄 X X O X ·', J(a.top)===J(['X','X','O','X','·']), J(a.top));
  T('G6 아랫줄 – – △ (빈) (빈)', J(a.bot)===J(['–','–','△','','']), J(a.bot));
  T('G6 줄 끝 「마지막 9/7」(채점된 것 중 가장 늦은 날)', !!a.last&&a.last.textContent.trim()==='마지막 9/7', a.last&&a.last.textContent);
  T('G6 딱 두 줄 · 개수 요약 글자 0', a.rows.length===2&&a.text==='XXOX·마지막9/7––△', a.rows.length+' · '+a.text);
  T('G6 칸 title = M/D · 단원라벨 · N회독째 (⚡면 큐 이름)', (a.topEl[0]&&a.topEl[0].title)==='9/1 · '+CH+' · 1회독째'&&(a.topEl[2]&&a.topEl[2].title)==='9/5 · ⚡ 🔥 약점 다시 풀기 (틀림+헷갈림) · 1회독째', J(a.topEl.map(x=>x.title)));
  T('G6 칸 색 — O 파랑 · X 빨강 · · 회색 점선', /text-blue-700/.test(a.topEl[2].className)&&/text-red-700/.test(a.topEl[0].className)&&/border-dashed/.test(a.topEl[4].className), J(a.topEl.map(x=>x.className)));
  const hist2=JSON.parse(J(hist)); hist2['민법총칙||1. 총칙 > 1.2 신의칙||all||all']=[{score:0,total:1,date:'2026. 8. 30.',marks:{Q9901:true}}];
  const prog={}; prog['민법총칙||'+CH+'||all||all']={marks:{Q9901:true},date:'2026. 9. 9.',total:2}; prog['민법총칙||1. 총칙 > 1.2 신의칙||all||all']={marks:{Q9901:false},date:'2026. 9. 8.',total:1};
  resetLS({ox_chap_history:hist2,ox_q_tags:{Q9901:{confuse:true}},ox_in_progress:prog});
  const b=parse(recStripHTML('Q9901'));
  V('G6.b',{top:b.top,bot:b.bot,titles:b.topEl.map(x=>x.title)});
  T('G6 차례 — 날짜 오름차순(늦게 넣은 키의 8/30 이 맨 앞) · 진행중 다른 chapKey 한 칸 · 이번 세션 맨 끝', J(b.top)===J(['O','X','X','O','X','X','·']), J(b.top));
  T('G6 진행중 칸은 점선 · title 에 「진행중」 · 지금 chapKey 의 진행중은 안 센다', /border-dashed/.test(b.topEl[5].className)&&/진행중/.test(b.topEl[5].title)&&b.topEl.filter(x=>/진행중/.test(x.title)).length===1, J(b.topEl.map(x=>x.title)));
  T('G6 이번 세션 칸의 △ 는 지금 태그(헷갈림)', b.bot[b.bot.length-1]==='△', J(b.bot));
  resetLS({ox_chap_history:{},ox_in_progress:{}});
  const c=recStripHTML('Q9901');
  T('G6 기록이 0이면 「풀이 기록 없음」 한 줄', /풀이 기록 없음/.test(c)&&!/width:22px/.test(c), c.slice(0,200));
}
async function G7(){
  resetLS({ox_chap_history:{},ox_q_tags:{Q9902:{confuse:true},Q9901:{confuse:false}},ox_in_progress:{}});
  openQuiz(['Q9901','Q9902','Q9903'],'민법총칙',CH);
  currentSessionMarks={Q9901:true,Q9902:false,Q9903:true}; currentSessionScore=2;
  finishChapter();
  const key1='민법총칙||'+CH+'||all||all';
  const h=lsO('ox_chap_history')[key1]||[], e=h[h.length-1]||{};
  V('G7.a',e);
  T('G7 finishChapter 새 항목에 cf 가 있고 헷갈림 문항만 들어 있다', J(e.cf)===J({Q9902:true}), J(e.cf));
  localStorage.setItem('ox_q_tags','{}');
  openQuiz(['Q9901','Q9902','Q9903'],'민법총칙',CH);
  currentSessionMarks={Q9901:true}; currentSessionScore=1;
  finishChapter();
  const h2=lsO('ox_chap_history')[key1]||[], e2=h2[h2.length-1]||{};
  T('G7 헷갈림 0 이면 cf = {} (칸 자체는 있다)', h2.length===2&&Object.prototype.hasOwnProperty.call(e2,'cf')&&J(e2.cf)==='{}', J(e2));
  T('G7 다른 칸(score·total·confuse·fake·date·marks·labels)은 그대로', ['score','total','confuse','fake','date','marks','labels'].every(x=>Object.prototype.hasOwnProperty.call(e2,x)), J(Object.keys(e2)));
  showHome();
}
async function G8(){
  const hist={}; hist['민법총칙||'+CH+'||all||all']=[{score:1,total:2,date:'2026. 9. 1.',marks:{Q9901:false,Q9902:true}}];
  resetLS({ox_chap_history:hist,ox_q_tags:{},ox_in_progress:{}});
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  const btn=document.querySelector('#q-box-Q9901 button[onclick^="recStripToggle"]');
  T('G8 출처 칩이 단추다(recStripToggle)', !!btn, document.querySelector('#q-box-Q9901')?'':'카드 없음');
  if(!btn) return;
  btn.click();
  const strip=document.getElementById('rec-strip-Q9901');
  const open1=!!strip&&!strip.classList.contains('hide');
  const before=strip?strip.textContent.replace(/\s/g,''):'';
  document.querySelector('input[name="answer_Q9901"][value="O"]').checked=true;
  document.querySelector('input[name="answer_Q9902"][value="X"]').checked=true;
  gradeCurrentPage();
  const after=strip.textContent.replace(/\s/g,'');
  const td=new Date(), md=(td.getMonth()+1)+'/'+td.getDate();
  V('G8',{before:before,after:after});
  T('G8 누르면 헤더 줄 바로 아래에 열린다', open1&&strip.previousElementSibling&&/border-b/.test(strip.previousElementSibling.className), strip&&strip.previousElementSibling?strip.previousElementSibling.className:'');
  T('G8 채점 전 이번 칸은 ·', before==='X·마지막9/1–', before);
  T('G8 채점 직후 열려 있던 상자가 이번 칸을 O/X 로 바꾼다(다시 안 그려진 카드)', after==='XO마지막'+md+'–', after);
  btn.click();
  T('G8 다시 누르면 접힌다', strip.classList.contains('hide'));
  try{ closeGradeModal(); }catch(e){}
}
async function G9(){
  resetLS({ox_chap_history:{},ox_q_tags:{},ox_in_progress:{}});
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  const b2=document.getElementById('q-box-Q9902'), b1=document.getElementById('q-box-Q9901');
  T('G9 출처 없는 문항은 칩도 상자도 없다', !!b2&&!b2.querySelector('[onclick^="recStripToggle"]')&&!document.getElementById('rec-strip-Q9902'), b2?'':'카드 없음');
  T('G9 (확인) 출처 있는 문항은 칩과 빈 상자(닫힘)가 있다', !!b1&&!!b1.querySelector('button[onclick^="recStripToggle"]')&&!!document.getElementById('rec-strip-Q9901')&&document.getElementById('rec-strip-Q9901').classList.contains('hide')&&document.getElementById('rec-strip-Q9901').innerHTML==='', b1?'':'카드 없음');
  const sb=b1?b1.querySelector('[onclick^="recStripToggle"]'):null;
  T('G9 (확인) 출처 칩 class 는 옛 글자 그대로', !!sb&&sb.className==='bg-purple-100 text-purple-800 text-[11px] font-extrabold px-2 py-0.5 rounded-md border border-purple-200 whitespace-nowrap', sb?sb.className:'');
}
async function G11(){
  resetLS({});
  loadQuiz(); showHome(); closeAllWins();
  renderDashboard();
  T('G11 첫 화면이 그려진다', document.getElementById('dashboard-container').children.length>0);
  startQuiz('민법총칙',CH);
  T('G11 문제풀이가 열린다', !document.getElementById('quiz-screen').classList.contains('hide')&&!!document.getElementById('q-box-Q9901'));
  goHome();
  startQuiz('변리사 기출','2016년 제53회');
  T('G11 기출뷰가 열린다', !!document.getElementById('q-box-Q9905'), document.getElementById('quiz-container').textContent.slice(0,120));
  goHome();
  /* 정리OMR 뷰어(openViewer)는 클로저 안이라 밖에서 못 부른다 — 사람이 누르는 그 길(카드의 📍 핀 단추 · injectPins 가 붙인다)로 연다 */
  startQuiz('민법총칙',CH);
  await new Promise(r=>setTimeout(r,250));
  const a0=__ALERTS.length;
  const pin=document.getElementById('tag-coord-Q9901');
  if(pin) pin.click();
  let cd=null;                                                    /* openViewer 는 IndexedDB 를 기다린다 — 조건이 설 때까지 기다린다 */
  for(let i=0;i<200&&!(cd=document.getElementById('cd-close'));i++) await new Promise(r=>setTimeout(r,50));
  T('G11 정리OMR(좌표기억) 뷰어가 열린다(카드 📍 핀 단추)', !!pin&&!!cd&&__ALERTS.length===a0, 'pin '+!!pin+' · cd-close '+!!cd+' · alert '+__ALERTS.slice(a0).join('/'));
  if(cd) cd.click();
  goHome();
}

async function Gprobe(){
  resetLS({ox_chap_history:{},ox_q_tags:{},ox_in_progress:{}});
  openQuiz(['Q9901','Q9902'],'민법총칙',CH);
  document.querySelector('input[name="answer_Q9901"][value="O"]').checked=true;
  document.querySelector('input[name="answer_Q9902"][value="X"]').checked=true;
  gradeCurrentPage();
  try{ closeGradeModal(); }catch(e){}
  T('Gp (진단) 채점만 돌렸다', true);
}
const LIST=(P.gradeOnly?[['Gp',Gprobe]]:[['G1',G1],['G2',G2],['G3',G3],['G4',G4],['G5',G5],['G6',G6],['G7',G7],['G8',G8],['G9',G9],['G11',G11]]).filter(x=>P.skip.indexOf(x[0])<0);
if(P.skip.length) say('건너뜀(진단용) : '+P.skip.join(','));
setTimeout(async function(){
  for(const [n,f] of LIST){
    console.log('HZ-START '+n);
    try{ await f(); }
    catch(e){ T(n+' 하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' ')); }
    console.log('HZ-END '+n+' · '+R.filter(x=>x.startsWith('FAIL')).length+' FAIL');
  }
  console.log('HZ-WAIT');
  await new Promise(r=>setTimeout(r,300));
  console.log('HZ-OUT '+R.length);
  const errs=(window.__ERR||[]), cerr=(window.__CERR||[]);
  T('G11 헤드리스 페이지 오류 0 · console.error 0', errs.length===0&&cerr.length===0, 'error '+errs.length+' '+errs.slice(0,3).join(' / ')+' · console.error '+cerr.length+' '+cerr.slice(0,3).join(' / '));
  say('alert '+__ALERTS.length+'번 : '+__ALERTS.slice(0,3).join(' / '));
  const pre=document.createElement('pre'); pre.id='hz-out'; pre.textContent=R.join('\n'); document.documentElement.appendChild(pre);
  R.forEach(x=>console.log('HZR|'+encodeURIComponent(x)));   /* 크롬이 뒤에 죽어도 결과가 stderr 에 남는다 */
  console.log('HZR|END');
  console.log('HZ-DONE');
},1500);
})();
</script>
"""

if __name__ == '__main__':
    sys.exit(main())
