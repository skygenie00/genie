# -*- coding: utf-8 -*-
"""tt앱 경주 하네스 — `_task_tt_sync_lost_add1.md` §3 갈음판.

**스텁이 창을 직접 연다.** 감시 파일의 ghGet/ghPut 안에서 upsert 를 부르므로
지연을 얼마로 잡든·파일 차례가 바뀌든 항상 창 한가운데다(시계로 안 맞춘다).

⚠ 토큰은 **시드가 아니라 시험 스크립트에서** 켠다 — 시드에 넣으면 파일 끝
   `if(cfg.token)syncAll(true)` 가 먼저 돌아 syncing 을 점유한다(add1 §2).

쓰기 : python _harness_tt_race.py          (다섯 판 직렬)
       python _harness_tt_race.py A        (하나만)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
# --mode gate|regress|smoke (_task_qa_slim2 2026-10-08 · 인자 없으면 gate = 이 판 앞과 같음)
#   regress = 판 다섯(A~E) · 칸 다섯 모두 「회귀」(처리표) — 판마다 띄움 한 번은 gate 와 같고 결과 html · 크롬 프로필만 %TEMP%\h_tt_race(gate = 하네스 옆 N: h_race)
#   smoke   = 판 A(세션 · ghGet 창) 하나만 띄워 「새로 만든 것이 살아남았다」(+ 예외 잡이 줄)만 찍는다 — 인자로 판을 주면 그 판
#   N:(마이박스) 크롬 프로필을 TEMP 로 옮기는 까닭 — N: 프로필은 띄움마다 느리다: 9/17 tt 회귀(N: 결과 파일 시각) _harness_timetable 76 초 · tt_race 판마다 76~92 초 /
#     10/6 use_count N: 프로필 --dump-dom 180 초 초과 되풀이 → 사용자 「해」로 TEMP(결정로그 10/6 21:36 · 22:0x) / 프로필이 TEMP 인 민법 dump-dom 하네스는 띄움당 9~14 초
#     · 마이박스가 하네스 프로필 폴더 목록을 못 펼쳐 _qa_sync copy 10 분 멈춤 · 실행기 열쇠 셈 멈춤(결정로그 10/2 · 10/4)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) A-1 · 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · import 때 --mode · --snap-in · --snap-out 을 sys.argv 에서 뗀다
import json, os, re, subprocess, sys

SRC = _roots.genie(r"timetable\index.html")
if QC.REGRESS:   # regress · smoke — 결과 html · 크롬 프로필을 N:(마이박스) 밖 로컬 임시 폴더로(A-2 · 까닭 = 머리 주석) · gate 는 이 판 앞 그대로
    import tempfile as _rg_tf
    OUT = os.path.join(_rg_tf.gettempdir(), 'h_tt_race')
else:
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_race")
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ANCHOR = "<script>\n/* ============================================================\n   타임테이블 v1"

PIN = ("<script>(function(){const R=Date;const OFF=new R('2026-09-05T12:00:00+09:00').getTime()-R.now();"
       "function D(...a){return a.length?new R(...a):new R(R.now()+OFF)}D.prototype=R.prototype;"
       "D.now=()=>R.now()+OFF;D.parse=R.parse;D.UTC=R.UTC;window.Date=D;})();</script>")

PERSON = '꼬까'
SESS = 'sessions/%s/2026-09.json' % PERSON
SEED_SESS = {'v': 1, 'sessions': [{'id': 'seed1', 'd': '2026-09-01', 's': '민법', 'a': 600, 'b': 660, 'u': 1}]}

# name · 설명 · 감시경로 · 시드 · 창에서 칠 것 · 어느 창(get|put) · run 이 필요한가
SCEN = [
    ('A', '세션 · ghGet 창에서 STOP', SESS, SEED_SESS, 'stopTimer()', 'get', True),
    ('B', '세션 · ghPut 창에서 STOP', SESS, SEED_SESS, 'stopTimer()', 'put', True),
    ('C', '할일 · ghGet 창에서 upsertTodo', 'todos/%s.json' % PERSON,
     {'v': 2, 'cats': [], 'items': [{'id': 'seedT', 'n': '씨앗', 'u': 1}]},
     "upsertTodo({id:'RACE_T',n:'경주',done:false})", 'get', False),
    ('D', '시험기록 · ghGet 창에서 upsertExam', 'exam/%s.json' % PERSON,
     {'v': 1, 'items': [{'id': 'seedX', 'u': 1}]},
     "upsertExam({id:'RACE_X',who:%s})" % json.dumps(PERSON, ensure_ascii=False), 'get', False),
    ('E', '음식 · ghGet 창에서 upsertFood', 'food/food.json',
     {'v': 1, 'items': [{'id': 'seedF', 'name': '씨앗', 'u': 1}]},
     "upsertFood({id:'RACE_F',name:'경주'})", 'get', False),
]

# ⚠ 토큰 없음 — 부팅 syncAll 을 막는다(add1 §2)
SEED_TPL = """<script>
localStorage.clear();
localStorage.setItem('tt.cfg',JSON.stringify({person:__PERSON__,token:'',lastSync:0}));
localStorage.setItem('tt.f.__WATCH__',JSON.stringify({data:__SEEDDATA__,sha:null,dirty:true}));
</script>"""

RACE_TPL = r"""<script>
(async function(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i):''));
const say=s=>R.push('INFO | '+s);
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const WATCH=__WATCH__, DEF=__DEF__, WHERE=__WHERE__;
const IDS=d=>(((d||{}).sessions||(d||{}).items||[]).map(x=>x.id));
const REM={},GETS=[],PUTS=[];
let openedAt=null,stopAt=null,fired=false,actErr='';

