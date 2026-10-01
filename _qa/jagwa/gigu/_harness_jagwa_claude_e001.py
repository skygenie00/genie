# -*- coding: utf-8 -*-
r"""_task_jagwa_claude_e001 · _add1 · _add2 관문 「CE1」 — 지학 149·84 Claude 풀이 · 모션

  python _harness_jagwa_claude_e001.py [--eng chromium,webkit] [--res <결과>]

  NEW = genie 작업트리(motion/index.json · earth_149.html · earth_84.html 더함 · jagwa/index.html 무변)
        + 지학 기록 = studyplandata 작업트리 earth/기록.json(적재 뒤) — 아직 적재 전이면 같은 두 칸을 더한 사본을 만든다(「합성」이라 적음)
  BASE(헛잣대) = genie 인도 앞 커밋(--base · 2998b9e)의 motion/*(84·149 없음) + 기록에서 gpt 149·84 와 그 도장만 뺀 것
        ⚠ 인도 뒤 다시 돌려도 헛잣대가 거저 PASS 가 안 되게 바탕을 HEAD 에서 읽지 않는다(9/29 실측 — HEAD 로 읽으니 모션 줄 바탕이 PASS)
  적재 커밋(--seed · cbd451ae) = studyplandata 에서 earth/기록.json 하나만 건드렸나
  기록은 route 사본 · PUT 은 가로채 밖으로 안 나감 · 앱 코드 한 벌(무변 확인)
"""
import io, json, os, re, sys, time, hashlib, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import _harness_jagwa_uid as HU   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = HU.GENIE; SPD = HU.SPD
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_claude_e001_result.txt'))
MAT = os.path.join(HERE, 'claude_motion')
BASE_REV = ARG('--base', '2998b9e')   # genie — 이 판 인도(802cb0a) 바로 앞 = env_lanes 인도판
SEED_REV = ARG('--seed', 'cbd451ae')  # studyplandata — _gpt_seed.py earth 149 84 --write 커밋
NOS = {'149': {'code': 'G09-46-10', 'li': 19, 'b': 3}, '84': {'code': 'G03-40-05', 'li': 18, 'b': 6}}
ROWS = []
from playwright.sync_api import sync_playwright   # noqa: E402


def R(eng, name, okn, okb, val):
    ROWS.append((eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:420]), flush=True)


def md(no):
    return io.open(os.path.join(MAT, 'earth_%s.md' % no), encoding='utf-8', newline='').read().replace('\r\n', '\n')


def recs():
    head = HU.git(SPD, 'show', 'HEAD:earth/기록.json')
    wt = open(os.path.join(SPD, 'earth', '기록.json'), 'rb').read()
    dw = json.loads(wt.decode('utf-8'))
    if all((dw['data'].get('gpt') or {}).get(n) == md(n) for n in NOS):
        b = json.loads(wt.decode('utf-8'))   # 바탕 = 지금 기록에서 이 판의 두 칸과 도장만 뺀 것(다른 칸은 같게)
        for n in NOS:
            b['data']['gpt'].pop(n, None); b['u'].pop('gpt|' + n, None); b.get('gone', {}).pop('gpt|' + n, None)
        return wt, json.dumps(b, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), '적재 뒤 실물'
    d = json.loads(head.decode('utf-8'))
    now = int(time.time() * 1000)
    for n in NOS:
        d['data'].setdefault('gpt', {})[n] = md(n); d['u']['gpt|' + n] = now
    return json.dumps(d, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), head, '합성(적재 전)'


def statics():
    mdir = os.path.join(GENIE, 'jagwa', 'motion')
    new = {'motion/' + f: open(os.path.join(mdir, f), 'rb').read() for f in os.listdir(mdir)}
    base = {}
    for f in HU.git(GENIE, 'ls-tree', '--name-only', BASE_REV, 'jagwa/motion/').decode('utf-8').split():
        base['motion/' + f.split('/')[-1]] = HU.git(GENIE, 'show', BASE_REV + ':' + f)
    assert base, 'NG 바탕 motion 을 못 읽었다(%s)' % BASE_REV
    return new, base


