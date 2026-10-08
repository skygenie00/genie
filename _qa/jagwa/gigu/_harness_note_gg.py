# -*- coding: utf-8 -*-
"""자과앱 add7 묶음 「N — 코멘트」 — 잃은 물리 코멘트 31개 되살림 · 원인 막기.

    PYTHONIOENCODING=utf-8 python _harness_note_gg.py

  N-1  되살림 — 재료 31건이 근거 통에 **글자까지 같게** 한 줄씩 · ts = 재료 도장
  N-2  멱등 — 두 번 돌려 +0 · 기기 둘 흉내(각자 복구 → 세포 병합) 뒤에도 31줄
  N-3  올린 기록 흉내 — data.gg 31통 · data.note 0 · gone 의 note| 31 그대로
  N-4  재현(§B-3) — 가드 전에는 `ggEatNotes` 가 한 글자도 안 건드린다 ·
       가드가 풀리면 코멘트 0 · 근거 3 (헛잣대 = 고침 전 판은 코멘트 0 · 근거 0)
  N-5  다른 키 무변 — status·qtype·twin·frm·maskpos·omrpos·mcard
  N-6  오프라인에서도 되살림이 돈다(가드는 IndexedDB 만 본다 · add7 §D)

⚠ 픽셀 게이트는 안 쓴다(CLAUDE.md). 재는 것은 **통 안의 글자와 수**다.
⚠ 진짜 網을 막는다 — 같은 출처 밖 fetch 는 전부 거절한다.
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import hashlib
import http.server
import io
import json
import os
import shutil
import socketserver
import subprocess
import threading
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')
MAT = os.path.join(HERE, '_phys_note_복구_f6cee06.json')
OUT = os.path.join(os.environ.get('TEMP', '.'), 'hnotegg')
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_MD5 = 'cc835f04b02e9408cf46d85ef9f39de2'      # 고침 전(add6 앞) 판 — 헛잣대
BASE = os.path.join(OUT, '_base.html')


def _ensure_base():
    if os.path.isfile(BASE):
        b = open(BASE, 'rb').read()
        if hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            return BASE
    revs = subprocess.run(['git', '-C', GENIE, 'log', '--format=%H', '-400', '--', 'jagwa/index.html'],   # ★ 10/8 jagwa_ink_sync — 40 창은 새 판 커밋으로 사본이 41 번째로 밀려 죽었다(옛 줄: '-40')
                          capture_output=True, encoding='utf-8').stdout.split()
    for rev in revs:
        b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'],
                           capture_output=True).stdout
        if b and hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest() == BASE_MD5:
            open(BASE, 'wb').write(b)
            print('[base] git %s 에서 꺼냈다' % rev[:7])
            return BASE
    raise SystemExit('NG  고침 전 사본(md5 %s)을 못 찾았다' % BASE_MD5)


if QC.GATE:   # regress — 고침 전 사본 찾기(git log -40 · git show) 0 · 그 사본은 N-4 소스 헛잣대에만 쓴다(gate)
    _ensure_base()
MATJ = json.load(io.open(MAT, encoding='utf-8'))

STUB = """<script>try{localStorage.setItem('subj','phys')}catch(e){}</script>
<script>
window.katex={render:function(){},renderToString:function(s){return s}};
window.renderMathInElement=function(){};
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
</script>
"""

PROBE = r"""<script>
(function(){
 const R=[]; const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+' | '+JSON.stringify(i===undefined?null:i));
 const MAT=__MAT__;
 /* 진짜 網 막기 — 같은 출처만 통과(GitHub 은 통째로 거절 = 오프라인 흉내) */
 const __nf=window.fetch.bind(window);
 window.fetch=async function(u,o){const s=String(u);
   if(/^https?:/i.test(s)&&s.indexOf(location.origin)!==0)
     return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
   return __nf(u,o)};
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const until=async(fn,ms)=>{const t0=Date.now();
   while(Date.now()-t0<(ms||12000)){try{if(fn())return true}catch(e){}await wait(60)}return false};
 const NEW=(typeof ggRestoreNotes_f6cee06==='function');

 async function go(){
  try{
   await until(()=>typeof DATA!=='undefined'&&DATA.length>0,15000);
   await until(()=>typeof GG_READY!=='undefined'&&GG_READY,15000);
   R.push('NOTE | 진단 | '+JSON.stringify({SHELL:(typeof SHELL!=='undefined')?SHELL:'?',
     SUBJ:(typeof SUBJ_ID!=='undefined')?SUBJ_ID:'?',
     READY:(typeof GG_READY!=='undefined')?GG_READY:'?',
     HASBOOK:(typeof HASBOOK!=='undefined')?HASBOOK:'?',
     DATA:(typeof DATA!=='undefined')?DATA.length:'?',
     getT:(typeof get==='function')?'fn':'?',
     GGn:(typeof GG!=='undefined')?Object.keys(GG).length:'?',
     CMTn:(typeof CMT!=='undefined')?Object.keys(CMT).length:'?'}));
   if(typeof get==='function'){
     let r1='?';try{const v=await Promise.race([get('kv','gg'),new Promise(z=>setTimeout(()=>z('TIMEOUT'),4000))]);
       r1=(v==='TIMEOUT')?'TIMEOUT':('ok '+JSON.stringify(v).slice(0,40))}catch(e){r1='throw '+e}
     R.push('NOTE | get(kv,gg) | '+JSON.stringify(r1));
     R.push('NOTE | get 정체 | '+JSON.stringify(String(get).slice(0,110)));
     R.push('NOTE | db | '+JSON.stringify(typeof db==='undefined'?'undef':String(!!db)));
     R.push('NOTE | tx 정체 | '+JSON.stringify(String(tx).slice(0,130)));
     R.push('NOTE | stores | '+JSON.stringify([...(db.objectStoreNames||[])]));
     try{const o=db.transaction('kv','readonly').objectStore('kv');
       R.push('NOTE | 직접 store | '+JSON.stringify(String(o&&o.name)));}catch(e){R.push('NOTE | 직접 store | '+JSON.stringify('throw '+e))}
   }
   await wait(600);

   /* ── N-1 되살림 ─────────────────────────────────────────── */
   if(!NEW){
     T('N-1 되살림 — 근거 통 31곳',false,'ggRestoreNotes_f6cee06 없음 — 고침 전 판');
     T('N-2 멱등 +0',false,'같음');
     T('N-3 올린 기록 흉내',false,'같음');
   } else {
     const nos=Object.keys(MAT.note);
     const badT=[],badS=[];
     nos.forEach(no=>{
       const r=rec(+no); const uid=r?GGU(r):'';
       const list=uid?ggOf(uid):[];
       const hit=list.filter(g=>String(g.t||'')===String(MAT.note[no]));
       if(hit.length!==1){badT.push([no,uid,hit.length,list.length]);return}
       const want=MAT.u['note|'+no];
       if(want&&hit[0].ts!==want)badS.push([no,hit[0].ts,want]);
     });
     T('N-1 되살림 — 31곳에 재료 글자가 한 줄씩(문자까지)',badT.length===0,badT.slice(0,4));
     T('N-1 ts = 재료 도장',badS.length===0,badS.slice(0,4));
     T('N-1 src 는 note',nos.every(no=>{const r=rec(+no);const l=r?ggOf(GGU(r)):[];
       return l.some(g=>String(g.t||'')===String(MAT.note[no])&&g.src==='note')}),'');
     /* ── N-2 멱등 · 기기 둘 흉내 ──────────────────────────── */
     const before=JSON.stringify(GG);
     const n2=await ggRestoreNotes_f6cee06();
     T('N-2 두 번 돌려 +0',n2===0&&JSON.stringify(GG)===before,[n2]);
     /* 기기 둘 흉내 — 다른 기기가 제 열쇠로 넣은 줄을 세포 하나에 얹고 다시 돌린다 */
     { const no='9', r=rec(9), uid=GGU(r);
       const other=ggOf(uid).map(g=>Object.assign({},g,{k:'g_other'}));
       GG[uid]=other;                                   /* 원격이 이긴 셈 */
       const n3=await ggRestoreNotes_f6cee06();
       const l=ggOf(uid).filter(g=>String(g.t||'')===String(MAT.note[no]));
       T('N-2 기기 둘이 같이 돌려도 31줄이 62줄이 안 된다',n3===0&&l.length===1,[n3,l.length]); }
     /* ── N-3 올린 기록 흉내 ─────────────────────────────────
        찬 시동이라 묘비가 없다 — 사용자 상태를 흉내 내어 31개를 심고
        **되살림이 그것을 안 건드리는지**(§A-3) 본다. */
     { const g0={};Object.keys(MAT.note).forEach(no=>{g0['note|'+no]=MAT.u['note|'+no]||1});
       localStorage.setItem(GONE_KEY,JSON.stringify(g0));
       await ggRestoreNotes_f6cee06();
       let gone={};try{gone=JSON.parse(localStorage.getItem(GONE_KEY)||'{}')}catch(e){}
       const payload={};SYNC_KEYS.forEach(k=>{const v=SYNC_REF[k].g();if(v)payload[k]=v});
       const nGG=Object.keys(payload.gg||{}).length;
       const nNote=Object.keys(payload.note||{}).length;
       const nGone=Object.keys(gone).filter(k=>k.indexOf('note|')===0).length;
       T('N-3 올린 기록 — data.gg 31통',nGG===31,nGG);
       T('N-3 올린 기록 — data.note 0',nNote===0,nNote);
       T('N-3 묘비 note| 31 그대로',nGone===31,nGone); }
   }

   /* ── N-4 재현(§B-3) ──────────────────────────────────────── */
   { const R0=rec(7), R1=rec(8), R2=rec(11);
     const U0=GGU(R0),U1=GGU(R1),U2=GGU(R2);
     [U0,U1,U2].forEach(u=>{delete GG[u]});
     CMT[7]='흉내 코멘트 가';CMT[8]='흉내 코멘트 나';CMT[11]='흉내 코멘트 다';
     const snap=JSON.stringify(GG);
     /* ⓐ 가드 전 — `GG` 가 빈 통인 채로 흡수가 돌면 어떻게 되나 */
     const keep=GG_READY; GG_READY=false; const gkeep=GG; GG={};
     const n0=await ggEatNotes();
     const cmtLeft=[7,8,11].filter(x=>CMT[x]).length;
     /* 늦게 오는 읽기가 통을 되덮는다(2026-09-20 19:57 에 일어난 일) */
     GG=gkeep; GG_READY=keep;
     const gg0=[U0,U1,U2].reduce((a,u)=>a+ggOf(u).length,0);
     T('N-4 가드 전에는 코멘트를 안 지운다',cmtLeft===3,[n0,cmtLeft]);
     T('N-4 헛잣대 — 가드 전에 지우면 근거가 0 이 된다(고침 전 판의 일)',gg0===0,gg0);
     /* ⓑ 가드 뒤 — 코멘트 0 · 근거 3 */
     const n1=await ggEatNotes();
     const cmtLeft2=[7,8,11].filter(x=>CMT[x]).length;
     const gg1=[U0,U1,U2].reduce((a,u)=>a+ggOf(u).length,0);
     T('N-4 가드 뒤 — 코멘트 0 · 근거 3',cmtLeft2===0&&gg1===3,[n1,cmtLeft2,gg1]);
     T('N-4 옮긴 줄에 src:note',[U0,U1,U2].every(u=>ggOf(u).every(g=>g.src==='note')),'');
     /* 되돌린다 — 다른 잣대에 안 섞이게 */
     [U0,U1,U2].forEach(u=>{delete GG[u]}); JSON.parse(snap); }

   /* ── N-5 다른 키 무변 ───────────────────────────────────── */
   { const keys=['status','qtype','twin','frm','maskpos','omrpos','mcard'];
     const got={};keys.forEach(k=>{const v=(SYNC_REF[k]||{g:()=>null}).g();
       got[k]=v?Object.keys(v).length:-1});
     T('N-5 다른 키를 안 건드렸다(통이 열려 있고 셈이 난다)',
       keys.every(k=>got[k]>=0),got); }

   /* ── N-6 오프라인에서도 되살림이 돈다 ───────────────────── */
   T('N-6 밖 網 없이도 가드가 풀리고 되살림이 돈다',
     (typeof GG_READY!=='undefined')&&GG_READY===true,GG_READY);

   /* 1.2초 타이머가 없어졌는가(소스) — 파이썬이 따로 잰다 */
  }catch(e){R.push('FAIL | 묶음 예외 | '+JSON.stringify(String(e&&e.stack||e).slice(0,300)))}
  R.push('NOTE | err | '+JSON.stringify((window.__err||[]).slice(0,4)));
  try{await __nf('/done',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 if(document.readyState==='complete')setTimeout(go,900);
 else window.addEventListener('load',()=>setTimeout(go,900));
})();
</script>"""


def build(src_path, tag):
    html = io.open(src_path, encoding='utf-8', newline='').read()
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js',
                        STUB + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    probe = (PROBE if not QC.SMOKE else _rg_smoke_probe(PROBE)).replace('__MAT__', json.dumps(MATJ, ensure_ascii=False))   # smoke — 쪽 안 시험 글을 이 자리에서만 잘라 씀
    io.open(os.path.join(OUT, 'app_%s.html' % tag), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', probe + '</body>', 1))


def run(src_path, tag, secs=120):
    build(src_path, tag)
    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            box['txt'] = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers(); done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + tag); shutil.rmtree(prof, ignore_errors=True)
    QC.launch('new')   # 셈(§B-4) — 새 판 크롬 한 번(바탕은 본디 안 띄운다)
    t0 = time.time()
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1500,950',
                          'http://127.0.0.1:%d/app_%s.html' % (port, tag)],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs)
    p.terminate()
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (tag, time.time() - t0))
    if not got:
        return ['FAIL | %s 가 시간 안에 안 끝났다 | null' % tag]
    return [x for x in box['txt'].split('\n') if x.strip()]


def static():
    s = io.open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    b = io.open(BASE, encoding='utf-8', newline='').read().replace('\r\n', '\n') if QC.GATE else ''   # regress — 고침 전 사본 안 읽음(헛잣대 칸은 gate 만)
    out = []
    old_timer = "setTimeout(()=>{try{ggEatNotes()}catch(e){console.warn('ggEatNotes',e)}},1200)"
    out.append(('PASS' if old_timer not in s else 'FAIL')
               + ' | N-4 소스 — 1.2초 타이머가 없다 | ' + json.dumps(s.count(old_timer)))
    if QC.GATE:   # 관문만 — 헛잣대(고침 전 사본 · md5 cc835f04)
        out.append(('PASS' if old_timer in b else 'FAIL')
                   + ' | N-4 헛잣대 — 고침 전 판에는 그 타이머가 있다 | ' + json.dumps(b.count(old_timer)))
    guard = "if(!GG_READY||!(SYNC_REF.gg&&SYNC_REF.gg.g()))return 0;"
    out.append(('PASS' if s.count(guard) >= 2 else 'FAIL')
               + ' | N-4 소스 — 되살림·흡수 둘 다 가드를 본다 | ' + json.dumps(s.count(guard)))
    out.append(('PASS' if 'await ggEatNotes()' in s and s.index('GG_READY=true') < s.index('await ggEatNotes()')
                else 'FAIL') + ' | N-4 소스 — 흡수가 가드 뒤에서 불린다 | null')
    out.append(('PASS' if s.count("moved.forEach(no=>{delete CMT[no]})") == 1
                and s.index('await saveGG();') < s.index("moved.forEach(no=>{delete CMT[no]})")
                else 'FAIL') + ' | N-4 소스 — saveGG 뒤에야 CMT 를 지운다(§B-2) | null')
    return out


# ── _task_qa_slim2(10/8) smoke 도우미 — 이름이 `_rg` 로 시작하는 것 = gate 에서 안 쓰는 갈래(PROBE 상수는 글자 그대로) ──
def _rg_smoke_probe(t):
    """smoke — N-1 · N-2 · N-3 블록까지(N-4 재현 앞에서 끊고 묶음 예외 catch 로 잇는다 · 못 찾으면 통째)"""
    a = t.find("   /* ── N-4 재현(§B-3) ──")
    c = t.find("  }catch(e){R.push('FAIL | 묶음 예외 | '")
    if min(a, c) < 0 or a > c:
        print('NOTE | smoke 자르기 자리 못 찾음 — 통째로 돈다')
        return t
    return t[:a] + t[c:]


print('== 자과앱 add7 묶음 N — 코멘트 ==')
lines = run(SRC, 'new') + (static() if QC.want('static') else [])   # smoke — 소스 글 칸(N-4 소스)은 smoke 칸이 아니다
ng = [x for x in lines if x.startswith('FAIL')]
print('  %d항 · PASS %d · FAIL %d' % (len(lines), len(lines) - len(ng), len(ng)))
for x in lines:
    print('   ', x)