/* add1 §2 — 가르는 세 값. 토큰을 켜기 전에 먼저 잰다 */
const pre={token:cfg.token,onLine:navigator.onLine,syncing:(typeof syncing!=='undefined')?syncing:'?'};

/* ① 토큰은 여기서 켠다(시드에 넣으면 부팅 sync 가 syncing 을 점유) */
cfg.token='t_test';LS.set('tt.cfg',cfg);
try{Object.defineProperty(navigator,'onLine',{get:()=>true,configurable:true})}catch(e){}
/* ⚠ ui.view 는 건드리지 않는다 — 'arch' 로 바꾸면 분석 화면이 ghGetRaw 로 진짜 網을 때려
   크롬이 180초 타임아웃까지 간다(실측). food 는 시드가 dirty 라 listDirty() 로 들어온다. */
window.fetch=()=>Promise.reject(new Error('net blocked by harness'));
window.ghGetRaw=async()=>null;

/* ② 스텁이 창을 연다 */
window.ghGet=async function(p){GETS.push(p);
 if(p===WATCH&&WHERE==='get'&&!fired){fired=true;openedAt=Date.now();
  await sleep(50);try{__ACTION__}catch(e){actErr=e.message}stopAt=Date.now();await sleep(50);}
 else await sleep(30);
 const r=REM[p];return r?{sha:r.sha,data:JSON.parse(JSON.stringify(r.data))}:null;};
window.ghPut=async function(p,d,sha){PUTS.push({p:p,ids:IDS(d)});
 if(p===WATCH&&WHERE==='put'&&!fired){fired=true;openedAt=Date.now();
  await sleep(50);try{__ACTION__}catch(e){actErr=e.message}stopAt=Date.now();await sleep(50);}
 else await sleep(30);
 REM[p]={sha:'s'+PUTS.length,data:JSON.parse(JSON.stringify(d))};return REM[p].sha;};

/* ③ 돌고 있는 타이머(STOP 판만) */
__RUNSEED__

const idsBefore=IDS((JSON.parse(localStorage.getItem('tt.f.'+WATCH)||'null')||{}).data);

try{
 await syncAll(true);                           /* 창 안에서 STOP 이 떨어진다 */
 const f1=loadF(WATCH,DEF);
 const ids1=IDS(f1.data);
 const NEW=ids1.filter(x=>idsBefore.indexOf(x)<0)[0]||null;
 const dirty1=f1.dirty;

 await syncAll(true);                           /* ④ 새것이 실제로 올라가는가 */
 const pushed=PUTS.filter(x=>x.p===WATCH).some(x=>NEW&&x.ids.indexOf(NEW)>=0);
 const f2=loadF(WATCH,DEF);

 /* 헛잣대 먼저 — 이게 아니면 아래 판정은 전부 버린다(add1 §3) */
 const watchSeen=GETS.filter(p=>p===WATCH).length;
 T('R-__N__ [헛잣대] 감시 파일이 돌았다(watchSeen>=1)',watchSeen>=1,'gets='+GETS.length+' watchSeen='+watchSeen);
 T('R-__N__ [헛잣대] 창이 열리고 그 안에서 쳤다',!!openedAt&&!!stopAt&&!actErr,'opened='+!!openedAt+' stop='+!!stopAt+' err='+actErr);

 T('R-__N__ 새로 만든 것이 살아남았다',!!NEW&&IDS(f2.data).indexOf(NEW)>=0,'new='+NEW+' ids='+JSON.stringify(IDS(f2.data)));
 T('R-__N__ dirty 로 남아 다시 올라간다',dirty1===true,'dirty(1차 뒤)='+dirty1);
 T('R-__N__ 두 번째 sync 의 push 본문에 그 id',pushed,'puts='+JSON.stringify(PUTS.filter(x=>x.p===WATCH).map(x=>x.ids)));

 say('켜기 전 cfg.token='+JSON.stringify(pre.token)+' · navigator.onLine='+pre.onLine+' · syncing='+pre.syncing);
 say('감시 파일은 syncAll 의 '+(GETS.indexOf(WATCH)+1)+'번째 GET (전체 '+GETS.length+'건)');
 say('창 '+WHERE+' · new='+NEW+' · dirty(1차)='+dirty1+' · dirty(2차)='+f2.dirty+' · pushed='+pushed);
 say('감시 push 본문 '+JSON.stringify(PUTS.filter(x=>x.p===WATCH).map(x=>x.ids)));
}catch(e){T('R-__N__ 하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n')[1])}

