# -*- coding: utf-8 -*-
"""세 앱 동기화 합치기 + 민법 근거 한도 검산 (minbeop/task/_task_ox_sync_and_limit.md §L).

한 페이지 안에서 기기 여럿을 흉내 낸다 — 기기 = localStorage 한 벌(자과앱은 + 메모리 전역 SYNC_REF).
원격 기록 파일은 fetch 흉내(메모리)다. 사람 기기의 기록·깃허브에는 쓰지 않는다(studyplandata 클론은 읽기만).
  판 NEW  = genie 작업트리
     HEAD = git HEAD (고치기 전 · 헛잣대)
     A32  = 민법OX a32e669 (지시서 §0 기준 판 877.81KB — 합치기 판 d418d9d 이전)
⚠ 앱 타이머(10초 도장·3분 동기화)는 끈다 — 검사가 syncRecords 를 직접 부른다(setInterval 을 비운다 · 민법은 onload 도 끈다).
⚠ 자과앱은 IndexedDB 열기를 멈춰 시동 IIFE 가 전역을 덮지 못하게 한다. recMerge 의 put('kv',…) 은 기록하는 가짜로 바꿔 부른 키·값을 잰다.
⚠ 민법 index.html 은 </body> 가 둘이다 — rindex 로 붙이고 결과는 documentElement 에 붙인다.

쓰기 : python _harness_sync_and_limit.py [앱…]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, datetime
sys.stdout.reconfigure(encoding='utf-8')

GENIE = _roots.genie()
SP = _roots.spd()
OUT = os.path.join(tempfile.gettempdir(), 'h_sync_limit')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
A32 = 'a32e669'
PC_REV, IP_REV = '14a2d899', '9a545651'
APPS = {
    'minbeop': {'rel': 'minbeop/index.html', 'path': 'minbeop/기록.json', 'ckey': "const ckey = (k, c) => k + '|' + c;"},
    'jo': {'rel': 'jo/index.html', 'path': 'jopangi/기록.json', 'ckey': "const ckey = (k, c) => k + '|' + c;"},
    'jagwa': {'rel': 'jagwa/index.html', 'path': 'phys/기록.json', 'ckey': "const ckey=(k,c)=>k+'|'+c;"},
}
FNS = ['function stampAll(', 'async function ghPutJson(']
BASELINE = ('G1', 'G2', 'G3', 'G4', 'G6', 'G8', 'G11', 'G13', 'G15', 'G16')
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G7-자동', 'G8', 'G9', 'G9-2', 'G10', 'G11', 'G12', 'G13', 'G14',
         'G15', 'G16', 'G17', 'G18', 'G19', 'G-실물']


def git(repo, *a):
    QC.sub('git:show-data' if repo == SP else 'git:show-app')   # 셈 — studyplandata = 데이터 · genie = 바탕 앱(gate 만)
    r = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false'] + list(a), capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def _rg_md5(t):
    """regress — 기준 칸 값(함수 글자)은 md5(16) 로 스냅샷"""
    return None if t is None else hashlib.md5(t.encode('utf-8')).hexdigest()[:16]


def fn_text(src, head):
    i = src.find(head)
    if i < 0:
        return None
    j = src.find('{', i)
    depth = 0
    for p in range(j, len(src)):
        ch = src[p]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return src[i:p + 1]
    return None


def sk_text(app, src):
    if app == 'minbeop':
        m = re.search(r"const SYNC_KEYS = \[[^\]]*\];", src)
        return m.group(0) if m else None
    if app == 'jo':
        i = src.find('const SYNC_KEYS = [')
        j = src.find('.map(k => REC_PRE + k);', i)
        return src[i:j] if i >= 0 and j > i else None
    m = re.search(r"const SYNC_KEYS=[^;]*;", src)
    return ('\n'.join(re.findall(r"SYNC_KEYS:\[[^\]]*\]", src)) + '\n' + m.group(0)) if m else None


def build_and_run(tag, src, seed, tests, budget=150000):
    QC.launch('new' if tag.endswith('_NEW') else 'base')   # 셈(§B-4)
    html = src.replace('\r\n', '\n')
    b = html.index('<body')
    bb = html.index('>', b) + 1
    html = html[:bb] + seed + html[bb:]
    e = html.rindex('</body>')
    html = html[:e] + tests + html[e:]
    app = os.path.join(OUT, 'app_%s.html' % tag)
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                        '--user-data-dir=' + prof, '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=%d' % budget, '--dump-dom', 'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=600)
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
    f = len(ls_) - p
    return '%dP/%dF' % (p, f)


def main():
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:] or list(APPS)
    ms = lambda iso: int(datetime.datetime.fromisoformat(iso.replace('Z', '+00:00')).timestamp() * 1000)
    if QC.GATE or 'minbeop' in only:   # regress — 민법 실물 기록 둘은 민법 판(G-실물)만 씀 → 자과 · jo 사슬은 안 읽음(git 0)
        pc, ip = json.loads(git(SP, 'show', PC_REV + ':minbeop/기록.json')), json.loads(git(SP, 'show', IP_REV + ':minbeop/기록.json'))
    quiz = [{'id': u, 'q': '더미 지문 ' + u + ' 가나다라마바사', 'exp': '더미 해설 ' + u, 'a': 'O', 'subject': '민법총칙',
             'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원', 'displayNo': i + 1, 'probNum': i + 1, 'subNum': '',
             'source': '변리사 20', 'pending': False, 'examMeta': [], 'caseText': '', 'stem': '', 'status': '', 'excelLogic': ''}
            for i, u in enumerate(['Q9901', 'Q9902', 'Q9903'])]
    js_json = lambda v: json.dumps(v, ensure_ascii=False).replace('</', '<\\/')
    results, srcrep = {}, []
    for app in only:
        cfg = APPS[app]
        rel = cfg['rel']
        new = io.open(os.path.join(GENIE, rel.replace('/', os.sep)), encoding='utf-8', newline='').read().replace('\r\n', '\n')
        if QC.GATE:
            head = git(GENIE, 'show', 'HEAD:' + rel)
            vers = [('NEW', new), ('HEAD', head)]
            if app == 'minbeop':
                vers.append(('A32', git(GENIE, 'show', A32 + ':' + rel)))
            for h in FNS:
                a, b = fn_text(new, h), fn_text(head, h)
                srcrep.append((app, h.strip('('), a is not None and a == b))
            srcrep.append((app, 'const ckey', new.count(cfg['ckey']) == 1 and head.count(cfg['ckey']) == 1))
            sa, sb = sk_text(app, new), sk_text(app, head)
            srcrep.append((app, 'SYNC_KEYS 정의', sa is not None and sa == sb))
        else:   # regress — HEAD 판(헛잣대 열) · A32 판 안 풂 · 안 띄움 · G19 소스 = 앞 인도판 스냅샷(md5 · 수)
            vers = [('NEW', new)]
            if not QC.SMOKE:   # smoke — G19 소스 대조는 smoke 칸이 아님(표도 안 찍고 종합 셈에도 안 듦)
                for h in FNS:
                    a = fn_text(new, h)
                    srcrep.append((app, h.strip('('), a is not None and QC.same('G19/%s/%s' % (app, h.strip('(')), _rg_md5(a))))
                srcrep.append((app, 'const ckey', new.count(cfg['ckey']) == 1 and QC.same('G19/%s/ckey' % app, new.count(cfg['ckey']))))
                sa = sk_text(app, new)
                srcrep.append((app, 'SYNC_KEYS 정의', sa is not None and QC.same('G19/%s/SYNC_KEYS' % app, _rg_md5(sa))))
        P = {'quiz': quiz} if app == 'minbeop' else {}
        if app == 'minbeop':
            P['real'] = {'pc': {'data': pc['data'], 'u': pc['u'], 'gone': pc['gone'], 'ms': ms(pc['savedAt'])},
                         'ip': {'data': ip['data'], 'u': ip['u'], 'gone': ip['gone'], 'ms': ms(ip['savedAt']), 'savedAt': ip['savedAt']}}
        seed = SEED.replace('__PATH__', cfg['path']).replace('__IDB__', IDB_STOP if app == 'jagwa' else '')
        tests = TESTS.replace('__APP__', app).replace('__P__', js_json(P))
        for tag, src in vers:
            lines = build_and_run(app + '_' + tag, src, seed, tests)
            if QC.SMOKE and lines:   # smoke — G2(도장 없는 원격 칸 병합) 줄만
                lines = [x for x in lines if gate_of(x) == 'G2']
            results[(app, tag)] = lines
            print('=== %s · %s 판 ===' % (app, tag))
            if lines is None:
                print('  결과 줄 없음 → %s' % os.path.join(OUT, 'dom_%s_%s.html' % (app, tag)))
                continue
            for ln in lines:
                print('   ' + ln)
            print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
            print()

    if not QC.SMOKE:   # smoke — G19 소스 표 안 찍음(smoke 칸 아님)
        if QC.GATE:
            print('=== G19 소스 — NEW 와 HEAD 가 문자까지 같아야 하는 것 ===')
        else:   # regress — 바탕(HEAD) 대신 기준 스냅샷(앞 인도판 · 글자 md5 · 수)
            print('=== G19 소스 — NEW 가 기준 스냅샷(앞 인도판 글자 md5 · ckey 수)과 같아야 하는 것 ===')
        for app, what, ok in srcrep:
            print('  %-8s %-24s %s' % (app, what, 'PASS 문자까지 같다' if ok else 'FAIL 달라졌다'))
        print()
    cols = [(a, t) for a in only for t in (('NEW', 'HEAD', 'A32') if a == 'minbeop' else ('NEW', 'HEAD'))]
    print('=== 게이트 표 (P/F) — ★ = §L 헛잣대 열 ===')
    print('  %-8s ' % '게이트' + ' '.join('%-12s' % ('%s·%s' % c) for c in cols))
    for g in GATES:
        print('  %-8s ' % (g + ('★' if g in BASELINE else '')) + ' '.join('%-12s' % tally(results.get(c), g) for c in cols))
    print()
    bad = [c for c in cols if c[1] == 'NEW' and (results.get(c) is None or any(x.startswith('FAIL') for x in results[c]))]
    nsrc = sum(1 for x in srcrep if not x[2])
    print('종합 : %s' % ('ALL PASS (NEW 판 FAIL 0 · 소스 대조 어긋남 0)' if not bad and not nsrc else 'FAIL 있음 — %s · 소스 어긋남 %d' % (bad, nsrc)))
    return 0 if not bad and not nsrc else 1


SEED = r"""<script>
window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});
window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});
window.__ALERTS=0;window.alert=function(){__ALERTS++;};window.confirm=function(){return true;};window.prompt=function(){return null;};
window.__WARN=[];(function(){var w=console.warn.bind(console);console.warn=function(){try{__WARN.push(Array.prototype.map.call(arguments,function(x){return typeof x==='string'?x:JSON.stringify(x)}).join(' '))}catch(e){}return w.apply(null,arguments);};})();
window.setInterval=function(){return 0;};
window.__PUTS=[];
window.__R={path:"__PATH__",text:null,n:0,sha:null,puts:0,fail:false,rawDelay:0,rawHook:null};
window.fetch=function(url,opt){
 url=String(url);var m=(opt&&opt.method)||'GET';var h=(opt&&opt.headers)||{};var acc=String(h.Accept||'');
 var rec=url.indexOf('/contents/'+encodeURI(__R.path))>=0;
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
__IDB__
localStorage.clear();
</script>"""

IDB_STOP = r"""try{indexedDB.open=function(){return {};};}catch(e){}   /* 자과앱 — 시동 IIFE 를 await open() 에 세워 둔다 */"""

TESTS = r"""<script>
window.onload=null;
(function(){
const APP="__APP__";
const P=__P__;
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,400):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v===undefined?null:v).slice(0,1500));
const J=v=>JSON.stringify(v);
const canon=v=>{ if(Array.isArray(v)) return '['+v.map(canon).join(',')+']'; if(v&&typeof v==='object') return '{'+Object.keys(v).sort().map(k=>J(k)+':'+canon(v[k])).join(',')+'}'; return J(v); };
const lsO=k=>{try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return {}}};
const TOK={'tt.cfg':JSON.stringify({token:'harness-token',person:'하네스'})};
let AD;
if(APP==='minbeop'){
  AD={U:U_KEY,G:GONE_KEY,S:SHADOW_KEY,M:SMETA_KEY,K:'ox_q_fix',K2:'ox_q_logic',H:'ox_chap_history',
      base:Object.assign({},TOK,{'ox_uid_migrated':'1','ox_gg_okreset':'1','ox_gg_memo_merged':'{"at":1,"moved":0,"links":0}','ox_auto_important_v2':'1'}),
      read:k=>lsO(k), write:(k,v)=>localStorage.setItem(k,J(v)),
      chip:()=>(document.getElementById('rec-chip')||{}).textContent||'', val:s=>({t:s})};
}else if(APP==='jo'){
  AD={U:SU_KEY,G:SG_KEY,S:SS_KEY,M:SM_KEY,K:REC_PRE+'ox',K2:REC_PRE+'sticker',H:REC_PRE+'rounds',EQ:EQ_KEY,
      base:Object.assign({},TOK),
      read:k=>JSON.parse(J(cellsOf(k))),
      write:(k,v)=>{ if(k===EQ_KEY) localStorage.setItem(k,J(Object.keys(v).map(x=>v[x]))); else localStorage.setItem(k,J(v)); try{recDropCache()}catch(e){} },
      chip:()=>(document.getElementById('syncChip')||{}).textContent||'', val:s=>({t:s})};
}else{
  AD={U:U_KEY,G:GONE_KEY,S:SHADOW_KEY,M:SMETA_KEY,K:'note',K2:'qtype',H:'status',
      base:Object.assign({},TOK),
      read:k=>JSON.parse(J(SYNC_REF[k].g()||{})),
      write:(k,v)=>SYNC_REF[k].s(JSON.parse(J(v))),
      chip:()=>(document.getElementById('recChip')||{}).textContent||'', val:s=>s};
  window.put=function(s,k,v){ __PUTS.push([s,k,JSON.stringify(v)]); return Promise.resolve(1); };
}
const K=AD.K, val=AD.val;
const lsDump=()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k);}return o;};
const DEV={}; let CURD=null;
const snap=()=>{const s={ls:lsDump()}; if(APP==='jagwa'){s.mem={};SYNC_KEYS.forEach(k=>s.mem[k]=J(SYNC_REF[k].g()||{}));} return s;};
const restore=s=>{ localStorage.clear(); for(const k in s.ls) localStorage.setItem(k,s.ls[k]);
  if(APP==='jagwa') SYNC_KEYS.forEach(k=>SYNC_REF[k].s(JSON.parse((s.mem&&s.mem[k])||'{}')));
  if(APP==='jo'){ try{recDropCache()}catch(e){} } };
