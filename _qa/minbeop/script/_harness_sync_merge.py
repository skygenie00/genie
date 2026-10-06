# -*- coding: utf-8 -*-
"""민법OX 동기화 「합치기」 검산 (minbeop/task/_task_ox_sync_merge.md §K).

한 페이지 안에서 기기 여럿을 흉내 낸다 — localStorage 를 통째로 떠 두었다가 갈아 끼운다(기기 = 저장소 한 벌).
원격 기록 파일은 fetch 흉내(메모리)다. 사람 기기의 기록·깃허브에는 쓰지 않는다(studyplandata 클론은 읽기만).
  NEW  = 작업트리 genie/minbeop/index.html
  HEAD = 고치기 전(헛잣대 — §K 일곱 게이트는 떨어져야 정상)
실물 = studyplandata 클론의 09-15 10:15(PC 14a2d899) · 10:21(아이패드 9a545651) 두 판.
  G5-실물의 기대값은 **파이썬이 따로 짠 합치기 규칙**으로 계산한다(앱 코드를 안 쓴다 — 두 구현 대조).

⚠ 앱 onload(IndexedDB)는 헤드리스 가상 시계와 경합한다 — onload 를 끄고 검사가 syncRecords 를 직접 부른다.
⚠ index.html 은 </body> 가 둘이다 — rindex 로 붙이고 결과는 documentElement 에 붙인다.

쓰기 : python _harness_sync_merge.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import copy, datetime, hashlib, io, json, os, re, shutil, subprocess, sys, tempfile

GENIE = _roots.genie()
SP = _roots.spd()
SRC = os.path.join(GENIE, 'minbeop', 'index.html')
REC = 'minbeop/기록.json'
PC_REV, IP_REV = '14a2d899', '9a545651'
OUT = os.path.join(tempfile.gettempdir(), 'h_sync_merge')     # ⚠ N: 밖(마이박스) · 크롬 프로필은 로컬 디스크
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASELINE = ('G1', 'G2', 'G3', 'G5', 'G7', 'G9', 'G10')        # §K 헛잣대 일곱
KCOUNT = ['ox_q_fix', 'ox_q_logic', 'ox_chap_history', 'ox_q_geunge', 'ox_q_reflinks']
MISSING = '\x00없음'


def git(repo, *a):
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def fn_block(text, head):
    i = text.index(head)
    ls = text.rfind('\n', 0, i) + 1
    j = text.find('\n', i)
    first = text[ls:j]
    if first.rstrip().endswith('}') and first.count('{') == first.count('}'):
        return first
    end = text.find('\n        }\n', j)
    return text[ls:end + len('\n        }')]


# ── 파이썬 쪽 합치기 규칙(앱과 따로 짰다) — G5-실물 기대값
def py_merge(dev, remote, sk):
    u, gone, sh = dev['u'], dev['gone'], dev['shadow']
    rU, rG, rD = remote.get('u') or {}, remote.get('gone') or {}, remote.get('data') or {}
    by = {}
    for s in list(rU) + list(rG):
        k, c = s.split('|', 1)
        by.setdefault(k, set()).add(c)
    took = dele = 0
    for k in sk:
        cur, old, rd = dev['data'].setdefault(k, {}), sh.setdefault(k, {}), (rD.get(k) or {})
        for c in sorted(set(by.get(k, set())) | set(rd)):
            ck = k + '|' + c
            if json.dumps(cur.get(c, MISSING), ensure_ascii=False) != json.dumps(old.get(c, MISSING), ensure_ascii=False):
                continue
            mine, theirs = max(u.get(ck, 0), gone.get(ck, 0)), max(rU.get(ck, 0), rG.get(ck, 0))
            if theirs == 0:
                if mine == 0 and c not in cur and c in rd:
                    cur[c] = copy.deepcopy(rd[c]); u[ck] = 1; took += 1; old[c] = copy.deepcopy(rd[c])
                continue
            if theirs < mine:
                continue
            if rG.get(ck, 0) >= rU.get(ck, 0) and rG.get(ck, 0) > 0:
                if c in cur:
                    del cur[c]; dele += 1; old.pop(c, None)
                gone[ck] = rG[ck]; u.pop(ck, None)
            elif c in rd:
                if c not in cur or json.dumps(cur[c], ensure_ascii=False) != json.dumps(rd[c], ensure_ascii=False):
                    cur[c] = copy.deepcopy(rd[c]); took += 1; old[c] = copy.deepcopy(rd[c])
                u[ck] = rU[ck]; gone.pop(ck, None)
    return took, dele


def py_payload(dev, remote):
    u, g = dict(dev['u']), dict(dev['gone'])
    if remote:
        for x, t in (remote.get('u') or {}).items():
            if not (u.get(x, 0) >= t):
                u[x] = t
        for x, t in (remote.get('gone') or {}).items():
            if not (g.get(x, 0) >= t):
                g[x] = t
        for x in list(u):
            if x in g:
                if g[x] >= u[x]:
                    del u[x]
                else:
                    del g[x]
    return {'v': 1, 'data': copy.deepcopy(dev['data']), 'u': u, 'gone': g}


def counts(data, sk):
    return [len(data.get(k) or {}) for k in KCOUNT] + [sum(len(data.get(k) or {}) for k in sk)]


def build_and_run(tag, src, seed, tests):
    html = src
    k = html.index('<script>', html.index('<body'))
    html = html[:k] + seed + html[k:]
    b = html.rindex('</body>')
    html = html[:b] + tests + html[b:]
    app = os.path.join(OUT, 'app_%s.html' % tag)
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                        '--user-data-dir=' + prof, '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=40000', '--dump-dom', 'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=420)
    dom = r.stdout.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'dom_%s.html' % tag), 'w', encoding='utf-8').write(dom)
    m = re.search(r'<pre id="hz-out">(.*?)</pre>', dom, re.S)
    if not m:
        return None
    txt = m.group(1).replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')
    return [ln for ln in txt.split('\n') if ln.strip()]


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(SRC, encoding='utf-8', newline='').read()
    base = git(GENIE, 'show', 'HEAD:minbeop/index.html')
    sk = json.loads(re.search(r"const SYNC_KEYS = (\[[^\]]*\]);", base).group(1).replace("'", '"'))
    pc, ip = json.loads(git(SP, 'show', PC_REV + ':' + REC)), json.loads(git(SP, 'show', IP_REV + ':' + REC))
    ms = lambda iso: int(datetime.datetime.fromisoformat(iso.replace('Z', '+00:00')).timestamp() * 1000)

    # 실물 두 판 — 서로 다른 칸의 도장·묘비
    cp = {k + '|' + c for k in sk for c in (pc['data'].get(k) or {})}
    ci = {k + '|' + c for k in sk for c in (ip['data'].get(k) or {})}
    print('실물 — PC %s savedAt %s · 아이패드 %s savedAt %s' % (PC_REV, pc['savedAt'], IP_REV, ip['savedAt']))
    for x in sorted(cp ^ ci):
        print('  %s %s · PC u=%s gone=%s · 아이패드 u=%s gone=%s' % ('PC만' if x in cp else '아이패드만', x,
              pc['u'].get(x), pc['gone'].get(x), ip['u'].get(x), ip['gone'].get(x)))
    gd = set(pc['gone']) ^ set(ip['gone'])
    print('  gone 이 다른 칸', sorted(gd)[:6])

    # 파이썬 규칙으로 §J 차례(아이패드 → PC → 아이패드 → PC · 모두 칩을 누른 것 = force) 를 돌린다
    devs = {}
    for name, rec in (('PC', pc), ('IP', ip)):
        devs[name] = {'data': copy.deepcopy(rec['data']), 'u': dict(rec['u']), 'gone': dict(rec['gone']),
                      'shadow': copy.deepcopy(rec['data'])}
    remote = {'v': 1, 'data': copy.deepcopy(ip['data']), 'u': dict(ip['u']), 'gone': dict(ip['gone'])}
    model_rows = []
    for step, name in (('아이패드1', 'IP'), ('PC1', 'PC'), ('아이패드2', 'IP'), ('PC2', 'PC')):
        py_merge(devs[name], remote, sk)
        remote = py_payload(devs[name], remote)
        model_rows.append([step, counts(remote['data'], sk)])
    want = {'pc': counts(devs['PC']['data'], sk), 'ipad': counts(devs['IP']['data'], sk)}
    print('파이썬 규칙 기대 — 원격 %s · 끝 PC %s · 끝 아이패드 %s  [정정칸·논리·단원기록·근거·연결·전체]' % (
        [r[1] for r in model_rows], want['pc'], want['ipad']))

    quiz = [{'id': u, 'q': '더미 지문 ' + u + ' 가나다라마바사', 'exp': '더미 해설 ' + u, 'a': 'O', 'subject': '민법총칙',
             'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'displayNo': i + 1, 'probNum': i + 1, 'subNum': '',
             'source': '변리사 20', 'pending': False, 'examMeta': [], 'caseText': '', 'stem': '', 'status': '', 'excelLogic': ''}
            for i, u in enumerate(['Q9901', 'Q9902', 'Q9903'])]
    P = {'syncKeys': sk, 'quiz': quiz,
         'real': {'pc': {'data': pc['data'], 'u': pc['u'], 'gone': pc['gone'], 'ms': ms(pc['savedAt'])},
                  'ip': {'data': ip['data'], 'u': ip['u'], 'gone': ip['gone'], 'ms': ms(ip['savedAt']), 'savedAt': ip['savedAt']},
                  'want': want}}
    js_json = lambda v: json.dumps(v, ensure_ascii=False).replace('</', '<\\/')
    tests = TESTS.replace('__P__', js_json(P))

    print()
    print('=== G12 소스 (NEW vs HEAD) ===')
    nbad = 0
    for h in ('function stampAll(', 'async function ghPutJson(', 'function recPending(', 'async function recForcePull(',
              'async function ghSha(', 'async function ghRaw('):
        same = fn_block(new, h) == fn_block(base, h)
        nbad += (not same)
        print('  %-30s %s' % (h, 'PASS 문자까지 같다' if same else 'FAIL 달라졌다'))
    ck_line = "        const ckey = (k, c) => k + '|' + c;\n"
    ok_ck = new.count(ck_line) == 1 and base.count(ck_line) == 1
    nbad += (not ok_ck)
    print('  %-30s %s' % ('const ckey', 'PASS 문자까지 같다' if ok_ck else 'FAIL'))
    sk_new = re.search(r"const SYNC_KEYS = (\[[^\]]*\]);", new).group(1)
    ok_sk = sk_new == re.search(r"const SYNC_KEYS = (\[[^\]]*\]);", base).group(1) and len(sk) == 17
    nbad += (not ok_sk)
    print('  %-30s %s' % ('SYNC_KEYS 17키', 'PASS 무변' if ok_sk else 'FAIL'))
    print('  G12 소스 : %s' % ('ALL OK' if not nbad else '%d개 어긋남' % nbad))
    print()

    res = {}
    for tag, src in (('NEW', new), ('HEAD', base)):
        lines = build_and_run(tag, src, SEED, tests)
        res[tag] = lines
        print('=== %s 판 ===' % tag)
        if lines is None:
            print('  결과 줄 없음 → %s' % os.path.join(OUT, 'dom_%s.html' % tag))
            continue
        for ln in lines:
            print('   ' + ln)
        print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
        print()

    def gate(lines, g):
        ls_ = [x for x in (lines or []) if x.startswith(('PASS', 'FAIL')) and x.split(' | ')[1].split(' ')[0] == g]
        return '%dP/%dF' % (sum(1 for x in ls_ if x.startswith('PASS')), sum(1 for x in ls_ if x.startswith('FAIL')))

    print('=== 헛잣대 표 — §K 일곱 게이트 (NEW / HEAD) ===')
    for g in BASELINE + ('G5-실물', 'G3-2', 'G4', 'G6', 'G8', 'G11', 'G12'):
        print('  %-8s NEW %-8s HEAD %s%s' % (g, gate(res.get('NEW'), g), gate(res.get('HEAD'), g), '   ← §K 헛잣대' if g in BASELINE else ''))
    nf = sum(1 for x in (res.get('NEW') or []) if x.startswith('FAIL'))
    ok = res.get('NEW') is not None and nf == 0 and not nbad
    print()
    print('종합 : %s' % ('ALL PASS' if ok else 'FAIL 있음'))
    return 0 if ok else 1


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=0;window.alert=function(){__ALERTS++;};window.confirm=function(){return true;};
window.__R={text:null,n:0,sha:null,puts:0,fail:false,rawDelay:0,rawHook:null};
window.fetch=function(url,opt){
 url=String(url);var m=(opt&&opt.method)||'GET';var h=(opt&&opt.headers)||{};var acc=String(h.Accept||'');
 var rec=url.indexOf('/contents/'+encodeURI('minbeop/기록.json'))>=0;
 function RS(st,b){return Promise.resolve(new Response(typeof b==='string'?b:JSON.stringify(b),{status:st,headers:{'Content-Type':'application/json'}}));}
 if(!rec)return RS(404,{message:'Not Found'});
 if(m==='GET'){
  if(!__R.text)return RS(404,{message:'Not Found'});
  if(acc.indexOf('raw')>=0){
   var t=__R.text;
   if(__R.rawHook){var f=__R.rawHook;__R.rawHook=null;try{f();}catch(e){}}
   if(__R.rawDelay>0){var d=__R.rawDelay;return new Promise(function(res){setTimeout(function(){res(new Response(t,{status:200}));},d);});}
   return RS(200,t);
  }
  return RS(200,{sha:__R.sha});
 }
 if(m==='PUT'){
  if(__R.fail)return RS(500,{message:'harness fail'});
  var body=JSON.parse(opt.body||'{}');
  if(__R.text&&body.sha!==__R.sha)return RS(409,{message:'conflict'});
  __R.text=decodeURIComponent(escape(atob(body.content)));__R.n++;__R.sha='sha-'+__R.n;__R.puts++;
  return RS(200,{content:{sha:__R.sha}});
 }
 return RS(404,{});
};
localStorage.clear();
</script>"""