CJS = r"""
window.__C={
 tx:e=>e?String(e.textContent||'').replace(/\s+/g,' ').trim():'',
 async open(no){try{closeView()}catch(e){}await new Promise(r=>setTimeout(r,150));await openView(no);await new Promise(r=>setTimeout(r,1200));
   const b=document.getElementById('tGpt');const row=b&&b.parentElement;const vis=[...(row?row.children:[])].filter(x=>x.offsetParent!==null&&getComputedStyle(x).display!=='none');
   return {btn:__C.tx(b),last:vis.length?vis[vis.length-1]===b:false}},
 sheet(){const s=[...document.querySelectorAll('.sheet')].pop();if(!s)return null;const rd=s.querySelector('.gpread');
   return {p:__C.tx(s.querySelector('.panel > p')),read:!!rd,edit:!!s.querySelector('#gpIn'),h3:rd?rd.querySelectorAll('h3.gph').length:0,
     li:rd?rd.querySelectorAll('ul.gpul li').length:0,tb:rd?rd.querySelectorAll('table.gptb').length:0,th:rd?rd.querySelectorAll('table.gptb th').length:0,
     tr:rd?rd.querySelectorAll('table.gptb tbody tr').length:0,b:rd?rd.querySelectorAll('b').length:0,script:rd?rd.querySelectorAll('script').length:0,
     paras:rd?[...rd.querySelectorAll('p')].slice(0,3).map(__C.tx):[],p1:rd?((rd.querySelector('p.gpp')||{}).innerText||''):'',text:rd?rd.textContent:'',
     mot:(()=>{const m=s.querySelector('#gpMotBar');return !!m&&m.style.display!=='none'})()}},
 closeSheets(){document.querySelectorAll('.sheet').forEach(x=>x.remove())},
 async frame(){const f=document.getElementById('gpMotFrame');if(!f)return null;for(let i=0;i<40;i++){try{if(f.contentDocument&&f.contentDocument.readyState==='complete'&&f.contentDocument.body)break}catch(e){}await new Promise(r=>setTimeout(r,150))}
   let d=null;try{d=f.contentDocument}catch(e){return {src:f.getAttribute('src'),same:false}}
   const st=await fetch(f.getAttribute('src'),{cache:'no-store'}).then(r=>r.status).catch(()=>0);
   const hide=d.getElementById('hideBtn');
   const big=[...d.querySelectorAll('a')].find(x=>/크게 보기/.test(x.textContent));
   return {src:f.getAttribute('src'),status:st,same:true,card:d.querySelectorAll('svg.card').length,hideBtn:!!hide&&/가리기/.test(hide.textContent),
     ansT:__C.ansOp(d),big:big?big.getAttribute('target'):null,text:d.body?d.body.textContent:''}},
 ansOp(d){return [...d.querySelectorAll('.ans text')].map(t=>getComputedStyle(t).opacity)},
 frameAfter(){const d=document.getElementById('gpMotFrame').contentDocument;const c=d.getElementById('card');
   return {ansT:__C.ansOp(d),pressed:d.getElementById('hideBtn').getAttribute('aria-pressed'),blank:!!c&&c.classList.contains('blank')}},
 gpNos(){return Object.keys(GP).sort()},
 listTags(){return [...document.querySelectorAll('#list .item')].filter(d=>d.querySelector('.tag.gp')).map(d=>+((DATA.find(r=>r[F.CODE]===d.dataset.uid)||[])[0]||0))}
};
"""


def dv_open(br, eng, app, subj, rec, stat, phone=False):
    dv = HU.Dev(br, eng, phone)
    dv.load(app, SPD, subj, rec={'%s/기록.json' % subj: rec} if rec else None, static=stat)
    dv.ev(CJS)
    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
    return dv


def click(dv, sel):
    r = dv.ev("s=>{const e=document.querySelector(s);if(!e)return null;e.scrollIntoView({block:'nearest'});const b=e.getBoundingClientRect();return [b.x+b.width/2,b.y+b.height/2]}", sel)
    if not r:
        return False
    dv.pg.mouse.click(r[0], r[1]); dv.pg.wait_for_timeout(700)
    return True


OLDNUM = re.compile(r'G\d\d-\d\d-\d(?!\d)|(?<![A-Za-z0-9])C\d-\d{3}')