const use=(name,init)=>{ if(CURD) DEV[CURD]=snap(); restore(init||DEV[name]); CURD=name; };
const fresh=(pairs)=>{ CURD=null; for(const n in pairs) DEV[n]=pairs[n]; };
const mk=(data,u,gone,opts)=>{ opts=opts||{}; const s={ls:Object.assign({},AD.base)}; const sh={};
  SYNC_KEYS.forEach(k=>{ const v=(data&&data[k])||{}; sh[k]=v;
    if(APP==='jagwa') return;
    if(APP==='jo'&&k===AD.EQ) s.ls[k]=J(Object.keys(v).map(x=>v[x])); else s.ls[k]=J(v); });
  if(APP==='jagwa'){ s.mem={}; SYNC_KEYS.forEach(k=>s.mem[k]=J((data&&data[k])||{})); }
  s.ls[AD.U]=J(u||{}); s.ls[AD.G]=J(gone||{}); s.ls[AD.S]=J(opts.shadow||sh); s.ls[AD.M]=J(opts.meta||{lastSync:0});
  return s; };
const rec=(data,u,gone)=>{ const d={}; for(const k in (data||{})){ const v=data[k]; d[k]=(APP==='jo'&&k===AD.EQ)?Object.keys(v).map(x=>v[x]):v; }
  return {v:1,savedAt:new Date().toISOString(),by:'하네스원격',data:d,u:u||{},gone:gone||{}}; };
