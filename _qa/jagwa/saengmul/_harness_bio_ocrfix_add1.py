# -*- coding: utf-8 -*-
r"""_task_jagwa_bio_ocrfix_add1 §D 관문 — 해설2 머리 · G54-10 · 전각 0 · 다른 칸 무변 · 앱(마우스·손가락) · 멱등

  바탕(헛잣대) = studyplandata 550ee2e5 의 bio/문항.json(본판 인도판 · md5 504af149 — git 에서 꺼내 못 박는다)
  새 값 = 바탕 사본에 _ocrfix_bio.py write 를 두 번(멱등) — 인도 뒤면 studyplandata 로컬 bio/문항.json 과 바이트가 같아야 한다
  앱 = genie 작업트리 jagwa/index.html · 누름 = page.mouse · 손가락 = CDP Input.dispatchTouchEvent(반지름 22) · el.click() 없음
  보임 = computed display ≠ none 이고 높이 > 0
  몸통(서버 · 앱 흉내 網 · __h 도구)은 본판 하네스(_harness_bio_ocrfix.py)를 그대로 불러 쓴다.

쓰기 : python _harness_bio_ocrfix_add1.py [--out 파일]   결과 = _harness_bio_ocrfix_result.txt 끝에 이어 붙인다(--out 이면 그 파일에 새로)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import tempfile   # noqa: E402 — 옛 남 하네스 속성(HU.tempfile · B.WORK)을 갈음
import collections, hashlib, io, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
JG.conf(REFDIR=os.path.join(HERE, '_ocrfix', 'ref'))   # 옛 B 의 REFDIR(같은 폴더 HERE/_ocrfix/ref) — serve_BO 가 읽음 · JG 기본값도 같은 곳


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


OUTF = ARG('--out', os.path.join(HERE, '_harness_bio_ocrfix_result.txt'))
BASE_REV, BASE_MD5 = '550ee2e5', '504af14958a7ec760c717d1f26e646ba'
WORK = os.path.join(os.path.join(tempfile.gettempdir(), 'h_bio_ocrfix'), 'add1'); os.makedirs(WORK, exist_ok=True)
BASEQ, NEWQ = os.path.join(WORK, '문항_base.json'), os.path.join(WORK, '문항_new.json')
T15 = ['G38-07', 'G39-06', 'G39-07', 'G40-01', 'G40-07', 'G41-04', 'G45-01', 'G47-04', 'G50-05', 'G50-10', 'G51-06', 'G51-10', 'G58-02', 'G53-10', 'G54-10']
FWS = '（）、，：；［］｛｝＜＞！'
RES = []


def T(name, ok, detail=''):
    RES.append(('PASS' if ok else 'FAIL', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s | %s' % ('PASS' if ok else 'FAIL', name, d[:300]), flush=True)


def N(name, detail=''):
    RES.append(('NOTE', name, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s | %s' % (name, d[:300]), flush=True)


def cells(r):
    yield '문항', r.get('문항') or ''
    for i, c in enumerate(r.get('선택지') or []):
        yield '선택지%d' % (i + 1), c or ''
    for b in r.get('보기') or []:
        yield '보기%s.내용' % b.get('키'), b.get('내용') or ''
        yield '보기%s.설명' % b.get('키'), b.get('설명') or ''
    yield '해설2', r.get('해설2') or ''
    for j, x in enumerate(r.get('참고') or []):
        yield '참고%d.글' % (j + 1), x.get('글') or ''
    yield '해설', r.get('해설') or ''


APPJS = r"""
Object.assign(window.__h,{
 btn(sel,txt){const c=document.getElementById('card');let e=[...c.querySelectorAll(sel)];if(txt)e=e.filter(x=>__h.tx(x).indexOf(txt)>=0);e=e[0];if(!e)return null;
   e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();const x=r.left+r.width/2,y=r.top+r.height/2;const t=document.elementFromPoint(x,y);
   return {x,y,vis:__h.vis(e),top:t?(t.id||t.tagName.toLowerCase()+'.'+String(t.className&&t.className.baseVal!=null?t.className.baseVal:t.className||'').split(' ')[0]):null}},
 syn(){const c=document.getElementById('card');const d=document.getElementById('cDet');
   const tabs=[...c.querySelectorAll('.soltabs button')].map(b=>({t:__h.tx(b),on:b.classList.contains('on')}));
   const s=[...c.querySelectorAll('.soltx')].filter(x=>!x.hidden&&__h.vis(x));
   const first=s.map(x=>{const h=x.innerHTML.split(/<br\s*\/?>/i)[0];const t=document.createElement('div');t.innerHTML=h;t.querySelectorAll('.tag').forEach(y=>y.remove());return __h.tx(t)});
   return {open:!!(d&&d.open),tabs,first,vis:s.length}},
 bexp(k){const c=document.getElementById('card');const row=[...c.querySelectorAll('.bogi .row')].find(r=>r.dataset.k===k);const e=row&&row.querySelector('.bexp');
   const refs=[...c.querySelectorAll('.ocrref')];return {t:e?__h.tx(e):null,vis:e?__h.vis(e):null,ref:refs.length,refVis:refs.map(__h.vis)}},
 tool(){try{setTool('view')}catch(e){}return typeof TOOL!=='undefined'?TOOL.mode:null}
});
"""


def launch(pw, app, qjson, tag, touch):
    srv, port = JG.serve_BO(app, qjson, 'bio', tag)
    br = pw.chromium.launch()
    kw = dict(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
    if touch:
        kw.update(has_touch=True)
    ctx = br.new_context(**kw)
    ctx.add_init_script(JG.INIT_BO.replace('__SUBJ__', 'bio'))
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%d/app.html' % port, wait_until='load')
    pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=90000)
    pg.wait_for_timeout(2500) if QC.GATE else QC.until(pg, _RG_SYNCED, 2500, '첫 기록 동기화 끝(SMETA lastSync · recBusy 거짓)')   # regress — 같은 상한의 표지
    pg.evaluate(JG.JS_HELP)
    pg.evaluate(APPJS)
    if QC.REGRESS:   # regress — 인도본은 uid 새 꼴 · 하네스 칸은 옛 uid 꼴 → __h.row/show/open/prev/item 이 옛 uid 를 새 uid 로 갈아 부른다(앱 무변)
        pg.evaluate(_RG_OLDU_JS)
    QC.launch('base' if tag.startswith('a1b') else 'new')
    cdp = ctx.new_cdp_session(pg) if touch else None
    return srv, br, pg, cdp, errs


def press(pg, cdp, p):
    if not p:
        return False
    if cdp:
        tp = {'x': p['x'], 'y': p['y'], 'radiusX': 22, 'radiusY': 22, 'id': 1}
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [tp]}); pg.wait_for_timeout(60)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    else:
        pg.mouse.click(p['x'], p['y'])
    pg.wait_for_timeout(500) if QC.GATE else QC.sleep(500, '누름 뒤 앱 반응(정답·해설 펼침 · 탭) — 공통 표지 없음', pg)
    return True


def app_flow(pw, app, qjson, tag, touch):
    srv, br, pg, cdp, errs = launch(pw, app, qjson, tag, touch)
    out = {}
    try:
        out['tool'] = pg.evaluate('()=>__h.tool()')
        for u in ('G45-01', 'G54-10'):
            pg.evaluate('u=>__h.show(u)', u); pg.evaluate('u=>__h.open(u)', u); pg.wait_for_timeout(300)
            d = {}
            p = pg.evaluate("()=>__h.btn('#cDetBtn')")
            d['정답·해설'] = p; press(pg, cdp, p)
            p2 = pg.evaluate("()=>__h.btn('.soltabs button','SYNAPSE')")
            d['SYNAPSE 탭'] = p2
            if p2:
                press(pg, cdp, p2)
            d['syn'] = pg.evaluate('()=>__h.syn()')
            if u == 'G54-10':
                d['ㄷ'] = pg.evaluate("k=>__h.bexp(k)", 'ㄷ')
            out[u] = d
            pg.evaluate("()=>{try{closeView()}catch(e){}}"); pg.wait_for_timeout(200)
        out['err'] = errs + (pg.evaluate('()=>(window.__err||[]).slice(0,5)') or [])
    finally:
        br.close(); srv.shutdown()
    return out


# ── _task_qa_slim2(10/8) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 갈래 ──
_RG_SYNCED = "()=>{try{return typeof recBusy!=='undefined'&&!recBusy&&((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}')||{}).lastSync||0)>0}catch(e){return false}}"   # 앱 syncRecords 끝 lsPut(SMETA_KEY,{lastSync})
_RG_OLDU_JS = r"""()=>{const H=window.__h;if(!H||H.__rgOldu)return 0;const R0=H.row;
  const nu=u=>{const r=R0(u)||((typeof F!=='undefined'&&F.OLDU!==undefined)?DATA.find(x=>x[F.OLDU]===u):null);return r?r[F.CODE]:u};
  H.row=u=>R0(nu(u));['show','open','prev','item'].forEach(k=>{const f=H[k];if(typeof f==='function')H[k]=u=>f(nu(u))});H.__rgOldu=1;return 1}"""   # 옛 uid → 앱 F.OLDU 로 새 uid(F.CODE)


def _rg_app(pw, app):
    """regress — 새 앱 + 인도본(굽기 0) · 마우스 · 손가락(smoke = 마우스만) · 바탕 데이터 판(헛잣대) 안 띄움"""
    qj = _roots.spd('bio', '문항.json')
    A = {'새 마우스': app_flow(pw, app, qj, 'a1n_m', False)}
    if not QC.SMOKE:
        A['새 손가락'] = app_flow(pw, app, qj, 'a1n_t', True)
    return A


def main():
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    if QC.GATE:   # 관문만 — 바탕(550ee2e5 · git show) 땅값 · 굽기(_ocrfix_bio.py write 두 번) · 인도 커밋(b3bb3c3b) 대조
        raw = subprocess.run(['git', '-C', _roots.spd(), 'show', BASE_REV + ':bio/문항.json'], capture_output=True).stdout
        T('땅값 — 바탕 = studyplandata %s bio/문항.json(본판 인도판 · md5 504af149)' % BASE_REV, hashlib.md5(raw).hexdigest() == BASE_MD5, hashlib.md5(raw).hexdigest())
        open(BASEQ, 'wb').write(raw); open(NEWQ, 'wb').write(raw)
        env = dict(os.environ, PYTHONIOENCODING='utf-8', OCRFIX_QJ=NEWQ, OCRFIX_TABLE=os.path.join(HERE, '_ocrfix', 'ocrfix_bio.json'))
        r1 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_bio.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
        b1 = open(NEWQ, 'rb').read()
        r2 = subprocess.run([sys.executable, os.path.join(HERE, '_ocrfix_bio.py'), 'write'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
        b2 = open(NEWQ, 'rb').read()
        now = open(_roots.spd('bio', '문항.json'), 'rb').read()
        T('A-6 쓰기 두 번 = 같은 바이트(멱등) · 왕복 무변 · 검산 OK · 두 번째 「바뀐 칸 0」', b1 == b2 and 'OK  json 왕복 무변' in r1 and '검산 OK' in r1 and '바뀐 칸 0' in r2,
          {'1회': [x for x in r1.splitlines() if x.startswith(('①', '②', '옛 md5'))][:3], '2회': [x for x in r2.splitlines() if '바뀐 칸' in x][:1]})
        # ★ A-6(d) 9/30 — 인도본 = 인도 커밋 b3bb3c3b(add2 인도 · 고침표·스크립트 지금 판으로 다시 만들면 add2 인도본과 같다 · md5 73f4c803) —
        #   뒤 jagwa_uid(studyplandata 4a011475)가 uid 를 새 꼴로 바꿔 로컬 ≠ 재생성(이 칸 전용 now_dl · 「인도 전이면 로컬 = 바탕」 쪽은 그대로)
        now_dl = subprocess.run(['git', '-C', _roots.spd(), 'show', 'b3bb3c3b:bio/문항.json'], capture_output=True).stdout
        T('A-6 인도본(studyplandata b3bb3c3b bio/문항.json · 고침표·스크립트 지금 판의 인도 = add2) = 재생성(바탕 + 스크립트) — 인도 전이면 로컬 = 바탕', now_dl == b1 or now == raw,
          {'인도본': hashlib.md5(now_dl).hexdigest()[:8], '로컬': hashlib.md5(now).hexdigest()[:8], '재생성': hashlib.md5(b1).hexdigest()[:8], '바탕': hashlib.md5(raw).hexdigest()[:8]})
    else:   # regress — 「새 값」 = studyplandata 인도본 bio/문항.json(굽기 0)
        raw = None; now = open(_roots.spd('bio', '문항.json'), 'rb').read(); b1 = now
    D0 = {r['uid']: r for r in json.loads(raw.decode('utf-8'))} if QC.GATE else {}
    D1 = {r['uid']: r for r in json.loads(b1.decode('utf-8'))} if QC.GATE else {(r.get('옛uid') or r['uid']): r for r in json.loads(b1.decode('utf-8'))}   # regress — 인도본(uid 새 꼴)을 옛 uid(칸 · 목록이 쓰는 꼴)로 집는다
    L = json.load(io.open(os.path.join(HERE, '_ocrfix', 'ocrfix_bio_lists.json'), encoding='utf-8'))
    HEAD = L.get('해설2_머리') or {}
    FIXT = json.load(io.open(os.path.join(HERE, '_ocrfix', 'ocrfix_bio.json'), encoding='utf-8'))
    if QC.want('A-data'):   # smoke — 데이터 칸(A-1~A-4) 건넘
        # ── A-1 머리 ──
        first = lambda r: (r.get('해설2') or '').split('⏎')[0]
        bad15 = {u: [first(D1[u]), HEAD.get(u)] for u in T15 if first(D1[u]) != HEAD.get(u)}
        badall = {u: [first(D1[u]), v] for u, v in HEAD.items() if first(D1[u]) != v}
        g0 = lambda D: sum(1 for r in D.values() if '궤' in (r.get('해설2') or '')[:12])
        T('A-1 15 행 해설2 첫 줄 = 원본 머리(수행 결과 표) · 같은 꼴 %d 행 전부 = 목록 · 「궤」로 시작(앞 12자) 0 · G44-01 「궤양」 남음' % len(HEAD),
          not bad15 and not badall and g0(D1) == 0 and '궤양' in (D1['G44-01'].get('해설2') or ''),
          {'15 어긋남': bad15, '전체 어긋남': list(badall)[:5], '궤(새)': g0(D1), 'G44-01 궤양': '궤양' in (D1['G44-01'].get('해설2') or '')})
        N('A-1 15 행 첫 줄(새)', {u: first(D1[u])[:40] for u in T15})
        if QC.GATE:   # 관문만 — 헛잣대(바탕 데이터)
            T('A-1 헛잣대 — 바탕 「궤」로 시작(앞 12자) 13', g0(D0) == 13, g0(D0))
        # ── A-2 G54-10 ──
        g = D1['G54-10']; g_all = (g.get('해설2') or '') + ''.join(b.get('설명') or '' for b in g.get('보기') or [])
        toks = ['돌연변이체 n', '돌연변이체 I', '문제해설']
        ex = lambda s: [t for t in toks if t in s]
        by_cell = {'해설2': (g.get('해설2') or '').count('→ 아래 📎 참고'), '보기ㄷ.설명': next((b.get('설명') or '') for b in g['보기'] if b['키'] == 'ㄷ').count('→ 아래 📎 참고')}
        T('A-2 G54-10 — 해설2·〈보기〉 설명에 「돌연변이체 n」「돌연변이체 I」「문제해설」 0 · 「→ 아래 📎 참고」 칸마다 1(해설2 · ㄷ 설명)',
          not ex(g_all) and by_cell == {'해설2': 1, '보기ㄷ.설명': 1}, {'남은 꼴': ex(g_all), '칸별': by_cell})
        if QC.GATE:   # 관문만 — 헛잣대(바탕 데이터)
            g0a = (D0['G54-10'].get('해설2') or '') + ''.join(b.get('설명') or '' for b in D0['G54-10'].get('보기') or [])
            T('A-2 헛잣대 — 바탕 G54-10 에 셋 다 있음', len(ex(g0a)) == 3, ex(g0a))
        # ── A-3 전각 0 ──
        fwc = lambda D: sum(v.count(c) for r in D.values() for _, v in cells(r) for c in FWS)
        par = []
        for u, r in D1.items():
            for k, v in cells(r):
                if any(v.count(a) != v.count(b) for a, b in (('(', ')'), ('[', ']'), ('{', '}'))):
                    if QC.GATE:
                        r0 = D0[u]; v0 = dict(cells(r0)).get(k, '')
                        if all(v0.count(a) + v0.count(fa) == v0.count(b) + v0.count(fb) for a, b, fa, fb in (('(', ')', '（', '）'), ('[', ']', '［', '］'), ('{', '}', '｛', '｝'))):
                            par.append('%s:%s' % (u, k))
                    else:
                        par.append('%s:%s' % (u, k))   # regress — 짝 틀린 칸 전부(바탕 대조 대신 아래 기준 스냅샷)
        if QC.REGRESS:   # regress — 「새로 틀어진」 = 앞 인도판(기준 스냅샷)에 없던 짝 틀림
            par = sorted(set(par) - set(QC.base('A-3.par', sorted(par)) or []))
        T('A-3 전각 13 글자 모든 대상 칸 0(문항 · 선택지 · 〈보기〉 내용·설명 · 해설2 · 참고 글 · 해설) · 괄호 짝이 새로 틀어진 칸 0', fwc(D1) == 0 and not par, {'새': fwc(D1), '새로 틀어짐': par[:10]})
        if QC.GATE:   # 관문만 — 헛잣대(바탕 데이터)
            T('A-3 헛잣대 — 바탕 대상 칸 전각 450+', fwc(D0) >= 450, fwc(D0))
        left = collections.Counter()
        for r in D1.values():
            for k in ('교재문장', '비고'):
                if isinstance(r.get(k), str):
                    left[k] += sum(r[k].count(c) for c in FWS)
        N('A-3 교재문장 · 비고에 남은 전각 — add1 때는 칸 목록 밖(안 바꿈) · add2(9/28)부터 같은 표로 반각(0 이어야)', dict(left))
        dots = [(u, k, v.count('。')) for u, r in D1.items() for k, v in cells(r) if '。' in v]
        N('A-3 「。」 칸 %d(안 바꿈 · 목록 = ocrfix_bio_lists.json 마침표_목록 · 그림 판독)' % len(dots), dots)
        if QC.GATE:   # 관문만 — 다른 칸 무변(바탕 ↔ 굽기 사본 바이트 대조 · 고침 범위 검사)
            # ── A-4 다른 칸 무변 ──
            fwt = str.maketrans({c: h for c, h in zip(FWS, '(),,:;[]{}<>!')})
            viol = []
            for u, r0 in D0.items():
                r1 = D1[u]; f = FIXT.get(u, {})
                if [k for k in r1 if k != '참고'] != [k for k in r0 if k != '참고']:
                    viol.append((u, '열')); continue
                for k in r0:
                    if k in ('문항', '선택지', '보기', '해설2', '참고', '해설'):
                        continue
                    if k in ('교재문장', '비고'):   # ★ add2(9/28) — 이 두 칸도 반각 바꿈(글자 대 글자)만 받는다
                        if r1[k] != (r0[k].translate(fwt) if isinstance(r0[k], str) else r0[k]):
                            viol.append((u, k))
                        continue
                    if r0[k] != r1[k]:
                        viol.append((u, k))
                exp2 = (f['해설2'] if '해설2' in f else (r0.get('해설2') or '')).translate(fwt)
                if (r1.get('해설2') or '') != exp2 and (r0.get('해설2') or r1.get('해설2')):
                    viol.append((u, '해설2'))
                if (r1.get('해설') or '') != (r0.get('해설') or '').translate(fwt):
                    viol.append((u, '해설'))
                for x0, x1 in zip(r0.get('보기') or [], r1.get('보기') or []):
                    fb = (f.get('보기') or {}).get(x0.get('키')) or {}
                    for fld in ('내용', '설명'):
                        if fld in x0 and x1.get(fld) != fb.get(fld, x0[fld]).translate(fwt):
                            viol.append((u, '보기' + x0.get('키') + fld))
            sq = lambda D: sum((x.get('글') or '').count('■') for r in D.values() for x in r.get('참고') or [])
            T('A-4 다른 칸 무변 — 고침표·반각 밖 바이트 같음(add2 부터 교재문장·비고 = 반각 바꿈만) · 행 746 · 행 차례 · 참고 「■」 무변',
              not viol and len(D1) == 746 and list(D1) == list(D0) and sq(D1) == sq(D0), {'어긋남': viol[:8], '행': len(D1), '■': [sq(D0), sq(D1)]})
    # ── A-5 앱 ──
    app = io.open(_roots.genie('jagwa', 'index.html'), encoding='utf-8', newline='').read()
    with sync_playwright() as pw:
        A = {'새 마우스': app_flow(pw, app, NEWQ, 'a1n_m', False), '새 손가락': app_flow(pw, app, NEWQ, 'a1n_t', True),
             '바탕 마우스': app_flow(pw, app, BASEQ, 'a1b_m', False)} if QC.GATE else _rg_app(pw, app)   # regress — 새 앱 + 인도본 · 바탕 데이터 판 0
    def okapp(a):
        s45 = (a.get('G45-01') or {}).get('syn') or {}
        g54 = (a.get('G54-10') or {}).get('ㄷ') or {}
        f45 = [x for x in (s45.get('first') or []) if x]
        return (bool(s45.get('open')) and any(t['t'] == 'SYNAPSE' and t['on'] for t in s45.get('tabs') or [])
                and f45 == [HEAD.get('G45-01')] and not any('궤' in x for x in f45)
                and g54.get('vis') is True and '아래 📎 참고' in (g54.get('t') or '') and g54.get('ref', 0) >= 1 and all(g54.get('refVis') or [False]))
    for k in (('새 마우스', '새 손가락') if not QC.SMOKE else ('새 마우스',)):   # smoke — 마우스 한 판
        a = A[k]
        T('A-5 앱 [%s] — G45-01 「정답·해설 ▸」 → SYNAPSE 탭 → 첫 줄 「%s」(「궤」 안 보임) · G54-10 〈보기〉 ㄷ 설명 「아래 📎 참고」 보임 · 참고 칸 보임'
          % (k, (HEAD.get('G45-01') or '')[:24]), okapp(a) and not a.get('err'),
          {'G45-01': (a.get('G45-01') or {}).get('syn'), 'G54-10 ㄷ': (a.get('G54-10') or {}).get('ㄷ'), '누른 곳': [(a.get('G45-01') or {}).get('정답·해설'), (a.get('G45-01') or {}).get('SYNAPSE 탭')], 'err': a.get('err')})
    if QC.GATE:   # 관문만 — 헛잣대(바탕 데이터로 연 앱)
        b = A['바탕 마우스']
        bf = ((b.get('G45-01') or {}).get('syn') or {}).get('first') or []
        T('A-5 헛잣대 — 바탕 데이터: G45-01 SYNAPSE 첫 줄 「궤」 · G54-10 ㄷ 설명 「문제해설」', any('궤' in x for x in bf) and '문제해설' in (((b.get('G54-10') or {}).get('ㄷ') or {}).get('t') or ''),
          {'첫 줄': bf, 'ㄷ': ((b.get('G54-10') or {}).get('ㄷ') or {}).get('t')})
    # ── 기록 ──
    lines = ['', '# ─── add1(9/27 · _task_jagwa_bio_ocrfix_add1) — %s ───' % time.strftime('%Y-%m-%d %H:%M'),
             '바탕 = studyplandata %s bio/문항.json(md5 %s) · 새 = 바탕 + _ocrfix_bio.py(md5 %s) · 앱 genie 작업트리 jagwa/index.html md5(LF) %s'
             % (BASE_REV, hashlib.md5(raw).hexdigest()[:8] if QC.GATE else '(regress · 안 읽음)', hashlib.md5(b1).hexdigest()[:8], hashlib.md5(open(_roots.genie('jagwa', 'index.html'), 'rb').read().replace(b'\r\n', b'\n')).hexdigest()[:8]), '']
    for s, n, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s | %s' % (s, n, dd[:900]))
    nf = sum(1 for x in RES if x[0] == 'FAIL')
    lines += ['', 'add1 합계  PASS %d · FAIL %d · NOTE %d  (%.0f초)' % (sum(1 for x in RES if x[0] == 'PASS'), nf, sum(1 for x in RES if x[0] == 'NOTE'), time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    old = '' if ARG('--out') else (io.open(OUTF, encoding='utf-8').read() if os.path.exists(OUTF) else '')
    out = (old.rstrip('\n') + '\n' + txt) if old else txt.lstrip('\n')
    for _ in range(3):
        io.open(OUTF, 'w', encoding='utf-8', newline='\n').write(out); time.sleep(0.5)
        if io.open(OUTF, encoding='utf-8').read() == out:
            break
    print(lines[-1])
    return nf


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