def run_side(br, eng, who, app, rec, stat):
    out = {}
    dv = dv_open(br, eng, app, 'earth', rec, stat)
    try:
        out['list'] = dv.ev("()=>__C.listTags()")
        out['gp'] = dv.ev("()=>__C.gpNos()")
        for no in NOS:
            o = {'btn': dv.ev("n=>__C.open(n)", int(no))}
            click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
            o['sheet'] = dv.ev("()=>__C.sheet()")
            if o['sheet'] and o['sheet']['mot']:
                click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500)
                o['frame'] = dv.ev("()=>__C.frame()")
                if o['frame'] and o['frame'].get('same'):
                    try:   # iframe 안 「가리기」 = 진짜 누름(합성 click() 아님)
                        dv.pg.frame_locator('#gpMotFrame').locator('#hideBtn').click(timeout=15000); dv.pg.wait_for_timeout(600)
                        o['frame']['after'] = dv.ev("()=>__C.frameAfter()")
                    except Exception as e:
                        o['frame']['after'] = {'err': repr(e)[:160]}
            dv.ev("()=>__C.closeSheets()")
            out[no] = o
        # 이웃 번호 · 모션 단추 0
        nb = {}
        for n in (148, 150, 83, 85):
            dv.ev("n=>__C.open(n)", n); click(dv, '#tGpt'); dv.pg.wait_for_timeout(700)
            s = dv.ev("()=>__C.sheet()"); nb[n] = bool(s and s['mot']); dv.ev("()=>__C.closeSheets()")
        out['nb'] = nb
        out['gpText'] = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
        out['keys'] = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")
        out['stores'] = dv.ev("k=>__J.stores(k)", out['keys'])   # 빈 기기 — gpt 말고 나머지 칸(새 판·바탕이 같아야)
        ss = {}
        dv.ev("()=>{try{closeView()}catch(e){}}"); dv.pg.wait_for_timeout(300)
        for q in ('G18-55-02', 'G3-059C', 'G03-40-05'):
            try:   # 검색 칸을 눌러 치고 Enter(jagwa_search 하네스 typeq 와 같은 길)
                loc = dv.pg.locator('#q'); loc.click(); loc.fill('')
                dv.pg.keyboard.type(q, delay=5); dv.pg.keyboard.press('Enter'); dv.pg.wait_for_timeout(400)
                ss[q] = dv.ev("()=>typeof ES_NOS!=='undefined'?ES_NOS.map(n=>String(codeShow(DATA[n-1]))):null")
            except Exception as e:
                ss[q] = 'ERR ' + repr(e)[:120]
        try:
            loc = dv.pg.locator('#q'); loc.click(); loc.fill(''); dv.pg.keyboard.press('Enter')
        except Exception:
            pass
        out['search'] = ss
        out['errs'] = dv.errs[:3]
    finally:
        dv.close()
    return out


