# -*- coding: utf-8 -*-
r"""_qa/_qa_tabguard_gate.py — 자과 기록 보호 관문 · 2026-10-19 채팅이 만듦(tabguard · a02336da) → 같은 날 Code 가 jagwa_recstore_1019 §F 대로 고침
  python _qa/_qa_tabguard_gate.py <앱 index.html> [--eng chromium,webkit] [--port 0]
  같은 브라우저 두 탭 · 알림 놓친 낡은 탭 · 낡은 탭 저장 · 덮인 IndexedDB(옛 판 통째 값)로 열기 · 새 기기 · 가만히 둔 두 탭 · 한 탭 보통 쓰기 · 저장 즉시 도장 · 쓴 뒤 바로 꺼짐 + 올리기 막이 3 칸
  + 더한 칸(§F-2) ⓐ 두 탭 같은 문항 회독 1 초 안 · ⓑ 옮기기(옛 통째 값 + U/GONE → 행 · 두 번째 열기 = 0) · ⓒ 지움이 다른 탭에 · 원격 payload gone ·
    ⓓ 원격 병합 세 경우(원격 새 칸 · 원격 묘비 · 내가 새것) · ⓔ 옛 꼴 원격(u/gone 없음) · ⓕ 한 탭 회독 50 연속 저장(행 50 · 통째 쓰기 0 · 1 초 안).
  모두 기대값과 맞으면 종료 0 · 하나라도 다르면 그 줄을 찍고 종료 1. 앱 사본에 가짜 fetch(원격 0) — 사용자 기록 무변 · 시험 글은 지어낸 것.
  잼은 판 가리지 않게(헛잣대): 행이 있는 앱(recstore)은 행 · 옛 앱은 localStorage u/gone/shadow 를 읽는다(__G · __U · __SH).
  ★ recstore 고침(10/19 Code · §F-1): T1 = 새로고침 없이 B 가 칸 5 를 받음(reloaded false) · T3 둘 다 reload false · T2 = 알림 놓친 낡은 탭이 써도 다른 탭 칸을 묘비로 안 만들고 들임 ·
    T7 = 낡은 탭 저장이 다른 탭 칸 안 지움 + 자기 칸은 씀(saved8 true) · T5 = 옛 판 탭이 IndexedDB 통째 값을 낡은 것으로 덮어도(행은 그대로) 열면 그대로 · T9 = window.__jgStamp 대신 recWrite ·
    옛 줄: EXP_T T1 reloaded True · T7 saved8 False · 잼 = lsObj(GONE_KEY) · lsObj(U_KEY) · lsObj(SHADOW_KEY) 그대로."""