const remSet=r=>{ __R.n++; __R.text=r?J(r):null; __R.sha=r?('sha-'+__R.n):null; };
const remGet=()=>__R.text?JSON.parse(__R.text):null;
const remData=(r,k)=>{ const v=((r&&r.data)||{})[k]; if(APP==='jo'&&k===AD.EQ){const o={};(Array.isArray(v)?v:[]).forEach(it=>{if(it&&it.k)o[it.k]=it});return o;} return v||{}; };
const nCells=d=>{let n=0;SYNC_KEYS.forEach(k=>{const v=(d||{})[k]; n+=Array.isArray(v)?v.length:Object.keys(v||{}).length;});return n;};
const localData=()=>{const d={};SYNC_KEYS.forEach(k=>d[k]=AD.read(k));return d;};
const tieNow=()=>{try{return typeof recTie!=='undefined'?recTie:null}catch(e){return null}};
const resetFlags=()=>{ try{recBusy=false}catch(e){} try{if(typeof recFail!=='undefined')recFail=''}catch(e){} try{if(typeof recErr!=='undefined')recErr=''}catch(e){} try{if(typeof recLastErr!=='undefined')recLastErr=''}catch(e){} };
const merge=async r=>await Promise.resolve(recMerge(r));

async function G1(){
  const uid='Q9901', text286=('메모에서 옮겨 온 긴 근거 가나다라마바사 ').repeat(20).slice(0,286);
  const g={k:'g_Q9901_x',i:1,t:text286,ok:null,ts:1,cs:[],src:'memo'};
  use('g1', mk({ox_q_geunge:{[uid]:[g]}}, {}, {}));
  let host=document.getElementById('hz-gg'); if(!host){ host=document.createElement('div'); host.id='hz-gg'; document.body.appendChild(host); }
  host.innerHTML=ggLineHTML(uid);
  ggToggle(uid,g.k); ggEdit(uid,g.k);
  const inp=document.getElementById('gg-ein-'+uid+'-'+g.k);
  const edited=text286+' — 고쳤다';
  inp.value=edited; ggEditSave(uid,g.k);
  const saved=(ggOf(uid)[0]||{}).t;
  V('G1',{GG_TMAX:typeof GG_TMAX!=='undefined'?GG_TMAX:null,GG_CMAX:typeof GG_CMAX!=='undefined'?GG_CMAX:null,before:text286.length,saved:(saved||'').length});
  T('G1 이관된 286자짜리를 열어 고치고 저장된다', saved===edited, '저장된 글 '+(saved||'').length+'자 (고친 글 '+edited.length+'자)');
  ggEdit(uid,g.k);
  const over='가'.repeat(4213);
  inp.value=over; ggEditSave(uid,g.k);
  const note=document.getElementById(inp.id+'-over');
  T('G1 한도를 넘기면 저장하지 않는다(값 무변)', (ggOf(uid)[0]||{}).t===edited, ((ggOf(uid)[0]||{}).t||'').length);
  T('G1 한도를 넘기면 몇 자인지 그 칸 아래에 보인다', !!note&&/4000자까지 · 지금 4213자/.test(note.textContent), note?note.textContent:'안내 없음');
  inp.value=edited; ggFit(inp);
  T('G1 한도 안으로 고치면 안내가 걷힌다', !document.getElementById(inp.id+'-over'));
  const cin=document.getElementById('gg-cin-'+uid+'-'+g.k); cin.value='나'.repeat(2001); ggReply(uid,g.k);
  const cn=document.getElementById(cin.id+'-over');
  T('G1 댓글 한도(2000)를 넘기면 몇 자인지 보인다', !!cn&&/2000자까지 · 지금 2001자/.test(cn.textContent), cn?cn.textContent:'안내 없음');
  const gin=document.getElementById('gg-in-'+uid); gin.value='다'.repeat(300); ggAdd(uid,false);
  T('G1 새 근거 300자(옛 한도 200 초과)가 저장된다', ggOf(uid).length===2&&(ggOf(uid)[1]||{}).t.length===300, ggOf(uid).length);
  host.innerHTML='';
}
async function G2(){
  remSet(rec({[K]:{c2:val('원격 도장 없음')}},{},{}));
  use('g2', mk({}, {}, {}));
  await syncRecords();
  const f=AD.read(K), u=lsO(AD.U);
  T('G2 도장 없는 원격 칸 — 그 칸을 안 가진 기기가 병합하면 받는다', J(f.c2)===J(val('원격 도장 없음')), J(f));
  T('G2 받은 칸의 도장은 1', u[K+'|c2']===1, u[K+'|c2']);
}
async function G3(){
  remSet(rec({[K]:{c3:val('원격 값')}},{},{}));
  use('g3', mk({[K]:{c3:val('내 값')}}, {}, {}));
  await syncRecords(true);
  const f=AD.read(K), r=remGet();
  T('G3 내가 이미 가진 칸 — 원격에 도장이 없어도 내 값이 남는다', J(f.c3)===J(val('내 값')), J(f.c3));
  T('G3 안 지워진다(민 원격에도 그 칸이 있다)', !!remData(r,K).c3, J(remData(r,K)));
}
async function G4(){
  const d={[K]:{a4:val('v1')}}, u={[K+'|a4']:100};
  remSet(rec({[K]:{a4:val('v1'),r4:val('원격이 새로 준 칸')}}, {[K+'|a4']:100,[K+'|r4']:300}, {}));
  use('g4', mk(d, u, {}, {meta:{lastSync:100}}));
  __R.rawDelay=300;
  __R.rawHook=()=>setTimeout(()=>{ const f=AD.read(K); f.n4=val('내려받는 동안 새로 적음'); f.a4=val('v2 내려받는 동안 고침'); AD.write(K,f); },60);
  const t0=Date.now();
  await syncRecords();
  const f=AD.read(K), uu=lsO(AD.U), r=remGet(), rd=remData(r,K);
  V('G4',{n4:uu[K+'|n4'],a4:uu[K+'|a4'],t0:t0,local:f});
  T('G4 ★ 내려받는 동안 새로 쓴 칸(같은 키에서 원격 칸을 받는 판) — 병합 뒤 stampAll 이 도장을 찍는다', (uu[K+'|n4']||0)>=t0, 'u='+uu[K+'|n4']);
  T('G4 ★ 내려받는 동안 고친 기존 칸 — 원격 옛 값이 덮지 않고 도장이 찍힌다', J(f.a4)===J(val('v2 내려받는 동안 고침'))&&(uu[K+'|a4']||0)>=t0, J(f.a4)+' u='+uu[K+'|a4']);
  T('G4 (확인) 같은 키의 원격 칸은 받았다', J(f.r4)===J(val('원격이 새로 준 칸')), J(f.r4));
  T('G4 두 칸이 도장과 함께 올라갔다(force 아님)', !!rd.n4&&J(rd.a4)===J(val('v2 내려받는 동안 고침'))&&!!((r&&r.u)||{})[K+'|n4'], J(rd));
}
async function G5(){
  try{ if(typeof recTie!=='undefined') recTie=0; }catch(e){}
  const d={[K]:{s5:val('같은 값')}}, u={[K+'|s5']:500};
  remSet(rec(d,u,{}));
  use('g5', mk(d,u,{},{meta:{lastSync:500}}));
  const before=J(localData()), w0=__WARN.length;
  const m=await merge(remGet());
  T('G5 동률·값 같음 — 아무것도 안 바뀐다', before===J(localData()));
  T('G5 took 0', !!m&&m.took===0, J(m));
  await syncRecords();
  T('G5 「동률」이 화면에 안 뜬다', !/동률/.test(AD.chip()), AD.chip());
  T('G5 동률 경고가 콘솔에 안 찍힌다', !__WARN.slice(w0).some(x=>/동률/.test(x)), J(__WARN.slice(w0)));
}
async function G6(){
  const long=val('긴 값 — 가나다라마바사아자차카타파하'), short=val('짧은 값');
  const u={[K+'|t6']:600};
  remSet(rec({[K]:{t6:short}},u,{}));
  use('g6', mk({[K]:{t6:long}}, u, {}, {meta:{lastSync:600}}));
  const w0=__WARN.length;
  await syncRecords();
  const f=AD.read(K), r=remGet();
  const warns=__WARN.slice(w0).filter(x=>/동률/.test(x));
  V('G6',{local:f.t6,remote:remData(r,K).t6,warn:warns,chip:AD.chip()});
  T('G6 동률·값 다름 — 긴 쪽이 남는다(내가 긴 쪽 · 원격이 짧은 쪽)', J(f.t6)===J(long), J(f.t6));
  T('G6 긴 쪽이 원격에도 올라간다(force 아님)', J(remData(r,K).t6)===J(long), J(remData(r,K).t6));
  T('G6 짧은 쪽은 콘솔에 칸 열쇠·길이와 함께 찍힌다', warns.length>0&&warns[0].indexOf(K+'|t6')>=0&&/\d+자/.test(warns[0])&&warns[0].indexOf(J(short))>=0, J(warns));
  T('G6 칩에 「동률 N건」이 보인다', /동률 \d+건/.test(AD.chip()), AD.chip());
  remSet(rec({[K]:{t7:long}},{[K+'|t7']:700},{}));
  use('g6b', mk({[K]:{t7:short}}, {[K+'|t7']:700}, {}, {meta:{lastSync:700}}));
  await syncRecords();
  T('G6 반대(원격이 긴 쪽) — 원격의 긴 값을 받는다', J(AD.read(K).t7)===J(long), J(AD.read(K).t7));
}
async function g7run(force){
  const long=val('A 의 값 — 더 길게 적은 글 가나다라마바'), short=val('B 의 값');
  const u={[K+'|w7']:700}, out={};
  for(const order of [['A','B'],['B','A']]){
    remSet(rec({},{},{}));
    fresh({A7:mk({[K]:{w7:long}},u,{},{meta:{lastSync:700}}), B7:mk({[K]:{w7:short}},u,{},{meta:{lastSync:700}})});
    const seqR=[];
    for(let i=0;i<3;i++) for(const dv of order){ use(dv+'7'); await syncRecords(force); seqR.push(J(remData(remGet(),K).w7)); }
    use('A7'); const fa=AD.read(K).w7; use('B7'); const fb=AD.read(K).w7;
    out[order.join('')]={a:fa,b:fb,r:remData(remGet(),K).w7,seqR:seqR};
  }
  return {out,long};
}
async function G7(){
  const {out,long}=await g7run(true);
  V('G7',out);
  T('G7 동률 양방향 — 어느 쪽에서 먼저 눌러도 결과가 같다', J(out.AB.a)===J(out.BA.a)&&J(out.AB.b)===J(out.BA.b)&&J(out.AB.r)===J(out.BA.r), J({AB:[out.AB.a,out.AB.b,out.AB.r],BA:[out.BA.a,out.BA.b,out.BA.r]}));
  T('G7 두 기기·원격이 같은 값(긴 쪽)에 닿는다', ['AB','BA'].every(o=>J(out[o].a)===J(long)&&J(out[o].b)===J(long)&&J(out[o].r)===J(long)), J(out));
  T('G7 세 번 왕복해도 원격 값이 안 튕긴다(두 번째 걸음부터 한 값)', ['AB','BA'].every(o=>out[o].seqR.slice(1).every(x=>x===out[o].seqR[out[o].seqR.length-1])), J({AB:out.AB.seqR,BA:out.BA.seqR}));
}
async function G7auto(){
  const {out,long}=await g7run(false);
  V('G7-자동',out);
  T('G7-자동 (더함) 칩을 안 누른 3분 동기화만으로도 두 기기·원격이 긴 쪽에 닿는다', ['AB','BA'].every(o=>J(out[o].a)===J(long)&&J(out[o].b)===J(long)&&J(out[o].r)===J(long)), J(out));
}
async function G8(){
  let longH, shortH, stamp;
  if(APP==='minbeop'){ const a1={score:5,total:6,date:'2026. 9. 1.'}, a2={score:6,total:6,date:'2026. 9. 14.'}; longH=[a1,a2]; shortH=[a2]; stamp=1789300000000; }
  else if(APP==='jo'){ const r1={ts:'2026-09-01T01:00:00.000Z',r:'O'}, r2={ts:'2026-09-14T01:00:00.000Z',r:'X'}; longH=[r1,r2]; shortH=[r2]; stamp=Date.parse(r2.ts); }
  else { longH={h:[{m:'O',t:1789000000000,s:5},{m:'X',t:1789300000000,s:4}]}; shortH={h:[{m:'X',t:1789300000000,s:4}]}; stamp=1789300000000; }
  const H=AD.H, u={[H+'|h8']:stamp};
  remSet(rec({[H]:{h8:shortH}},u,{}));
  use('g8a', mk({[H]:{h8:longH}},u,{},{meta:{lastSync:stamp}}));
  await syncRecords();
  const a=AD.read(H).h8, r=remGet();
  V('G8',{A:a,remote:remData(r,H).h8});
  T('G8 회독 이력 — 도장은 같고 A 가 한 줄 더 긴 칸: A 에서 병합해도 A 의 이력이 남는다', J(a)===J(longH), J(a));
  T('G8 A 의 긴 이력이 원격으로 올라간다(force 아님)', J(remData(r,H).h8)===J(longH), J(remData(r,H).h8));
  remSet(rec({[H]:{h8:longH}},u,{}));
  use('g8b', mk({[H]:{h8:shortH}},u,{},{meta:{lastSync:stamp}}));
  await syncRecords();
  T('G8 B(짧은 이력)에서 병합하면 A 의 긴 이력을 받는다', J(AD.read(H).h8)===J(longH), J(AD.read(H).h8));
}
async function G9(){
  remSet(rec({},{},{[K+'|d9']:900}));
  use('g9a', mk({[K]:{d9:val('지워질 칸')}}, {[K+'|d9']:900}, {}, {meta:{lastSync:900}}));
  await syncRecords(true);
  T('G9 원격 묘비와 내 도장이 같은 시각 — 묘비가 이긴다(지운다 · 무변)', !AD.read(K).d9, J(AD.read(K)));
  remSet(rec({[K]:{e9:val('원격 값')}}, {[K+'|e9']:950}, {[K+'|e9']:950}));
  use('g9b', mk({[K]:{e9:val('내 값')}}, {[K+'|e9']:500}, {}, {meta:{lastSync:500}}));
  await syncRecords(true);
  T('G9 원격에 같은 시각의 도장·묘비가 둘 다 — 묘비가 이긴다(무변)', !AD.read(K).e9, J(AD.read(K)));
  remSet(rec({[K]:{f9:val('원격이 아직 가진 값')}}, {[K+'|f9']:990}, {}));
  use('g9c', mk({}, {}, {[K+'|f9']:990}, {meta:{lastSync:990}}));
  await syncRecords(true);
  T('G9-2 (더함) 내 묘비와 원격 도장이 같은 시각 — 되살리지 않는다(원격 묘비와 같은 규칙 · 어느 쪽에서 먼저 눌러도 같게)', !AD.read(K).f9, J(AD.read(K)));
}
async function G10(){
  remSet(rec({[K]:{R1:val('r'),S1:val('s-remote')}},{[K+'|R1']:500,[K+'|S1']:200,'zz_future|X1':800,[K+'|N1']:450},{[K+'|G1']:300,[K+'|C1']:400}));
  use('g10', mk({[K]:{A1:val('a'),S1:val('s-mine'),C1:val('c')}},{[K+'|A1']:600,[K+'|S1']:700,[K+'|C1']:350},{[K+'|G2']:650}));
  await syncRecords(true);
  const r=remGet()||{}, ru=r.u||{}, rg=r.gone||{};
  const wU={[K+'|A1']:600,[K+'|S1']:700,[K+'|R1']:500,'zz_future|X1':800,[K+'|N1']:450};
  const wG={[K+'|G1']:300,[K+'|G2']:650,[K+'|C1']:400};
  const eq=(a,b)=>J(Object.keys(a).sort().map(k=>[k,a[k]]))===J(Object.keys(b).sort().map(k=>[k,b[k]]));
  V('G10',{u:ru,gone:rg});
  T('G10 민 뒤 원격 u = 양쪽 합집합 · 같은 칸은 큰 시각', eq(ru,wU), J(ru));
  T('G10 민 뒤 원격 gone = 양쪽 합집합', eq(rg,wG), J(rg));
  T('G10 한 칸이 u 와 gone 에 동시에 있지 않다', Object.keys(ru).every(k=>!(k in rg)), Object.keys(ru).filter(k=>k in rg).join(','));
}
async function G11(){
  const su={[K+'|S5']:100};
  remSet(null);
  fresh({A11:mk({[K]:{S5:val('shared'),A5only:val('A만')},[AD.K2]:{L5:val('A 두번째 키')}}, su, {}), B11:mk({[K]:{S5:val('shared'),B5only:val('B만')}}, su, {})});
  const rows=[];
  for(let i=0;i<3;i++) for(const dv of ['A11','B11']){ use(dv); await syncRecords(true); const r=remGet(); rows.push([dv+(i+1),r?nCells(r.data):0]); }
  V('G11.rows',rows);
  const rc=rows.map(x=>x[1]);
  T('G11 A·B 를 번갈아 세 번 — 원격 칸 수가 한 번도 줄지 않는다', rc.every((v,i)=>i===0||v>=rc[i-1]), J(rc));
  use('A11'); const a=localData(); use('B11'); const b=localData();
  T('G11 끝에 두 기기 칸 수가 같고 서로의 칸을 가졌다', nCells(a)===nCells(b)&&!!a[K].B5only&&!!b[K].A5only&&!!b[AD.K2].L5, nCells(a)+' vs '+nCells(b));
}
async function G12(){
  const d={[K]:{D6:val('지울 칸'),K6:val('남는 칸')}}, u={[K+'|D6']:100,[K+'|K6']:100};
  remSet(rec(d,u,{}));
  fresh({A12:mk(d,u,{},{meta:{lastSync:100}}), B12:mk(d,u,{},{meta:{lastSync:100}})});
  use('A12'); const f=AD.read(K); delete f.D6; AD.write(K,f);
  await syncRecords(true);
  use('B12'); await syncRecords(true);
  T('G12 A 에서 지운 칸이 B 로 건너가 지워진다', !AD.read(K).D6, J(AD.read(K)));
  use('A12'); await syncRecords(true); use('B12'); await syncRecords(true); use('A12'); await syncRecords(true);
  const r=remGet(), aF=AD.read(K); use('B12'); const bF=AD.read(K);
  T('G12 그 뒤 A·B 를 돌려도 되살아나지 않는다(두 기기·원격 · 원격에 묘비)', !aF.D6&&!bF.D6&&!remData(r,K).D6&&!!(r.gone||{})[K+'|D6'], J({a:Object.keys(aF),b:Object.keys(bF),r:Object.keys(remData(r,K))}));
}
async function G13(){
  const d={[K]:{Q7001:val('old')}}, u={[K+'|Q7001']:100};
  remSet(rec(d,u,{}));
  use('g13', mk({[K]:{Q7001:val('old'),Q7002:val('도장 없이 생긴 칸')}}, u, {}, {meta:{lastSync:200}}));
  const p0=__R.puts;
  await syncRecords();
  const r=remGet();
  T('G13 도장 없이 바뀐 칸 — force 아닌 동기화에서도 올라간다', __R.puts>p0&&!!remData(r,K).Q7002, 'puts='+(__R.puts-p0));
}
async function G14(){
  if(typeof recForcePush!=='function'){ say('G14 이 앱에는 강제 올리기가 없다 — 건너뜀'); return; }
  remSet(rec({},{},{}));
  use('g14', mk({[K]:{Z1:val('묘비 있는 칸'),Z2:val('산 칸')}}, {}, {[K+'|Z1']:900,[K+'|Z9']:800}));
  await recForcePush();
  const g=lsO(AD.G), u=lsO(AD.U), r=remGet();
  T('G14 강제 올리기 — gone 이 안 비워진다', g[K+'|Z1']===900&&g[K+'|Z9']===800, J(g));
  T('G14 묘비 있는 칸에는 도장이 안 찍힌다 · 산 칸은 찍힌다', !((K+'|Z1') in u)&&!!u[K+'|Z2'], J(u));
  T('G14 민 원격에도 묘비가 남는다', !!(r&&r.gone&&r.gone[K+'|Z1']), J(r&&r.gone));
}
async function G15(){
  const d={[K]:{Q9101:val('O')}}, u={[K+'|Q9101']:100};
  if(APP!=='jagwa'){
    remSet(rec(d,u,{}));
    use('g15', mk(d,u,{},{meta:{lastSync:Date.now()-5*3600*1000}}));
    const p0=__R.puts;
    recPaint(); const c0=AD.chip();
    await syncRecords();
    const c1=AD.chip();
    const hm=x=>(x.getHours()<10?'0':'')+x.getHours()+':'+(x.getMinutes()<10?'0':'')+x.getMinutes();
    const now=new Date();
    const freshChip = APP==='minbeop' ? /동기화됨 방금/.test(c1) : (c1.indexOf(hm(now))>=0||c1.indexOf(hm(new Date(now-60000)))>=0);
    V('G15.받기만',{before:c0,after:c1,puts:__R.puts-p0});
    T('G15 받기만 하고 안 올렸어도 칩의 「마지막으로 맞춘 시각」이 갱신된다', __R.puts===p0&&freshChip&&c1!==c0, c0+' → '+c1+' · puts='+(__R.puts-p0));
  } else say('G15 자과앱은 맞출 때마다 올린다 — 「받기만」 갈래가 없다(§G 는 민법·조판기 몫)');
  remSet(rec(d,u,{}));
  use('g15f', mk(d,u,{},{meta:{lastSync:100}}));
  const a0=__ALERTS;
  __R.fail=true;
  const f=AD.read(K); f.Q9102=val('새 칸'); AD.write(K,f);
  await syncRecords(true);
  __R.fail=false;
  const c2=AD.chip();
  V('G15.실패',{chip:c2});
  T('G15 PUT 을 실패시키면 칩이 실패라고 보인다', /실패/.test(c2), c2);
  T('G15 alert 는 안 뜬다', __ALERTS===a0, __ALERTS-a0);
}
const showHome=()=>{ const h=document.getElementById('home-screen'), q=document.getElementById('quiz-screen'); if(h) h.classList.remove('hide'); if(q) q.classList.add('hide'); };
const dashFix=()=>{ const b=[...document.querySelectorAll('#dashboard-container button, #fix-chip-slot button')].find(x=>/✎ 정정/.test(x.textContent)); return b?b.textContent.trim():null; };   /* ★ 2026-10-06 (_task_ox_home_tidy §A-3 · §D 2) — 정정 칩이 빠른 실행 줄(#fix-chip-slot)로 옮겨 감 · 옛 자리(#dashboard-container)도 그대로 찾음 */
async function G16(){
  const d={ox_q_fix:{F1:{a:'O',done:false}}}, u={'ox_q_fix|F1':100};
  use('g16', mk(d,u,{},{meta:{lastSync:100}}));
  showHome(); quizData.length=0; P.quiz.forEach(q=>quizData.push(q));
  renderDashboard();
  const b0=dashFix();
  remSet(rec({ox_q_fix:{F1:{a:'O',done:false},F2:{a:'X',done:false}}},{'ox_q_fix|F1':100,'ox_q_fix|F2':500},{}));
  await syncRecords();
  const b1=dashFix();
  V('G16',{before:b0,after:b1});
  T('G16 병합이 정정을 가져오면 「✎ 정정 N」이 새로고침 없이 바뀐다', b0==='✎ 정정 1'&&b1==='✎ 정정 2', J({before:b0,after:b1}));
}
async function G17(){
  const d={ox_q_fix:{F1:{a:'O',done:false}}}, u={'ox_q_fix|F1':100};
  use('g17', mk(d,u,{},{meta:{lastSync:100}}));
  quizData.length=0; P.quiz.forEach(q=>quizData.push(q));
  currentSubject='민법총칙'; currentChapterLabel='1. 총칙 > 1.1 민법의 법원'; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={};
  currentFilteredData=quizData.slice(0,2);
  document.getElementById('home-screen').classList.add('hide'); document.getElementById('quiz-screen').classList.remove('hide');
  renderQuizPage();
  const uid=quizData[0].id, box0=document.getElementById('q-box-'+uid);
  const radio=document.querySelector('input[name="answer_'+uid+'"][value="O"]'); if(radio) radio.checked=true;
  remSet(rec({ox_q_fix:{F1:{a:'O',done:false},F3:{a:'X',done:false}}},{'ox_q_fix|F1':100,'ox_q_fix|F3':600},{}));
  let calls=0; const _rd=window.renderDashboard; window.renderDashboard=function(){calls++; return _rd.apply(this,arguments);};
  try { await syncRecords(); } finally { window.renderDashboard=_rd; }
  const box1=document.getElementById('q-box-'+uid);
  T('G17 문항 풀던 중 병합이 와도 카드가 다시 안 그려진다(같은 노드 · 고른 답 그대로)', !!box0&&box1===box0&&!!radio&&radio.checked, 'same='+(box1===box0));
  T('G17 renderDashboard 가 안 불렸다', calls===0, calls);
  T('G17 (확인) 병합은 정정을 받았다', !!lsO('ox_q_fix').F3);
  quizData.length=0; showHome();
}
async function G18jo(){
  const EQ=AD.EQ;
  const it=(k,at,note)=>({k:k,at:at,who:'하네스',target:'jo|특허|1',part:'본문',file:'',quote:'',kind:'오타',note:note,st:'대기'});
  const u={[EQ+'|e1']:100,[EQ+'|e2']:100};
  remSet(rec({[EQ]:{e2:it('e2','2026-09-02T00:00:00Z','남는 항목 — 원격이 더 길게 고친 글'),e3:it('e3','2026-09-03T00:00:00Z','원격 새 항목')}}, {[EQ+'|e2']:100,[EQ+'|e3']:300}, {[EQ+'|e1']:200}));
  use('g18', mk({[EQ]:{e1:it('e1','2026-09-01T00:00:00Z','지울 항목'),e2:it('e2','2026-09-02T00:00:00Z','남는 항목')}}, u, {}, {meta:{lastSync:100}}));
  await syncRecords();
  let arr=null; try{ arr=JSON.parse(localStorage.getItem(EQ)||'null'); }catch(e){}
  const ks=Array.isArray(arr)?arr.map(x=>x.k):null;
  T('G18 조판기 editq — 저장 꼴이 배열 그대로다', Array.isArray(arr), typeof arr);
  T('G18 원격 묘비 e1 은 지워지고 새 항목 e3 은 받는다', !!ks&&ks.indexOf('e1')<0&&ks.indexOf('e3')>=0, J(ks));
  T('G18 도장이 같은 e2 — 긴 쪽(원격이 고친 글)이 남는다', !!arr&&((arr.find(x=>x.k==='e2')||{}).note==='남는 항목 — 원격이 더 길게 고친 글'), J(arr&&arr.find(x=>x.k==='e2')));
  T('G18 배열은 at 내림차순 그대로', !!ks&&J(ks)===J(['e3','e2']), J(ks));
  const r=remGet();
  T('G18 민 원격 data 의 editq 도 배열', Array.isArray(r&&r.data&&r.data[EQ]), typeof (r&&r.data&&r.data[EQ]));
  T('G18 수정 큐 캐시(eqAll)가 새 배열을 본다', typeof eqAll==='function'&&!!ks&&eqAll().map(x=>x.k).join(',')===ks.join(','), typeof eqAll==='function'?eqAll().map(x=>x.k).join(','):'없음');
}
async function G18ja(){
  __PUTS.length=0;
  const d={note:{'5':'내 코멘트'},status:{'5':{h:[{m:'O',t:1000,s:3}]}}}, u={'note|5':1000,'status|5':1000};
  remSet(rec({note:{'5':'내 코멘트','6':'원격 새 코멘트'},status:{'5':{h:[{m:'O',t:1000,s:3}]}}}, {'note|5':1000,'note|6':2000,'status|5':1000}, {}));
  use('g18ja', mk(d,u,{},{meta:{lastSync:1000}}));
  await syncRecords();
  const kv=__PUTS.filter(x=>x[0]==='kv').map(x=>x[1]);
  const np=__PUTS.find(x=>x[0]==='kv'&&x[1]==='note');
  V('G18',{puts:__PUTS.map(x=>[x[0],x[1],x[2].slice(0,80)])});
  T('G18 자과앱 dirty — 받은 키(note)만 IndexedDB 에 쓴다(status 는 안 쓴다)', J(kv)===J(['note']), J(kv));
  T('G18 IndexedDB 에 쓴 값에 받은 칸이 들어 있다', !!np&&JSON.parse(np[2])['6']==='원격 새 코멘트', np?np[2]:'없음');
  T('G18 메모리 전역(SYNC_REF.note)도 받은 칸을 가졌다', (SYNC_REF.note.g()||{})['6']==='원격 새 코멘트', J(SYNC_REF.note.g()));
  const sh=lsO(AD.S), uu=lsO(AD.U);
  T('G18 그림자에 받은 칸이 들어갔다(다음 stampAll 이 오인하지 않는다)', (sh.note||{})['6']==='원격 새 코멘트', J(sh.note));
  T('G18 받은 칸 도장 = 원격 도장(새로 찍히지 않았다)', uu['note|6']===2000, uu['note|6']);
}
async function G19(){
  V('SYNC_KEYS', SYNC_KEYS.length);
  remSet(rec({[K]:{z19:val('O')}},{[K+'|z19']:100},{}));
  use('g19', mk({[K]:{z19:val('O'),z20:val('new')}}, {[K+'|z19']:100}, {}));
  const k0=Object.keys(localStorage).sort();
  await syncRecords(true);
  const k1=Object.keys(localStorage).sort(), added=k1.filter(k=>k0.indexOf(k)<0), meta=lsO(AD.M);
  V('G19',{added:added,meta:meta});
  T('G19 새 localStorage 키 0', added.length===0, added.join(','));
  if(APP!=='jagwa') T('G19 lastPush 는 SMETA 안의 칸이다', typeof meta.lastPush==='number'&&typeof meta.lastSync==='number', J(meta));
}
async function Greal(){
  const pc=P.real.pc, ip=P.real.ip;
  remSet({v:1,savedAt:ip.savedAt,by:'알수없음',data:ip.data,u:ip.u,gone:ip.gone});
  fresh({PCr:mk(pc.data,pc.u,pc.gone,{meta:{lastSync:pc.ms}}), IPr:mk(ip.data,ip.u,ip.gone,{meta:{lastSync:ip.ms}})});
  const t0=tieNow()||0, w0=__WARN.length, rows=[];
  for(const [dv,tag] of [['IPr','아이패드1'],['PCr','PC1'],['IPr','아이패드2'],['PCr','PC2']]){ use(dv); await syncRecords(true); rows.push([tag,nCells((remGet()||{}).data)]); }
  use('PCr'); const a=localData(); use('IPr'); const b=localData();
  const ties=__WARN.slice(w0).filter(x=>/동률/.test(x)).map(x=>x.slice(0,160));
  V('G-실물',{rows:rows,tie:(tieNow()||0)-t0,ties:ties,pc:nCells(a),ipad:nCells(b)});
  T('G-실물 09-15 10:15(PC)·10:21(아이패드) 두 판을 §K 차례로 돌리면 두 기기 기록이 글자까지 같다', canon(a)===canon(b), nCells(a)+' vs '+nCells(b));
  const tot=rows.map(x=>x[1]);
  T('G-실물 원격 칸 수가 한 번도 줄지 않는다', tot.every((v,i)=>i===0||v>=tot[i-1]), J(tot));
}