def main():
    rn, rb, how = recs()
    sn, sb = statics()
    app = HU.git(GENIE, 'show', 'HEAD:jagwa/index.html')
    wt = open(os.path.join(GENIE, 'jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')
    print('기록 = %s · 앱 = genie HEAD jagwa/index.html(작업트리와 %s)' % (how, '같음' if wt == app else '다름'))
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in ENGS:
            br = getattr(pw, eng).launch()
            try:
                N = run_side(br, eng, 'NEW', app, rn, sn)
                B = run_side(br, eng, 'BASE', app, rb, sb)
                for no, w in NOS.items():
                    n, b = N[no], B[no]
                    s = n['sheet'] or {}
                    ok1 = n['btn']['btn'] == 'Claude ✓' and n['btn']['last'] and s.get('read') and not s.get('edit') and s.get('p', '').startswith(w['code'] + ' · ') \
                        and 'undefined' not in s.get('p', '') and ' ·  ' not in s.get('p', '') and not s.get('p', '').endswith('·')
                    okb1 = b['btn']['btn'] == 'Claude ✓' and bool((b['sheet'] or {}).get('read'))
                    R(eng, '%s — 「Claude ✓」(아랫줄 맨 오른쪽) · 머리 「%s · …」 · 읽기 판 먼저' % (no, w['code']), ok1, okb1, {'단추': n['btn'], '머리': s.get('p'), '바탕 단추': b['btn']['btn']})
                    head = [x.strip() for x in md(no).split('\n\n')[0].replace('**', '').split('\n')]
                    p1 = [x.strip() for x in (s.get('p1') or '').split('\n')]
                    ok2 = s.get('h3') == 6 and s.get('li') == w['li'] and s.get('tb') == 1 and s.get('th') == 4 and s.get('tr') == 4 and s.get('b') == w['b'] and s.get('script') == 0 and p1 == head
                    R(eng, '%s 읽기 판 — h3.gph 6 · li %d · 표 1(th 4 · tr 4) · <b> %d · script 0 · 원문 첫 %d줄 = 첫 문단(줄마다)' % (no, w['li'], w['b'], len(head)), ok2, None,
                      dict({k: s.get(k) for k in ('h3', 'li', 'tb', 'th', 'tr', 'b', 'script')}, 첫문단=p1 == head, 첫문단줄=len(p1)))
                    f = n.get('frame') or {}
                    fa = f.get('after') or {}
                    a0, a1 = f.get('ansT') or [], fa.get('ansT') or []
                    ok3 = s.get('mot') and f.get('src') == 'motion/earth_%s.html' % no and f.get('status') == 200 and f.get('same') and f.get('card') == 1 \
                        and f.get('hideBtn') and bool(a0) and all(x == '1' for x in a0) and len(a1) == len(a0) and all(x == '0' for x in a1) \
                        and fa.get('pressed') == 'true' and fa.get('blank') and f.get('big') == '_blank'
                    R(eng, '%s 모션 — ▶ 모션 · iframe motion/earth_%s.html 200 · 같은 출처 · svg.card 1 · 「가리기」 진짜 누름 → .ans 글자 opacity 0 · 크게 보기 _blank' % (no, no), ok3,
                      bool((b['sheet'] or {}).get('mot')), {'src': f.get('src'), 'status': f.get('status'), 'same': f.get('same'), 'card': f.get('card'),
                                                            '.ans 글자': '%d개 %s → %s' % (len(a0), sorted(set(a0)), sorted(set(a1))), 'pressed': fa.get('pressed'),
                                                            'blank': fa.get('blank'), 'big': f.get('big'), 'err': fa.get('err')})
                    old = OLDNUM.findall(s.get('text', '') + ' ' + f.get('text', ''))
                    R(eng, '%s add2 — 읽기 판·모션 글자에 옛 꼴 번호 0' % no, not old and bool(s.get('text')) and bool(f.get('text')), None, old[:5])
                    R(eng, '%s 데이터 — GP[%s] = 재료 글자 전수(%d자)' % (no, no, len(md(no))), N['gpText'].get(no) == md(no), B['gpText'].get(no) == md(no),
                      {'길이': len(N['gpText'].get(no) or '')})
                R(eng, 'add2 — 새 꼴 번호 셋(G18-55-02 · G3-059C · G03-40-05) 검색 = 그 문항 하나', all(v == [k] for k, v in N['search'].items()), None, N['search'])
                R(eng, '이웃 148·150·83·85 — 모션 단추 0', not any(N['nb'].values()), None, N['nb'])
                # ★ 2026-10-01 claude_e004 — 지학 111 을 더해 gpt 칸이 셋이 된다. 「84·149 두 줄」 은 값을 박은 잣대라 뒤 판마다 거짓 FAIL
                #   → 「.tag.gp 줄 = 그 기록의 gpt 칸 번호 전부 · 84·149 가 든다」 로 갈음(바탕 = 두 칸 뺀 기록 → 84·149 없음 → FAIL 그대로)
                wl = sorted(int(k) for k in (json.loads(rn.decode('utf-8'))['data'].get('gpt') or {}))
                R(eng, '목록 — .tag.gp 줄 = 기록 gpt 칸 번호 전부(84·149 가 든다)', sorted(N['list']) == wl and {84, 149} <= set(wl),
                  sorted(B['list']) == wl and {84, 149} <= set(B['list']), {'NEW': N['list'], 'BASE': B['list'], '기록 gpt': wl})
                R(eng, '페이지 오류 0', not N['errs'], None, N['errs'])
                dk = [k for k in N['keys'] if N['stores'].get(k) != B['stores'].get(k)]
                R(eng, '빈 기기 — 동기화 뒤 gpt 말고 나머지 칸 %d 가 바탕과 같다(status·bogi·gg·unit·bpg …)' % len(N['keys']), not dk and N['keys'] == B['keys'], None,
                  {'다른 칸': dk, '칸 수': len(N['keys'])})
                # 물리 72 무변
                ph = {}
                for who, st in (('NEW', sn), ('BASE', sb)):
                    dv = dv_open(br, eng, app, 'phys', None, st)
                    try:
                        dv.ev("n=>__C.open(n)", 72); click(dv, '#tGpt'); dv.pg.wait_for_timeout(900)
                        s = dv.ev("()=>__C.sheet()")
                        if s and s['mot']:
                            click(dv, '#gpMot'); dv.pg.wait_for_timeout(1500)
                        f = dv.ev("()=>__C.frame()") or {}
                        ph[who] = {'gp72': dv.ev("()=>GP[72]||''"), 'mot': bool(s and s['mot']), 'src': f.get('src'), 'card': f.get('card'), 'h3': (s or {}).get('h3')}
                    finally:
                        dv.close()
                R(eng, '물리 72 — GP·모션 단추·iframe = 바탕', ph['NEW'] == ph['BASE'] and ph['NEW']['mot'], None, {'NEW': {k: v for k, v in ph['NEW'].items() if k != 'gp72'}, 'GP 같음': ph['NEW']['gp72'] == ph['BASE']['gp72']})
                # 기록 있는 기기 — 적재 전 기록으로 먼저 열고 5번에 △ 를 진짜로 눌러(내 칸이 더 새것) 둔 뒤 적재 뒤 원격을 받는다
                dv = dv_open(br, eng, app, 'earth', rb, sn)
                try:
                    keys = dv.ev("()=>SYNC_KEYS.filter(k=>k!=='gpt')")   # 동기화 칸 전부(gpt 는 따로 잰다)
                    dv.ev("n=>__C.open(n)", 5); h0 = dv.ev("()=>((ST[5]||{}).h||[]).length")
                    click(dv, '#card [data-vmark="Q"]'); dv.pg.wait_for_timeout(500); h1 = dv.ev("()=>((ST[5]||{}).h||[]).length")   # 지학 카드 층 = 카드 안 △(아랫줄 #mQ 는 숨음)
                    dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    before = dv.ev("k=>__J.stores(k)", keys)
                    dv.load(app, SPD, 'earth', rec={'earth/기록.json': rn}, static=sn); dv.ev(CJS)
                    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
                    after = dv.ev("k=>__J.stores(k)", keys)
                    gp = dv.ev("()=>Object.fromEntries(Object.entries(GP))")
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}')
                    bd = body.get('data', {})
                    same = {k: before.get(k) == after.get(k) for k in keys}
                    ok = h1 == h0 + 1 and all(gp.get(n) == md(n) for n in NOS) and all(same.values()) \
                        and len(((after.get('status') or {}).get('5') or {}).get('h') or []) == h1 \
                        and all((bd.get('gpt') or {}).get(n) == md(n) for n in NOS) and len(((bd.get('status') or {}).get('5') or {}).get('h') or []) == h1
                    R(eng, '기록 있는 기기 — 동기화 뒤 GP[149]·GP[84] = 재료 · 다른 칸 무변 · 내 새 칸(5번 △ 진짜 누름) 안 덮임 · 올린 몸통에 셋 다', ok, None,
                      {'다른 칸': [k for k in keys if not same[k]], '칸 수': len(keys), 'GP': {n: len(gp.get(n) or '') for n in NOS}, '5번 회독': [h0, h1]})
                finally:
                    dv.close()
                # 내 것이 더 새것 — 적재 전 기록 기기에서 149 Claude 창에 써서 저장(진짜 누름 · 원격 도장보다 뒤) → 적재 뒤 원격을 받아도 안 덮인다
                dv = dv_open(br, eng, app, 'earth', rb, sn)
                try:
                    MY = '내가 먼저 쓴 149번(검산)'
                    dv.ev("n=>__C.open(n)", 149); click(dv, '#tGpt'); dv.pg.wait_for_timeout(700)
                    dv.pg.locator('#gpIn').fill(MY); click(dv, '#gpSave'); dv.pg.wait_for_timeout(700)
                    dv.ev("()=>__C.closeSheets()"); dv.ev("()=>{try{closeView()}catch(e){}}"); dv.ev("()=>__J.sync()")
                    dv.load(app, SPD, 'earth', rec={'earth/기록.json': rn}, static=sn); dv.ev(CJS)
                    dv.ev("()=>__J.sync()"); dv.pg.wait_for_timeout(800)
                    g = dv.ev("()=>({a:GP[149]||'',b:GP[84]||''})")
                    body = json.loads(dv.ev("p=>__J.lastPut(p)", 'earth/기록.json') or '{}')
                    bg = body.get('data', {}).get('gpt') or {}
                    ok = g['a'] == MY and g['b'] == md('84') and bg.get('149') == MY and bg.get('84') == md('84')
                    R(eng, '내 것이 더 새것 — 원격 도장 뒤에 고친 GP[149] 는 원격이 못 덮는다(본판 §B-6 = claude_slot CL-6 ⓒ 잣대) · GP[84] 는 받는다 · 올린 몸통도 그대로', ok, None,
                      {'149': g['a'][:24], '84 길이': len(g['b']), '올린 149': (bg.get('149') or '')[:24], '올린 84 길이': len(bg.get('84') or '')})
                finally:
                    dv.close()
            finally:
                br.close()
    # 앱 무변 · 생물 gpt 무변
    R('-', 'jagwa/index.html 바이트 무변(작업트리 = HEAD)', wt == app, None, hashlib.md5(wt).hexdigest()[:8])
    if how.startswith('적재 뒤'):
        fs = HU.git(SPD, 'diff', '--name-only', SEED_REV + '~1', SEED_REV).decode('utf-8').split()
        R('-', '적재 커밋 %s 이 건드린 파일 = earth/기록.json 하나(물리·생물 기록 무변)' % SEED_REV, fs == ['earth/기록.json'], None, fs)
    # ★ 2026-10-01 claude_p002·claude_e004 — 뒤 판이 phys 에 97 · earth 에 111 을 끝에 더한다. 「= {"phys":[72],"earth":[149,84]}」 는 값을 박은 잣대라
    #   → 「earth 가 [149, 84] 로 시작(차례 그대로) · phys 맨 앞 72」 로 갈음(바탕 2998b9e = earth 없음 → FAIL 그대로)
    jx, jy = json.loads(sn['motion/index.json']), json.loads(sb['motion/index.json'])
    R('-', 'motion/index.json — earth 가 [149, 84] 로 시작(차례 그대로) · phys 맨 앞 72', (jx.get('earth') or [])[:2] == [149, 84] and (jx.get('phys') or [])[:1] == [72],
      (jy.get('earth') or [])[:2] == [149, 84] and (jy.get('phys') or [])[:1] == [72], sn['motion/index.json'].decode())
    for no in NOS:
        f = 'motion/earth_%s.html' % no
        src = open(os.path.join(MAT, 'earth_%s.html' % no), 'rb').read()
        # ★ A-6(d) 9/30 _task_qa_baseline — 줄끝만 뺀 바이트로 맞댄다: 새로 만든 작업트리(qa 워크트리 · core.autocrlf)는 CRLF 로 풀려(18,745 = 18,515 + 230) · git blob = 재료(LF) 그대로
        R('-', '%s = 재료 바이트(md5 %s)' % (f, hashlib.md5(src).hexdigest()[:8]), (sn.get(f) or b'').replace(b'\r\n', b'\n') == src.replace(b'\r\n', b'\n'), None, len(sn.get(f) or b''))
        tx = (sn.get(f) or b'').decode('utf-8', 'replace')
        ext = re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', tx)
        R('-', '%s — 바깥 스크립트 0 · 바깥 주소 = Google Fonts 뿐 · .pdf 0(공개 genie)' % f,
          not re.search(r'<script[^>]*\bsrc\s*=', tx) and all(u.startswith('https://fonts.googleapis.com/') for u in ext) and '.pdf' not in tx.lower(), None, ext)
    R('-', 'motion 폴더에 .pdf 0', not [k for k in sn if k.lower().endswith('.pdf')], None, sorted(sn))
    npass = sum(1 for r in ROWS if r[2]); nfail = sum(1 for r in ROWS if not r[2])
    print('\n== PASS %d · FAIL %d · %.0f초 · 기록 %s' % (npass, nfail, time.time() - t0, how))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · claude_e001(+add1+add2) CE1 · 기록 %s · genie HEAD %s · 바탕 %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), how,
                HU.git(GENIE, 'rev-parse', '--short', 'HEAD').decode().strip(), BASE_REV, ','.join(ENGS)))
        for eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1200]))
        f.write('== PASS %d · FAIL %d\n' % (npass, nfail))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