import sys, asyncio, json, subprocess, os, time, tempfile, shutil, socket
from playwright.async_api import async_playwright
SHIM = "<script>window.pdfjsLib={GlobalWorkerOptions:{},getDocument:function(){return {promise:new Promise(function(){})}}};window.katex={render:function(){},renderToString:function(s){return String(s)}};window.renderMathInElement=function(){};(function(){try{localStorage.setItem('tt.cfg',JSON.stringify({token:'demo',person:'꼬까'}))}catch(e){}\nvar of=window.fetch.bind(window);window.fetch=async function(u,o){var url=String(u&&u.url||u);\nif(/api\\.github\\.com/.test(url)){var m=String((o&&o.method)||'GET').toUpperCase();if(m==='PUT')return new Response(JSON.stringify({content:{sha:'x'}}),{status:200});return new Response('{}',{status:200,headers:{'Content-Type':'application/json'}})}\nif(/^https?:/.test(url))return new Response('',{status:404});return of(u,o)}})()</script>"
# 판 가리지 않는 잼 도구 — 행이 있으면 행 · 없으면 옛 localStorage(옛 판 = 헛잣대)
TOOLS = r"""(()=>{
window.__RECAPP=()=>typeof recRowsRaw==='function';
window.__rows=async k=>window.__RECAPP()?((await recRowsRaw(k))||{}):null;
window.__G=async(k,c)=>{const r=await __rows(k);if(r)return !!(r[c]&&r[c].g);return !!lsObj(GONE_KEY)[k+'|'+c]};
window.__U=async(k,c)=>{const r=await __rows(k);if(r)return r[c]?(r[c].u||0):0;return lsObj(U_KEY)[k+'|'+c]||0};
window.__SH=(k,c)=>(typeof REC_SNAP!=='undefined')?!!((REC_SNAP[k]||{})[c]&&!REC_SNAP[k][c].g):!!((lsObj(SHADOW_KEY)[k]||{})[c]);
window.__STAMP=()=>{try{return typeof stampAll==='function'?stampAll():0}catch(e){return 'ERR '+e}};
window.__RAWPUT=(s,k,v)=>typeof rawPut==='function'?rawPut(s,k,v):put(s,k,v);
window.__STORE=async k=>(await get('kv',k))||{};
window.__TOMBS=async k=>{const r=await __rows(k);if(r)return Object.values(r).filter(x=>x.g).length;return Object.keys(lsObj(GONE_KEY)).filter(x=>x.indexOf(k+'|')===0).length};
return 1})()"""
APP = sys.argv[1]
ENG = (sys.argv[sys.argv.index('--eng') + 1] if '--eng' in sys.argv else 'chromium').split(',')
PORT = int(sys.argv[sys.argv.index('--port') + 1]) if '--port' in sys.argv else 0   # 0 = 빈 자리(무리 둘이 겹쳐도 안 부딪침 · 옛: 8765 고정)


async def page(ctx, errs, wait=6000):
    P = await ctx.new_page(); P.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await P.goto('http://127.0.0.1:' + str(PORT) + '/a.html?subj=phys'); await P.wait_for_timeout(wait)
    await P.evaluate("window.__mark=1"); await P.evaluate(TOOLS); return P


async def reload(P, wait=7000):
    await P.reload(); await P.wait_for_timeout(wait); await P.evaluate(TOOLS)