const LIST=[];
const add=(n,f,apps)=>{ if(!apps||apps.indexOf(APP)>=0) LIST.push([n,f]); };
add('G1',G1,['minbeop']); add('G2',G2); add('G3',G3); add('G4',G4); add('G5',G5); add('G6',G6); add('G7',G7); add('G7-자동',G7auto);
add('G8',G8); add('G9',G9); add('G10',G10); add('G11',G11); add('G12',G12); add('G13',G13); add('G14',G14,['minbeop','jo']); add('G15',G15);
add('G16',G16,['minbeop']); add('G17',G17,['minbeop']); add('G18',G18jo,['jo']); add('G18',G18ja,['jagwa']); add('G19',G19); add('G-실물',Greal,['minbeop']);
setTimeout(async function(){
  say('판 = '+APP+' · SYNC_KEYS '+SYNC_KEYS.length+' · recTie '+(tieNow()===null?'없음(옛 판)':'있음'));
  for(const [n,f] of LIST){
    try{ __R.fail=false; __R.rawDelay=0; __R.rawHook=null; resetFlags(); await f(); }
    catch(e){ T(n+' 하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' ')); }
  }
  const errs=(window.__ERR||[]);
  say('alert '+__ALERTS+'번 · 페이지 오류 '+errs.length+'건 : '+(errs.slice(0,4).join(' / ')||'없음'));
  const pre=document.createElement('pre'); pre.id='hz-out'; pre.textContent=R.join('\n'); document.documentElement.appendChild(pre);
},1500);
})();
</script>
"""

if __name__ == '__main__':
    sys.exit(main())