TESTS = r"""<script>
window.onload=null;   /* 부팅(IndexedDB)은 끈다 — 검사가 syncRecords 를 직접 부른다 */
(function(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,320):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v===undefined?null:v));
const P=__P__;
const SK=P.syncKeys;
const BASE={'tt.cfg':JSON.stringify({token:'harness-token',person:'하네스'}),'ox_uid_migrated':'1','ox_gg_okreset':'1',
            'ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'};
const DEV={}; let CUR=null;
const dump=()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k);}return o;};
const load=o=>{localStorage.clear();for(const k in o)localStorage.setItem(k,o[k]);};
const use=(name,init)=>{ if(CUR) DEV[CUR]=dump(); load(init||DEV[name]); CUR=name; };
const mk=(data,u,gone,opts)=>{ opts=opts||{}; const o=Object.assign({},BASE);
  SK.forEach(k=>o[k]=JSON.stringify((data&&data[k])||{}));
  o.ox_sync_u=JSON.stringify(u||{}); o.ox_sync_gone=JSON.stringify(gone||{});
  const sh={}; SK.forEach(k=>sh[k]=(data&&data[k])||{}); o.ox_sync_shadow=JSON.stringify(sh);
  o.ox_sync_meta=JSON.stringify(opts.meta||{lastSync:0}); return o; };
const obj=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return {}}};
const remSet=r=>{ __R.n++; __R.text=r?JSON.stringify(r):null; __R.sha=r?('sha-'+__R.n):null; };
const remGet=()=>__R.text?JSON.parse(__R.text):null;
const nCells=d=>{ let n=0; SK.forEach(k=>n+=Object.keys((d&&d[k])||{}).length); return n; };
const localData=()=>{const d={};SK.forEach(k=>d[k]=obj(k));return d;};
const KC=['ox_q_fix','ox_q_logic','ox_chap_history','ox_q_geunge','ox_q_reflinks'];
const cnt=d=>KC.map(k=>Object.keys((d&&d[k])||{}).length).concat([nCells(d)]);
const chip=()=>(document.getElementById('rec-chip')||{}).textContent||'';
const showHome=()=>{ const h=document.getElementById('home-screen'), q=document.getElementById('quiz-screen'); if(h) h.classList.remove('hide'); if(q) q.classList.add('hide'); };
const dashFix=()=>{ const b=[...document.querySelectorAll('#dashboard-container button, #fix-chip-slot button')].find(x=>/✎ 정정/.test(x.textContent)); return b?b.textContent.trim():null; };   /* ★ 2026-10-06 (_task_ox_home_tidy §A-3 · §D 2) — 정정 칩이 빠른 실행 줄(#fix-chip-slot)로 옮겨 감 · 옛 자리(#dashboard-container)도 그대로 찾음 */
const hasFail=typeof recFail!=='undefined';
say('판 = '+(hasFail?'NEW(recFail 있음)':'HEAD'));

async function G1(){
  remSet({v:1,data:{ox_q_fix:{Q9001:{a:'X',done:false}}},u:{},gone:{}});
  use('g1', mk({}, {}, {}));
  await syncRecords();
  const f=obj('ox_q_fix'), u=obj('ox_sync_u');
  V('G1',{took:!!f.Q9001,stamp:u['ox_q_fix|Q9001']});
  T('G1 도장 없는 원격 칸 — 그 칸을 안 가진 기기가 병합하면 받는다', !!f.Q9001&&f.Q9001.a==='X', JSON.stringify(f));
  T('G1 받은 칸의 도장은 1', u['ox_q_fix|Q9001']===1, u['ox_q_fix|Q9001']);
}
async function G2(){
  remSet({v:1,data:{ox_q_fix:{Q9002:{a:'REMOTE'}}},u:{},gone:{}});
  use('g2', mk({ox_q_fix:{Q9002:{a:'MINE'}}}, {}, {}));
  await syncRecords(true);
  const f=obj('ox_q_fix'), r=remGet();
  T('G2 내가 이미 가진 칸 — 원격이 도장 없어도 내 값이 남는다', !!f.Q9002&&f.Q9002.a==='MINE', JSON.stringify(f.Q9002));
  T('G2 안 지워진다(민 원격에도 내 값)', !!(r&&r.data&&r.data.ox_q_fix&&r.data.ox_q_fix.Q9002&&r.data.ox_q_fix.Q9002.a==='MINE'), JSON.stringify(r&&r.data&&r.data.ox_q_fix));
}
async function G3(){
  const d={ox_q_fix:{Q9003:{a:'O'}}};
  remSet({v:1,data:d,u:{'ox_q_fix|Q9003':100},gone:{}});
  use('g3', mk(d, {'ox_q_fix|Q9003':100}, {}, {meta:{lastSync:100}}));
  __R.rawDelay=300;
  __R.rawHook=()=>setTimeout(()=>{ const f=obj('ox_q_fix'); f.Q9004={a:'내려받는 동안 적음'}; localStorage.setItem('ox_q_fix',JSON.stringify(f)); },60);
  const t0=Date.now();
  await syncRecords();
  const u=obj('ox_sync_u'), r=remGet();
  V('G3',{stamp:u['ox_q_fix|Q9004'],t0:t0,remote:!!(r&&r.data.ox_q_fix&&r.data.ox_q_fix.Q9004)});
  T('G3 ★ 내려받는 동안 쓴 칸 — 병합 뒤 stampAll 이 그 칸에 도장을 찍는다', (u['ox_q_fix|Q9004']||0)>=t0, 'u='+u['ox_q_fix|Q9004']);
  T('G3 그 칸이 도장과 함께 올라갔다(3분 타이머처럼 force 아님)', !!(r&&r.data.ox_q_fix&&r.data.ox_q_fix.Q9004&&r.u['ox_q_fix|Q9004']), JSON.stringify(r&&r.u));
}
async function G3b(){
  const d={ox_q_fix:{Q9005:{a:'v1'}}};
  remSet({v:1,data:d,u:{'ox_q_fix|Q9005':100},gone:{}});
  use('g3b', mk(d, {'ox_q_fix|Q9005':100}, {}, {meta:{lastSync:100}}));
  __R.rawDelay=300;
  __R.rawHook=()=>setTimeout(()=>{ const f=obj('ox_q_fix'); f.Q9005={a:'v2 내려받는 동안 고침'}; localStorage.setItem('ox_q_fix',JSON.stringify(f)); },60);
  const t0=Date.now();
  await syncRecords();
  const f=obj('ox_q_fix'), u=obj('ox_sync_u'), r=remGet();
  V('G3-2',{local:f.Q9005,stamp:u['ox_q_fix|Q9005'],remote:r&&r.data.ox_q_fix&&r.data.ox_q_fix.Q9005});
  T('G3-2 (더함) 내려받는 동안 고친 기존 칸 — 원격 옛 값이 덮지 않는다', !!f.Q9005&&f.Q9005.a.indexOf('v2')===0, JSON.stringify(f.Q9005));
  T('G3-2 그 칸에 도장이 찍히고 새 값이 올라간다', (u['ox_q_fix|Q9005']||0)>=t0&&!!r&&r.data.ox_q_fix.Q9005.a.indexOf('v2')===0, 'u='+u['ox_q_fix|Q9005']+' remote='+JSON.stringify(r&&r.data.ox_q_fix.Q9005));
}
async function G4(){
  remSet({v:1,data:{ox_q_fix:{R1:{a:'r'},S1:{a:'s-remote'}}},u:{'ox_q_fix|R1':500,'ox_q_fix|S1':200,'ox_future|X1':800,'ox_q_fix|N1':450},gone:{'ox_q_fix|G1':300,'ox_q_fix|C1':400}});
  use('g4', mk({ox_q_fix:{A1:{a:'a'},S1:{a:'s-mine'},C1:{a:'c'}}}, {'ox_q_fix|A1':600,'ox_q_fix|S1':700,'ox_q_fix|C1':350}, {'ox_q_fix|G2':650}));
  await syncRecords(true);
  const r=remGet()||{}, ru=r.u||{}, rg=r.gone||{};
  const wU={'ox_q_fix|A1':600,'ox_q_fix|S1':700,'ox_q_fix|R1':500,'ox_future|X1':800,'ox_q_fix|N1':450};
  const wG={'ox_q_fix|G1':300,'ox_q_fix|G2':650,'ox_q_fix|C1':400};
  const eq=(a,b)=>JSON.stringify(Object.keys(a).sort().map(k=>[k,a[k]]))===JSON.stringify(Object.keys(b).sort().map(k=>[k,b[k]]));
  V('G4',{u:ru,gone:rg});
  T('G4 민 뒤 원격 u = 양쪽 합집합 · 같은 칸은 큰 시각', eq(ru,wU), JSON.stringify(ru));
  T('G4 민 뒤 원격 gone = 양쪽 합집합', eq(rg,wG), JSON.stringify(rg));
  T('G4 한 칸이 u 와 gone 에 동시에 있지 않다', Object.keys(ru).every(k=>!(k in rg)), Object.keys(ru).filter(k=>k in rg).join(','));
}
async function G5(){
  const su={'ox_q_fix|S5':100};
  remSet(null);
  use('A5', mk({ox_q_fix:{S5:{a:'shared'},A5only:{a:'A만'}},ox_q_logic:{L5:'A 논리'}}, su, {}));   /* A 만 가진 도장 없는 칸 둘 */
  use('B5', mk({ox_q_fix:{S5:{a:'shared'},B5only:{a:'B만'}}}, su, {}));                              /* B 만 가진 도장 없는 칸 하나 */
  const rows=[];
  const step=async(dv,tag)=>{ use(dv); await syncRecords(true); const r=remGet(); rows.push([tag,r?nCells(r.data):0]); };
  await step('A5','A1'); await step('B5','B1'); await step('A5','A2'); await step('B5','B2'); await step('A5','A3'); await step('B5','B3');
  V('G5.rows',rows);
  const rc=rows.map(x=>x[1]);
  T('G5 A·B 를 번갈아 세 번 — 원격 칸 수가 한 번도 줄지 않는다', rc.every((v,i)=>i===0||v>=rc[i-1]), JSON.stringify(rc));
  use('A5'); const a=localData(); use('B5'); const b=localData();
  T('G5 끝에 두 기기 칸 수가 같고 서로의 칸을 가졌다', nCells(a)===nCells(b)&&!!a.ox_q_fix.B5only&&!!b.ox_q_fix.A5only&&!!b.ox_q_logic.L5, nCells(a)+' vs '+nCells(b));
}
async function G5real(){
  const pc=P.real.pc, ip=P.real.ip;
  remSet({v:1,savedAt:ip.savedAt,by:'알수없음',data:ip.data,u:ip.u,gone:ip.gone});
  use('PCr', mk(pc.data, pc.u, pc.gone, {meta:{lastSync:pc.ms}}));
  use('IPr', mk(ip.data, ip.u, ip.gone, {meta:{lastSync:ip.ms}}));
  const rows=[];
  const step=async(dv,tag)=>{ use(dv); await syncRecords(true); const r=remGet(); rows.push([tag,cnt(r&&r.data),cnt(localData())]); };
  await step('IPr','아이패드1'); await step('PCr','PC1'); await step('IPr','아이패드2'); await step('PCr','PC2');
  V('G5-실물.rows',rows);
  use('PCr'); const a=cnt(localData()); use('IPr'); const b=cnt(localData());
  V('G5-실물.final',{pc:a,ipad:b,want:P.real.want});
  T('G5-실물 §J 차례(아이패드→PC→아이패드→PC) 뒤 두 기기의 정정칸·논리·단원기록·근거·연결·전체가 같다', JSON.stringify(a)===JSON.stringify(b), JSON.stringify({pc:a,ipad:b}));
  T('G5-실물 그 수 = 파이썬이 따로 짠 합치기 규칙의 기대값', JSON.stringify(a)===JSON.stringify(P.real.want.pc)&&JSON.stringify(b)===JSON.stringify(P.real.want.ipad), JSON.stringify({got:{pc:a,ipad:b},want:P.real.want}));
  const tot=rows.map(x=>x[1][5]);
  T('G5-실물 원격 전체 칸 수가 한 번도 줄지 않는다', tot.every((v,i)=>i===0||v>=tot[i-1]), JSON.stringify(tot));
}
async function G6(){
  const d={ox_q_fix:{D6:{a:'지울 칸'},K6:{a:'남는 칸'}}}, u={'ox_q_fix|D6':100,'ox_q_fix|K6':100};
  remSet({v:1,data:d,u:u,gone:{}});
  use('A6', mk(d,u,{},{meta:{lastSync:100}}));
  use('B6', mk(d,u,{},{meta:{lastSync:100}}));
  use('A6'); const f=obj('ox_q_fix'); delete f.D6; localStorage.setItem('ox_q_fix',JSON.stringify(f));
  await syncRecords(true);
  use('B6'); await syncRecords(true);
  T('G6 A 에서 지운 칸이 B 로 건너가 지워진다', !obj('ox_q_fix').D6, JSON.stringify(obj('ox_q_fix')));
  use('A6'); await syncRecords(true); use('B6'); await syncRecords(true); use('A6'); await syncRecords(true);
  const r=remGet(), aF=obj('ox_q_fix'); use('B6'); const bF=obj('ox_q_fix');
  T('G6 그 뒤 A·B 를 돌려도 되살아나지 않는다(두 기기·원격 · 원격에 묘비)', !aF.D6&&!bF.D6&&!(r.data.ox_q_fix||{}).D6&&!!(r.gone||{})['ox_q_fix|D6'], JSON.stringify({a:Object.keys(aF),b:Object.keys(bF),r:Object.keys(r.data.ox_q_fix||{})}));
}
async function G7(){
  const d={ox_q_fix:{Q7001:{a:'old'}}}, u={'ox_q_fix|Q7001':100};
  remSet({v:1,data:d,u:u,gone:{}});
  use('A7', mk({ox_q_fix:{Q7001:{a:'old'},Q7002:{a:'도장 없이 생긴 칸'}}}, u, {}, {meta:{lastSync:200}}));   /* 그림자까지 새 칸을 가진 꼴(도장이 빠진 칸) */
  const p0=__R.puts;
  await syncRecords();
  const r=remGet();
  V('G7',{puts:__R.puts-p0});
  T('G7 도장 없이 바뀐 칸 — force 아닌 동기화(3분 타이머)에서도 올라간다', __R.puts>p0&&!!(r.data.ox_q_fix||{}).Q7002, 'puts='+(__R.puts-p0));
}
async function G8(){
  remSet({v:1,data:{},u:{},gone:{}});
  use('A8', mk({ox_q_fix:{Z1:{a:'묘비 있는 칸'},Z2:{a:'산 칸'}}}, {}, {'ox_q_fix|Z1':900,'ox_q_fix|Z9':800}));
  await recForcePush();
  const g=obj('ox_sync_gone'), u=obj('ox_sync_u'), r=remGet();
  T('G8 강제 올리기 — gone 이 안 비워진다', g['ox_q_fix|Z1']===900&&g['ox_q_fix|Z9']===800, JSON.stringify(g));
  T('G8 묘비 있는 칸에는 도장이 안 찍힌다 · 산 칸은 찍힌다', !('ox_q_fix|Z1' in u)&&!!u['ox_q_fix|Z2'], JSON.stringify(u));
  T('G8 민 원격에도 묘비가 남는다', !!(r&&r.gone&&r.gone['ox_q_fix|Z1']), JSON.stringify(r&&r.gone));
}
async function G9(){
  const d={ox_q_fix:{Q9101:{a:'O'}}}, u={'ox_q_fix|Q9101':100};
  remSet({v:1,data:d,u:u,gone:{}});
  use('A9', mk(d,u,{},{meta:{lastSync:Date.now()-5*3600*1000}}));
  const p0=__R.puts, a0=__ALERTS;
  await syncRecords();
  const c1=chip();
  V('G9.받기만',{chip:c1,puts:__R.puts-p0});
  T('G9 받기만 하고 안 올렸어도 「N분 전」이 갱신된다', __R.puts===p0&&/동기화됨 방금/.test(c1), c1+' · puts='+(__R.puts-p0));
  __R.fail=true;
  const f=obj('ox_q_fix'); f.Q9102={a:'새 칸'}; localStorage.setItem('ox_q_fix',JSON.stringify(f));
  await syncRecords(true);
  __R.fail=false;
  const c2=chip(), st=(document.getElementById('sync-status')||{}).textContent||'';
  V('G9.실패',{chip:c2,status:st});
  T('G9 PUT 을 실패시키면 칩이 실패라고 보인다', /실패/.test(c2), c2);
  T('G9 실패 까닭이 syncStatus 에 적힌다', /실패/.test(st), st);
  T('G9 alert 는 안 뜬다', __ALERTS===a0, __ALERTS-a0);
}
async function G10(){
  const d={ox_q_fix:{F1:{a:'O',done:false}}}, u={'ox_q_fix|F1':100};
  use('g10', mk(d,u,{},{meta:{lastSync:100}}));
  showHome(); quizData.length=0; P.quiz.forEach(q=>quizData.push(q));   /* 문항이 비면 대시보드가 다른 꼴로 그려져 정정 단추가 없다(첫 판 실측 null) */
  renderDashboard();
  const b0=dashFix();
  remSet({v:1,data:{ox_q_fix:{F1:{a:'O',done:false},F2:{a:'X',done:false}}},u:{'ox_q_fix|F1':100,'ox_q_fix|F2':500},gone:{}});
  await syncRecords();
  const b1=dashFix();
  V('G10',{before:b0,after:b1});
  T('G10 병합이 정정을 가져오면 「✎ 정정 N」이 새로고침 없이 바뀐다', b0==='✎ 정정 1'&&b1==='✎ 정정 2', JSON.stringify({before:b0,after:b1}));
}
async function G11(){
  const d={ox_q_fix:{F1:{a:'O',done:false}}}, u={'ox_q_fix|F1':100};
  use('g11', mk(d,u,{},{meta:{lastSync:100}}));
  quizData.length=0; P.quiz.forEach(q=>quizData.push(q));
  currentSubject='민법총칙'; currentChapterLabel='1. 총칙 > 1.1 민법의 법원'; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={};
  currentFilteredData=quizData.slice(0,2);
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  renderQuizPage();
  const uid=quizData[0].id, box0=document.getElementById('q-box-'+uid);
  const radio=document.querySelector('input[name="answer_'+uid+'"][value="O"]'); if(radio) radio.checked=true;
  remSet({v:1,data:{ox_q_fix:{F1:{a:'O',done:false},F3:{a:'X',done:false}}},u:{'ox_q_fix|F1':100,'ox_q_fix|F3':600},gone:{}});
  let calls=0; const _rd=window.renderDashboard; window.renderDashboard=function(){calls++; return _rd.apply(this,arguments);};
  try { await syncRecords(); } finally { window.renderDashboard=_rd; }
  const box1=document.getElementById('q-box-'+uid);
  T('G11 문항 풀던 중 병합이 와도 카드가 다시 안 그려진다(같은 노드 · 고른 답 그대로)', !!box0&&box1===box0&&!!radio&&radio.checked, 'same='+(box1===box0));
  T('G11 renderDashboard 가 안 불렸다', calls===0, calls);
  T('G11 (확인) 병합은 정정을 받았다', !!obj('ox_q_fix').F3);
  quizData.length=0; showHome();
}
async function G12(){
  remSet({v:1,data:{ox_q_fix:{Z12:{a:'O'}}},u:{'ox_q_fix|Z12':100},gone:{}});
  use('g12', mk({ox_q_fix:{Z12:{a:'O'},Z13:{a:'new'}}}, {'ox_q_fix|Z12':100}, {}));
  const k0=Object.keys(localStorage).sort();
  await syncRecords(true);
  const k1=Object.keys(localStorage).sort(), added=k1.filter(k=>k0.indexOf(k)<0), meta=obj('ox_sync_meta');
  V('G12',{added:added,meta:meta});
  T('G12 SYNC_KEYS 17키 무변', JSON.stringify(SYNC_KEYS)===JSON.stringify(P.syncKeys)&&SYNC_KEYS.length===17, SYNC_KEYS.length);
  T('G12 새 localStorage 키 0', added.length===0, added.join(','));
  T('G12 lastPush 는 ox_sync_meta 안의 칸이다', typeof meta.lastPush==='number'&&typeof meta.lastSync==='number', JSON.stringify(meta));
}

const LIST=[['G1',G1],['G2',G2],['G3',G3],['G3-2',G3b],['G4',G4],['G5',G5],['G5-실물',G5real],['G6',G6],['G7',G7],['G8',G8],['G9',G9],['G10',G10],['G11',G11],['G12',G12]];
setTimeout(async function(){
  for(const [n,f] of LIST){
    try{ __R.fail=false; __R.rawDelay=0; __R.rawHook=null; if(hasFail) recFail=''; recBusy=false; await f(); }
    catch(e){ T(n+' 하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' ')); }
  }
  const errs=(window.__ERR||[]);
  say('alert '+__ALERTS+'번 · 페이지 오류 '+errs.length+'건 : '+(errs.slice(0,3).join(' / ')||'없음'));
  const pre=document.createElement('pre'); pre.id='hz-out'; pre.textContent=R.join('\n'); document.documentElement.appendChild(pre);
},1500);
})();
</script>
"""

if __name__ == '__main__':
    sys.exit(main())