async def run(app, eng):
    res = {}
    async with async_playwright() as p:
        b = await getattr(p, eng).launch()

        async def rt(r):
            u = r.request.url; await (r.continue_() if (u.startswith('http://127.0.0.1:' + str(PORT)) or not u.startswith('http')) else r.abort())
        errs = []

        async def newctx():
            c = await b.new_context(); await c.route('**/*', rt); return c
        # T1 — 같은 브라우저 두 탭 · A 가 쓴 칸을 B 가 새로고침 없이 받음 · B 도장(옛 이름) 뒤에도 묘비 0
        ctx = await newctx()
        A = await page(ctx, errs); B = await page(ctx, errs)
        await A.evaluate("(async()=>{ST['5']={h:[{m:'O',t:Date.now(),s:9}]};await saveST();__STAMP();})()"); await A.wait_for_timeout(1500)
        await B.evaluate("__STAMP()")
        await B.wait_for_timeout(5000)
        res['T1'] = await B.evaluate("(async()=>({reloaded:!window.__mark,has5:'5' in ST,gone5:await __G('status','5')}))()")
        await ctx.close()
        # T2 · T7 — 알림 놓친 낡은 탭: 다른 탭이 칸 7 을 써 둠(새 판 = 행 · 알림 없음 / 옛 판 = 그림자 · 도장) → 이 탭이 도장 · 쓰기
        ctx = await newctx()
        C = await page(ctx, errs)
        await C.evaluate("""(async()=>{const now=Date.now(),v={h:[{m:'O',t:now,s:3}]};
          if(__RECAPP())await recPutRows([{k:'status',c:'7',v:v,u:now,g:0}]);
          const sh=lsObj(SHADOW_KEY);sh.status=sh.status||{};sh.status['7']=v;localStorage.setItem(SHADOW_KEY,JSON.stringify(sh));
          const u=lsObj(U_KEY);u['status|7']=now;localStorage.setItem(U_KEY,JSON.stringify(u));localStorage.setItem(CUR.SYNC_PREFIX+'rev','other');return 1})()""")
        await C.evaluate("window.shStaleReload=()=>{}")
        res['T2'] = await C.evaluate("""(async()=>{let n=__STAMP();
          if(typeof recWrite==='function'){await recWrite('status',ST);n=(window.__recLast||{}).w||0}
          return {n:n,gone7:await __G('status','7'),has7:'7' in ST}})()""")
        res['T7'] = await C.evaluate("""(async()=>{const before=await __STORE('status');ST['8']={h:[{m:'X',t:1,s:1}]};await saveST();const db=await __STORE('status');
          return {before8:!!before['8'],saved8:!!db['8'],alive7:!!db['7']&&!(await __G('status','7'))}})()""")
        await ctx.close()
        # T5 — 옛 판 탭이 IndexedDB 통째 값을 낡은 것으로 덮은 채 다시 열기
        ctx = await newctx()
        D = await page(ctx, errs)
        await D.evaluate("(async()=>{ST['5']={h:[{m:'O',t:Date.now(),s:9}]};ST['6']={h:[{m:'O',t:Date.now(),s:4}]};await saveST();__STAMP();})()")
        await D.evaluate("(async()=>{const s=JSON.parse(JSON.stringify(ST));delete s['5'];s['6']={h:[{m:'X',t:1,s:1}]};await __RAWPUT('kv','status',s);})()")
        await reload(D)
        res['T5'] = await D.evaluate("(async()=>({has5:'5' in ST,v6:(ST['6']||{}).h&&ST['6'].h[0].m,gone5:await __G('status','5'),u6:(await __U('status','6'))>0}))()")
        # T6 — 그림자에 통이 없는 기기(새 기기) — 지우지 않음
        n0 = await D.evaluate("Object.keys(ST).length")
        await D.evaluate("(()=>{const sh=lsObj(SHADOW_KEY);delete sh.status;localStorage.setItem(SHADOW_KEY,JSON.stringify(sh));})()")
        await reload(D)
        res['T6'] = await D.evaluate("(async()=>({n0:%d,n:Object.keys(ST).length,goneAny:await __TOMBS('status')}))()" % n0)
        # T8 — 저장 즉시 도장 · T9 — 쓴 뒤 바로 꺼짐 → 열면 그대로
        res['T8'] = await D.evaluate("(async()=>{ST['11']={h:[{m:'O',t:Date.now(),s:2}]};await saveST();return {u11:(await __U('status','11'))>0,sh11:__SH('status','11')}})()")
        await D.evaluate("""(async()=>{ST['12']={h:[{m:'O',t:Date.now(),s:2}]};
          try{if(typeof recWrite==='function')await recWrite('status',ST);else window.__jgStamp()}catch(e){return 'ERR '+e}return 1})()""")
        await reload(D)
        res['T9'] = await D.evaluate("(async()=>{const db=await __STORE('status');return {has12:'12' in ST,db12:!!db['12'],gone12:await __G('status','12'),has11:'11' in ST}})()")
        await ctx.close()
        # T3 · T4 — 가만히 둔 두 탭(새로고침 되풀이 0) · 한 탭 보통 쓰기
        ctx = await newctx()
        E = await page(ctx, errs); F = await page(ctx, errs)
        await E.wait_for_timeout(20000)
        res['T3'] = {'E_reload': await E.evaluate("!window.__mark"), 'F_reload': await F.evaluate("!window.__mark")}
        await F.close()
        res['T4'] = await E.evaluate("(async()=>{ST['9']={h:[{m:'X',t:Date.now(),s:5}]};await saveST();const n1=__STAMP();const n2=__STAMP();return {n1,n2,u9:(await __U('status','9'))>0}})()")
        await ctx.close()
        # ⓐ 두 탭이 같은 문항 회독을 1 초 안에 각각 더함 → 둘 다 남음(h 2)
        ctx = await newctx()
        A = await page(ctx, errs); B = await page(ctx, errs)
        add = "(async m=>{const t=Date.now();ST['20']=ST['20']||{h:[]};ST['20'].h.push({m:m,t:t,s:1});await saveST();return t})"
        await asyncio.gather(A.evaluate(add, 'O'), B.evaluate(add, 'X'))
        await A.wait_for_timeout(1500)
        hA = await A.evaluate("((ST['20']||{}).h||[]).length"); hB = await B.evaluate("((ST['20']||{}).h||[]).length")
        hD = await A.evaluate("(async()=>(((await __STORE('status'))['20']||{}).h||[]).length)()")
        res['P1'] = {'hA': hA, 'hB': hB, 'hDB': hD}
        # ⓒ 탭 A 가 지움(회독 지우기 길 = delete ST[칸] + saveST) → B 에 알림으로 사라짐 · 원격 payload 에 gone
        await A.evaluate("(async()=>{ST['40']={h:[{m:'O',t:Date.now(),s:1}]};await saveST();})()"); await A.wait_for_timeout(1500)
        b40 = await B.evaluate("'40' in ST")
        await A.evaluate("(async()=>{delete ST['40'];await saveST();})()"); await A.wait_for_timeout(1500)
        res['P3'] = {'B_has40_after_add': b40, 'B_has40_after_del': await B.evaluate("'40' in ST"),
                     'payload_gone': await A.evaluate("!!(recPayload(null).gone||{})['status|40']")}
        await ctx.close()
        # ⓑ 옮기기 — 옛 통째 값 + U_KEY/GONE_KEY 를 심어 두고 처음 열기 → 행 · u 그대로 · 묘비 칸은 메모리에 없음 · 두 번째 열기 = 옮김 0
        ctx = await newctx()
        M = await page(ctx, errs)
        await M.evaluate("""(async()=>{
          await new Promise(ok=>{const t=db.transaction('kv','readwrite'),s=t.objectStore('kv');
            ['status','note'].forEach(k=>{s.delete(IDBKeyRange.bound('rec:'+k+'|','rec:'+k+'|\\uffff'));s.delete('recv:'+k)});
            s.put({'31':{h:[{m:'O',t:1111,s:1}]},'32':{h:[{m:'X',t:1500,s:2}]}},'status');s.put({'31':'옛 메모'},'note');t.oncomplete=ok;t.onerror=ok});
          localStorage.setItem(U_KEY,JSON.stringify({'status|31':1111,'note|31':2222}));localStorage.setItem(GONE_KEY,JSON.stringify({'status|33':3333}));return 1})()""")
        await reload(M)
        res['P2'] = await M.evaluate("""(async()=>{const r=await __rows('status')||{},n=await __rows('note')||{};
          const gg=[].concat(...Object.values(GG||{}).map(v=>Array.isArray(v)?v:[])).find(x=>x&&x.t==='옛 메모');   /* 물리는 코멘트를 근거로 옮긴다(ggEatNotes · ts = 그 코멘트 도장 · 근거 통이 늦게 서면 아직 안 옮겼을 수 있다) */
          const nr=n['31'];const noteOK=gg?gg.ts===2222:!!(nr&&!nr.g&&nr.u===2222&&CMT['31']==='옛 메모');   /* 옮겼으면 근거 ts = 옮긴 도장 · 아직이면 코멘트 행 u = 옮긴 도장 */
          return {mig:window.__RECMIG||0,u31:r['31']&&r['31'].u,u32:r['32']&&r['32'].u,g33:r['33']&&r['33'].g,has31:'31' in ST,has33:'33' in ST,noteOK:noteOK,moved:!!gg}})()""")
        await reload(M)
        res['P2b'] = await M.evaluate("({mig2:window.__RECMIG||0,has31:'31' in ST})")
        # ⓓ 원격 병합 — 원격 새 칸 · 원격 묘비 · 내가 새것 · ⓔ 옛 꼴 원격(u/gone 없음)
        await M.evaluate("""(async()=>{
          if(__RECAPP()){await recPutRows([{k:'status',c:'51',v:{h:[{m:'O',t:5000,s:1}]},u:5000,g:0},{k:'status',c:'52',v:{h:[{m:'O',t:5000,s:7}]},u:5000,g:0},{k:'status',c:'61',v:{h:[{m:'X',t:5000,s:1}]},u:5000,g:0}]);
            ST=await get('kv','status')}
          else{ST['51']={h:[{m:'O',t:5000,s:1}]};ST['52']={h:[{m:'O',t:5000,s:7}]};ST['61']={h:[{m:'X',t:5000,s:1}]};await saveST();
            const u=lsObj(U_KEY);u['status|51']=5000;u['status|52']=5000;u['status|61']=5000;localStorage.setItem(U_KEY,JSON.stringify(u));
            const sh=lsObj(SHADOW_KEY);sh.status=JSON.parse(JSON.stringify(ST));localStorage.setItem(SHADOW_KEY,JSON.stringify(sh))}
          return 1})()""")
        res['P4'] = await M.evaluate("""(async()=>{
          const R={data:{status:{'50':{h:[{m:'O',t:6000,s:1}]},'52':{h:[{m:'X',t:4000,s:1}]}}},u:{'status|50':6000,'status|52':4000},gone:{'status|51':7000}};
          const m=await recMerge(R);
          return {has50:'50' in ST,has51:'51' in ST,gone51:await __G('status','51'),v52:(ST['52']||{}).h&&ST['52'].h[0].m,took:m.took,del:m.del}})()""")
        res['P5'] = await M.evaluate("""(async()=>{
          const R={data:{status:{'60':{h:[{m:'O',t:6100,s:1}]},'61':{h:[{m:'O',t:6100,s:1}]}}}};
          await recMerge(R);return {has60:'60' in ST,u60:await __U('status','60'),v61:(ST['61']||{}).h&&ST['61'].h[0].m}})()""")
        await ctx.close()
        # ⓕ 한 탭 회독 50 연속 저장 → 행 50 · 통째 쓰기 0 · 1 초 안
        ctx = await newctx()
        S = await page(ctx, errs)
        res['P6'] = await S.evaluate("""(async()=>{const raw=k=>new Promise(ok=>{const r=db.transaction('kv','readonly').objectStore('kv').get(k);r.onsuccess=()=>ok(JSON.stringify(r.result));r.onerror=()=>ok('ERR')});
          const w0=await raw('status'),t0=performance.now();
          for(let i=1;i<=50;i++){ST[String(100+i)]={h:[{m:'O',t:Date.now(),s:1}]};await saveST()}
          const ms=Math.round(performance.now()-t0),w1=await raw('status');
          const r=await __rows('status');const rows=r?Object.keys(r).filter(c=>+c>100&&+c<=150).length:0;
          return {rows:rows,wholeSame:w0===w1,ms:ms,under1s:ms<1000}})()""")
        await ctx.close()
        res['errs'] = errs[:4]; await b.close()
    return res