const pre2=document.createElement('pre');pre2.textContent=R.join('\n');document.body.appendChild(pre2);
})();
</script>"""

RUNSEED = ("run={s:'민법',p:'객',i:'',cat:'',plan:'',unit:'',band:'',nt:false,"
           "d:'2026-09-05',a:600,at:Date.now()-600000};LS.set('tt.run',run);")


def empty_of(seed):
    return {k: ([] if isinstance(v, list) else v) for k, v in seed.items()}


_RG_SMOKE = ('새로 만든 것이 살아남았다', '하네스가 죽었다')   # smoke — 처리표 smoke 칸 + 예외 잡이 줄의 제목 끝(제목 = 「R-<판> …」)


def _rg_title(ln):
    """결과 줄 「PASS | 제목 | 값」의 제목 — smoke 거름(smoke 칸 끝)"""
    p = ln.split(' | ')
    return p[1] if len(p) > 1 else ln


def run_one(name, desc, watch, seed, action, where, need_run):
    html = open(SRC, encoding='utf-8').read()
    assert ANCHOR in html, 'seed anchor not found'
    seed_js = (SEED_TPL.replace('__PERSON__', json.dumps(PERSON, ensure_ascii=False))
                       .replace('__WATCH__', watch)
                       .replace('__SEEDDATA__', json.dumps(seed, ensure_ascii=False)))
    html = html.replace(ANCHOR, PIN + seed_js + ANCHOR, 1)
    race = (RACE_TPL.replace('__WATCH__', json.dumps(watch, ensure_ascii=False))
                    .replace('__DEF__', json.dumps(empty_of(seed), ensure_ascii=False))
                    .replace('__WHERE__', json.dumps(where))
                    .replace('__RUNSEED__', RUNSEED if need_run else '')
                    .replace('__ACTION__', action).replace('__N__', name))
    html = html.replace('</body>', race + '</body>', 1)
    app = os.path.join(OUT, 'app_%s.html' % name)
    open(app, 'w', encoding='utf-8', newline='\n').write(html)

    QC.launch('new')   # §B-4 셈 — 새 판 앱 띄움(판마다 1 · 바탕 띄움 없음)
    with QC.stage('chrome ' + name):   # 단계 시간(판마다 띄움 한 번)
        r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                            '--user-data-dir=' + os.path.join(OUT, 'prof_' + name),
                            '--allow-file-access-from-files', '--window-size=1280,900',
                            '--virtual-time-budget=20000', '--dump-dom',
                            'file:///' + app.replace('\\', '/')],
                           capture_output=True, timeout=180)
    dom = r.stdout.decode('utf-8', 'replace')
    open(os.path.join(OUT, 'dom_%s.html' % name), 'w', encoding='utf-8').write(dom)
    lines = []
    for ln in dom.replace('\r', '').split('\n'):
        s = re.sub(r'^.*?<pre[^>]*>', '', ln)
        s = re.sub(r'</pre>.*$', '', s).strip()
        if s.startswith(('PASS | ', 'FAIL | ', 'INFO | ')):
            lines.append(s)
    print('=== %s  %s ===' % (name, desc))
    if not lines:
        print('   결과 줄 없음 — 부팅 사망? dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom_%s.html' % name)))
        return [('FAIL', '%s 결과 줄 없음' % name)]
    if QC.SMOKE:   # smoke — 처리표 smoke 칸(새로 만든 것이 살아남았다) + 예외 잡이 줄만 찍는다(나머지 칸 · INFO 는 건넘)
        lines = [ln for ln in lines if QC.want(_rg_title(ln), smoke=_rg_title(ln).endswith(_RG_SMOKE))]
    out = []
    for ln in lines:
        print('   ' + ln)
        k = ln.split(' | ')[0]
        if k != 'INFO':
            out.append((k, ln))
    return out


if __name__ == '__main__':
    want = sys.argv[1].upper() if len(sys.argv) > 1 else None
    if QC.SMOKE and not want:   # smoke — 판 A 하나만 띄운다(처리표 smoke = 판 A)
        want = 'A'
    rows = []
    for s in SCEN:
        if want and s[0] != want:
            continue
        rows += run_one(*s)
        print()
    p = sum(1 for k, _ in rows if k == 'PASS')
    f = sum(1 for k, _ in rows if k == 'FAIL')
    print('합계  PASS %d · FAIL %d' % (p, f))
    sys.exit(0 if f == 0 else 1)