JS = r"""(()=>[['원격 없음(새 파일)',(()=>{try{jgPushGuard({data:{}},null,null);return '통과'}catch(e){return '막음'}})()],['원격 있는데 못 읽음',(()=>{try{jgPushGuard({data:{}},null,'abc');return '통과'}catch(e){return '막음'}})()],['원격 읽음 · 지움 25칸이어도 막지 않음(띠 없음)',(()=>{const R={data:{status:{}}},P={data:{status:{}}};for(let i=1;i<=25;i++)R.data.status[i]={h:[]};try{jgPushGuard(P,R,'abc');return '통과'}catch(e){return '막음'}})()]])()"""
JS2 = r'''({})'''


async def runguard(eng):
    async with async_playwright() as p:
        b = await getattr(p, eng).launch(); ctx = await b.new_context()

        async def rt(r):
            u = r.request.url; await (r.continue_() if (u.startswith('http://127.0.0.1:' + str(PORT)) or not u.startswith('http')) else r.abort())
        await ctx.route('**/*', rt); P = await ctx.new_page(); errs = []; P.on('pageerror', lambda e: errs.append(str(e)[:100]))
        await P.goto('http://127.0.0.1:' + str(PORT) + '/a.html?subj=phys'); await P.wait_for_timeout(5000)
        a = await P.evaluate(JS); c = await P.evaluate(JS2); await b.close(); return a, c, errs

# ★ recstore(§F-1) 기대값 — 옛 줄: 'T1':{'reloaded':True,'has5':True,'gone5':False} · 'T2':{'n':0,'gone7':False} · 'T7':{'saved8':False} · 'T5':{'has5':True,'v6':'O','gone5':False}
EXP_T = {'T8': {'u11': True, 'sh11': True}, 'T9': {'has12': True, 'db12': True, 'gone12': False, 'has11': True},
         'T1': {'reloaded': False, 'has5': True, 'gone5': False}, 'T2': {'n': 0, 'gone7': False, 'has7': True},
         'T7': {'saved8': True, 'alive7': True}, 'T5': {'has5': True, 'v6': 'O', 'gone5': False}, 'T6': {'goneAny': 0}, 'T4': {'n2': 0, 'u9': True},
         'P1': {'hA': 2, 'hB': 2, 'hDB': 2}, 'P3': {'B_has40_after_add': True, 'B_has40_after_del': False, 'payload_gone': True},
         'P2': {'mig': 4, 'u31': 1111, 'u32': 1, 'g33': 3333, 'has31': True, 'has33': False, 'noteOK': True}, 'P2b': {'mig2': 0, 'has31': True},
         'P4': {'has50': True, 'has51': False, 'gone51': True, 'v52': 'O'}, 'P5': {'has60': True, 'u60': 1, 'v61': 'X'},
         'P6': {'rows': 50, 'wholeSame': True, 'under1s': True}}
EXP_G = {'원격 없음': '통과', '원격 있는데': '막음', '원격 읽음': '통과'}
EXP_B = {}
NAME = {'P1': 'ⓐ 두 탭 회독 합침', 'P2': 'ⓑ 옮기기', 'P2b': 'ⓑ 두 번째 열기', 'P3': 'ⓒ 지움 알림 · payload gone', 'P4': 'ⓓ 원격 병합 세 경우', 'P5': 'ⓔ 옛 꼴 원격', 'P6': 'ⓕ 회독 50 연속'}


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); n = s.getsockname()[1]; s.close(); return n


def main():
    global PORT
    if not PORT:
        PORT = free_port()
    d = tempfile.mkdtemp(); os.makedirs(os.path.join(d, 'srv'))
    open(os.path.join(d, 'srv', 'a.html'), 'w', encoding='utf-8').write(open(APP, encoding='utf-8').read().replace('<head>', '<head>' + SHIM, 1))
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=os.path.join(d, 'srv'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    bad = 0
    try:
        for eng in ENG:
            t0 = time.time(); res = asyncio.run(run(APP, eng)); a, c, errs = asyncio.run(runguard(eng))
            for k, exp in EXP_T.items():
                ok = all(res.get(k, {}).get(x) == v for x, v in exp.items()); bad += not ok
                print(('PASS' if ok else 'FAIL'), '|', eng, k + ((' ' + NAME[k]) if k in NAME else ''), '|', json.dumps(res.get(k), ensure_ascii=False))   # 칸 이름 | 값(실행기 받개가 이름으로 id 를 잡게 · 옛: 이름 뒤에 값을 바로)
            t3 = res.get('T3', {}); ok = not t3.get('F_reload') and not t3.get('E_reload'); bad += not ok; print(('PASS' if ok else 'FAIL'), '|', eng, 'T3', '|', json.dumps(t3))   # 옛 줄: ok=not t3.get('F_reload')
            for name, r in a:
                key = next((x for x in EXP_G if name.startswith(x)), None); ok = key is not None and r.startswith(EXP_G[key]); bad += not ok; print(('PASS' if ok else 'FAIL'), '|', eng, '차단기', name, '|', r[:40])
            e = list(res.get('errs', [])) + list(errs); ok = not e; bad += not ok; print(('PASS' if ok else 'FAIL'), '|', eng, '페이지 오류', '|', e[:3]); print('  ', eng, '%.1f 분' % ((time.time() - t0) / 60))
    finally:
        srv.terminate(); shutil.rmtree(d, ignore_errors=True)
    print('합계: FAIL', bad); sys.exit(1 if bad else 0)


main()
