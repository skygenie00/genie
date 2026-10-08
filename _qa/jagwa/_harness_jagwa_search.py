# -*- coding: utf-8 -*-
r"""_task_jagwa_search §B 관문 — 자과 서재 검색 = 민법OX 꼴

  python _harness_jagwa_search.py [--new <앱>] [--base <앱 | HEAD>] [--eng chromium,webkit] [--only g1,g2,...] [--res <결과>]

  NEW = genie 작업트리 jagwa/index.html · BASE(헛잣대) = genie HEAD(바로 앞 인도판 = jagwa_uid)
  데이터·기록 = studyplandata 작업트리(= 원격과 같음) 를 같은 출처 route 로 · PUT 은 가로채 밖으로 안 나감
  관문마다 NEW 는 PASS, BASE 는 FAIL 이어야 한다(헛잣대 열) — 13·15·16 처럼 바탕도 참인 것은 「바탕 = 기준」 으로 적는다
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자 · 자리 · 개수 · 실제 마우스·손가락 누름
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import io, json, os, re, sys, time, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie(); SPD = _roots.spd()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEF = ARG('--base', 'HEAD')
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_search_result.txt'))
ROWS = []   # (관문, 엔진, 이름, NEW ok, BASE ok, 잰 값)
from playwright.sync_api import sync_playwright   # noqa: E402

SJS = JG.SJS   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)


def R(g, eng, name, okn, okb, val):
    ROWS.append((g, eng, name, okn, okb, val))
    print('%s | 바탕 %s | %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, name,
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:400]), flush=True)


# ── _task_qa_slim2(10/8) regress 도우미 — 이름이 `_rg` · `_RG` 로 시작하는 것 = gate 에서 안 쓰는 갈래(gate 에서 도는 줄은 원래 글 그대로) ──
_RG_SYNCED = "()=>{try{return typeof recBusy!=='undefined'&&!recBusy&&((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}')||{}).lastSync||0)>0}catch(e){return false}}"   # 앱 syncRecords 끝 lsPut(SMETA_KEY,{lastSync}) — 새 문맥이라 첫 동기화 전엔 0


def _rg_load(dv, app, spd, subj, rec=None, static=None):
    """regress — JG.Dev.load 와 같은 걸음(같은 출처 서버 · INIT_HU · JS_HU)이되 고정 대기 둘 → 표지(같은 상한): __J.ready()(DATA · GG_READY) · 첫 기록 동기화 끝(SMETA lastSync · recBusy 거짓)
    (JG 는 고치지 않는다 — JG.Dev.load 에 표지 갈래를 두면 이 사본은 걷는다 · 보고 「뿌리」)"""
    QC.launch('new')
    dv.S.app = app; dv.S.spd = spd; dv.S.rec = dict(rec or {}); dv.S.static = dict(static or {})
    if dv.pg:
        dv.pg.close()
    dv.ctx.clear_cookies()
    dv.pg = dv.ctx.new_page(); dv.pg.set_default_timeout(150000)
    dv.pg.add_init_script(JG.INIT_HU.replace('__SUBJ__', subj))
    dv.pg.on('pageerror', lambda e: dv.errs.append('page: ' + str(e)[:200]))
    dv.pg.goto('http://127.0.0.1:%d/app.html' % dv.S.port, wait_until='load')
    dv.pg.wait_for_function('typeof DATA!=="undefined"&&DATA.length>0', timeout=120000)
    dv.pg.evaluate(JG.JS_HU)
    QC.until(dv.pg, '()=>__J.ready()', 30000, '__J.ready(DATA · GG_READY)')
    QC.until(dv.pg, _RG_SYNCED, 2500, '첫 기록 동기화 끝(SMETA lastSync · recBusy 거짓)')


def open_dev(br, eng, app, subj, phone=False):
    dv = JG.Dev(br, eng, phone)
    dv.load(app, SPD, subj) if QC.GATE else _rg_load(dv, app, SPD, subj)   # regress — 띄움 고정 대기 → 표지
    dv.ev(SJS)
    dv.ev("()=>__J.sync()")
    dv.pg.wait_for_timeout(600) if QC.GATE else QC.sleep(600, '기록 맞춤(__J.sync = syncRecords + 400ms) 뒤 다시 그림 — 끝 표지 없음', dv.pg)
    return dv


def typeq(dv, text, enter=False):
    loc = dv.pg.locator('#q')
    if not loc.is_visible():
        return
    loc.click()
    loc.fill('')
    if text:
        dv.pg.keyboard.type(text, delay=5)
    if enter:
        dv.pg.keyboard.press('Enter')
    dv.pg.wait_for_timeout(250) if QC.GATE else QC.sleep(250, '검색 칸 타자 뒤 앱 거름 · 결과 다시 그림(입력 모으기 — 표지 없음)', dv.pg)


def st(dv):
    return dv.ev("()=>__S.st()")


def click_at(dv, sel_or_js, phone=False):
    r = dv.ev("s=>{const e=typeof s==='string'?document.querySelector(s):null;if(!e)return null;e.scrollIntoView({block:'nearest'});return __S.rect(e)}", sel_or_js)
    if not r:
        return False
    if phone:
        dv.pg.touchscreen.tap(r['cx'], r['cy'])
    else:
        dv.pg.mouse.click(r['cx'], r['cy'])
    dv.pg.wait_for_timeout(500) if QC.GATE else QC.sleep(500, '누름 뒤 앱 반응 — 누른 자리(결과 줄 · ▶ · ◀ · 분포 · 단원 · ! · 모드 · 접기)마다 효과가 달라 공통 표지 없음', dv.pg)
    return True


def both(br, eng, subj, fn, phone=False):
    """같은 관문을 NEW · BASE 에서 — fn(dv, who) → (ok, val)"""
    out = {}
    if QC.REGRESS:   # regress — 바탕 안 띄움(바탕 열 —)
        out['BASE'] = (None, None)
    for who in (('NEW', 'BASE') if QC.GATE else ('NEW',)):
        dv = open_dev(br, eng, APPS[who], subj, phone)
        try:
            out[who] = fn(dv, who)
        except Exception as e:
            out[who] = (False, 'ERR ' + repr(e)[:300])
        finally:
            errs = dv.errs[:]
            dv.close()
        if errs and who == 'NEW':
            out[who] = (False, {'값': out[who][1], '페이지 오류': errs[:3]})
    return out['NEW'], out['BASE']


def gate(g, eng, name, subj, fn, phone=False):
    if ONLY and g not in ONLY:
        return
    if not QC.want(g, smoke=g == 'g1'):   # smoke — g1(생물 「플라스미드」 · 검색 핵심) 하나
        return
    (okn, vn), (okb, vb) = both(HU_BR[0], eng, subj, fn, phone)
    R(g, eng, name, okn, okb, {'NEW': vn, 'BASE': vb})


# ── 관문 ──
def g1(dv, who):
    c0 = dv.ev("()=>__S.cnt()")
    typeq(dv, '플라스미드')
    s = st(dv)
    ok = s['cnt'] == c0 and s['esVis'] and re.fullmatch(r'\d+건', s['qcnt'] or '') is not None and s['n'] > 0 and s['n'] == int((s['qcnt'] or '0건')[:-1])
    return ok, {'목록 전': c0, '목록 뒤': s['cnt'], '개수': s['qcnt'], '줄': s['n']}


def g2(dv, who):
    typeq(dv, '자체 복제원점')
    s = st(dv)
    r = [x for x in s['rows'] if x['chat']]
    ok = s['n'] >= 1 and bool(r) and r[0]['lab'] in ('해설', '해설2') and r[0]['marks'] == 1
    return ok, {'개수': s['qcnt'], '줄': s['rows'][:2]}


def g3(dv, who):
    out = {}
    # 옛 줄: dv.ev("()=>{const r=DATA.find(x=>!noteOf(x[F.NO])&&String(x[F.BODY]).length>20);CMT[r[F.NO]]='검산용코멘트말씨하나 둘 셋 넷 다섯';return r[F.NO]}")
    # ★ uid_unify §A-1(10/5) — 카드 층 메모리 dict 는 uid 열쇠(qk) · 번호로 심으면 noteOf 가 못 봄(cand_v 에서 g3 「코멘트 표본 없음」)
    dv.ev("()=>{const r=DATA.find(x=>!noteOf(x[F.NO])&&String(x[F.BODY]).length>20);CMT[typeof qk==='function'?qk(r[F.NO]):r[F.NO]]='검산용코멘트말씨하나 둘 셋 넷 다섯';return r[F.NO]}")
    for lab in ('선택지', '보기', '해설', '해설2', '보기 설명', '참고', '코멘트'):
        sm = dv.ev("l=>__S.sample(l)", lab)
        if not sm:
            out[lab] = '표본 없음'; continue
        typeq(dv, sm['q'])
        s = st(dv)
        me = [x for x in s['rows'] if x['no'] == sm['no']]
        out[lab] = {'말': sm['q'], '문항': sm['code'], '건': s['qcnt'], '칸': me[0]['lab'] if me else None}
    # 〈보기〉 글은 두 과목 모두 본문에도 다 들어 있다(데이터 실측 1,235 줄 · 〈보기〉에만 있는 것 0) — 〈보기〉만 걸리는 말이 없어 표본 없음이 맞다
    ok = all(isinstance(v, dict) and v['칸'] == k for k, v in out.items() if k != '보기') and out.get('보기') == '표본 없음'
    return ok, out


def g4(dv, who):
    res = {}
    for q, want in (('B205705', 'B20-57-05'), ('B20-57-05', 'B20-57-05'), ('b20 57 05', 'B20-57-05'), ('B012T', 'B012T'), ('b012t', 'B012T'), ('G57-05', None), ('G20-57-25', None)):
        typeq(dv, q)
        s = st(dv)
        res[q] = [x['code'] for x in s['rows']][:3] if s['n'] else []
    ok = all(res[q] == [w] for q, w in (('B205705', 'B20-57-05'), ('B20-57-05', 'B20-57-05'), ('b20 57 05', 'B20-57-05'), ('B012T', 'B012T'), ('b012t', 'B012T'))) \
        and res['G57-05'] == [] and res['G20-57-25'] == []
    return ok, res


def g4e(dv, who):
    typeq(dv, 'G1010C')
    s = st(dv)
    return [x['code'] for x in s['rows']] == ['G1-010C'], {'개수': s['qcnt'], '줄': [x['code'] for x in s['rows']][:3]}


def g5(dv, who):
    src = dv.ev("()=>{const r=DATA[__S.byCode('B20-57-05')-1];return r[F.ROUND]+'회 '+r[F.LNO]+'번'}")
    typeq(dv, src)
    s = st(dv)
    return 'B20-57-05' in [x['code'] for x in s['rows']], {'출처': src, '개수': s['qcnt'], '줄': [x['code'] for x in s['rows']][:4]}


def g6(dv, who):
    uo = dv.ev("()=>__S.unitOnly('1.1')")
    typeq(dv, '1.1')
    s = st(dv)
    nos = set(s['nos'] or [])
    bad = [n for n in uo if n in nos]
    return s['esVis'] and not bad, {'단원 코드로만 걸리는 행': len(uo), '그중 결과에 든 것': len(bad), '개수': s['qcnt'], '목록': s['cnt']}


def g7(dv, who):
    typeq(dv, '플라스미드'); n0 = st(dv)['qcnt']
    typeq(dv, '')
    dv.ev("()=>{FL.types=new Set(['G']);FL.past='y';FL.mark='X';const u=DATA.map(r=>unitOf(r[F.NO])).find(Boolean);FL.unit=u||'';draw()}")
    dv.pg.wait_for_timeout(400)
    typeq(dv, '플라스미드')
    s = st(dv)
    return s['qcnt'] == n0 and s['n'] > 0, {'필터 없이': n0, '필터 켜고': s['qcnt'], '목록': s['cnt']}


def g8(dv, who):
    typeq(dv, '플')
    a = st(dv)
    typeq(dv, '플', enter=True)
    b = st(dv)
    typeq(dv, '플라스미드', enter=True)
    c = st(dv)
    ok = (not a['esVis']) and a['qcnt'] == '두 글자 이상 입력하세요' and (not b['esVis']) and b['qcnt'] == a['qcnt'] and c['esVis'] and c['n'] > 0
    return ok, {'한 글자': [a['esVis'], a['qcnt']], 'Enter': [b['esVis'], b['qcnt']], '두 글자 Enter': c['qcnt']}


def g9(dv, who):
    for q in ('다음', '것은', '옳은', '설명'):
        typeq(dv, q)
        s = st(dv)
        if s['nos'] is not None and len(s['nos']) > 100 or (s['qcnt'].endswith('건') and int(s['qcnt'][:-1] or 0) > 100):
            break
    ok = s['n'] == 100 and any('상위 100건만' in x for x in s['note'])
    return ok, {'말': q, '개수': s['qcnt'], '줄': s['n'], '안내': s['note'][-1:] if s['note'] else []}


def g10(dv, who):
    typeq(dv, '플라스미드')
    s = st(dv)
    if not s['n']:
        return False, {'줄': 0}
    nos = s['nos'] or [x['no'] for x in s['rows']]
    first = s['rows'][0]['no']
    click_at(dv, '#esres [data-esq]')
    dv.pg.wait_for_timeout(1200)
    v1 = dv.ev("()=>VNO")
    click_at(dv, '#vNext'); dv.pg.wait_for_timeout(1200)
    v2 = dv.ev("()=>VNO")
    vl = dv.ev("()=>VLIST.slice()")
    outside = dv.ev("n=>n.filter(x=>!DATA[x-1]||!(FL.types&&FL.types.has(kindOf(DATA[x-1])))).length", nos)
    click_at(dv, '#vBack'); dv.pg.wait_for_timeout(600)
    s2 = st(dv); qv = dv.ev("()=>document.getElementById('q').value")
    ok = v1 == first and len(nos) > 1 and v2 == nos[1] and vl == nos and s2['esVis'] and s2['qcnt'] == s['qcnt'] and qv == '플라스미드'
    return ok, {'연 문항': [v1, first], '▶': [v2, nos[1] if len(nos) > 1 else None], 'VLIST = 결과': vl == nos, '필터 밖 갈래 수': outside,
                '닫은 뒤': [qv, s2['esVis'], s2['qcnt']]}


def g11(dv, who):
    N = dv.ev("()=>__S.ggN()"); M = dv.ev("()=>__S.ggUnits()"); K = dv.ev("()=>__S.ggBangN()")
    click_at(dv, '.seg2 [data-sm="g"]')
    typeq(dv, '')
    a = st(dv)
    out = {'N': N, 'M': M, 'K': K, '개수 칸': a['qcnt']}
    ok = a['qcnt'] == '근거 %d개 ▸' % N
    click_at(dv, '#qCnt')
    head = dv.ev("()=>__S.tx(document.querySelector('#esres .esdh'))")
    nun = dv.ev("()=>document.querySelectorAll('#esres .esdr').length")
    out['분포 머리'] = head; out['단원 줄'] = nun
    ok = ok and head.startswith('근거 %d건 · %d개 단원' % (N, M)) and nun == M
    click_at(dv, '#esres .esdr')
    nl = dv.ev("()=>document.querySelectorAll('#esres [data-ggres]').length")
    k0 = dv.ev("()=>__S.tx(document.querySelector('#esres .esdk'))")
    out['단원 문항 줄'] = [k0, nl]
    ok = ok and nl > 0
    click_at(dv, '#esres [data-esback]')
    back = dv.ev("()=>document.querySelectorAll('#esres .esdr').length")
    out['◀ 뒤 단원 줄'] = back
    ok = ok and back == M
    if K:
        click_at(dv, '#esres [data-esbang]')
        hb = dv.ev("()=>__S.tx(document.querySelector('#esres .esdh'))")
        out['! 누름'] = hb
        ok = ok and ('! %d건' % K) in hb
        # WebKit 합성 마우스는 앞 누름 0.5초 안의 다음 누름을 먹는다(바탕 판도 같음 · 이 판과 무관) — 모드 단추 사이 0.8초
        dv.pg.wait_for_timeout(800); click_at(dv, '.seg2 [data-sm="q"]'); m1 = dv.ev("()=>GGMODE")
        dv.pg.wait_for_timeout(800); click_at(dv, '.seg2 [data-sm="g"]'); m2 = dv.ev("()=>GGMODE")
        typeq(dv, ''); qc = dv.ev("()=>__S.tx(document.getElementById('qCnt'))")
        click_at(dv, '#qCnt')
        h2 = dv.ev("()=>__S.tx(document.querySelector('#esres .esdh'))")
        out['문제 모드 갔다 옴'] = h2; out['갔다 옴 자취'] = [m1, m2, qc]
        ok = ok and h2.startswith('근거 %d건' % N)
    return ok, out


def g12(dv, who):
    c = dv.ev("()=>{const r=DATA.find(x=>!isC(x)&&ggOf(GGU(x)).length>0&&x[F.OLDU]);return r?String(codeShow(r)):''}")
    q = c.replace('-', '')
    click_at(dv, '.seg2 [data-sm="g"]')
    typeq(dv, q)
    rows = dv.ev("()=>[...document.querySelectorAll('#esres [data-ggres] .cd')].map(e=>e.textContent)")
    qc = dv.ev("()=>__S.tx(document.getElementById('qCnt'))")
    return c in rows and qc == '%d건' % len(rows), {'번호': c, '말': q, '줄': rows[:3], '개수': qc}


PHQ_JS = r"""()=>{const out=[];const pick=(a)=>{for(const x of a){const v=String(x||'').trim();if(v.replace(/\s+/g,'').length>=2&&!out.includes(v)){out.push(v);return}}};
  const D=DATA;
  pick([D[0][F.CODE]]);pick([String(D[40][F.CODE]).slice(0,4)]);pick([String(D[200][F.CODE]).toLowerCase()]);pick([D[300][F.CODE]]);
  pick([D[10][F.SUB]]);pick([D[120][F.SUB]]);pick([D[400][F.SUB]]);
  [5,77,150,260,333,480].forEach(i=>{const b=String(D[i%D.length][F.BODY]||'').replace(/\s+/g,' ');pick([b.slice(10,15),b.slice(20,24)])});
  pick(['속력']);pick(['전기장']);pick(['15']);pick(['101']);
  const t=D.map(r=>typeOf(r[F.NO])).find(a=>a&&a.length);if(t)pick([t[0]]);
  const g=D.map(r=>String(gptOf(r[F.NO])||'')).find(x=>x.length>8);if(g)pick([g.slice(2,7)]);
  pick([String(D[99][F.VLT]||'')]);pick(['가속도']);pick(['운동량']);
  return out.slice(0,20)}"""


def g13(dv, who):
    Q = dv.ev(PHQ_JS)
    res = {}
    for q in Q:
        if who == 'NEW':
            typeq(dv, q)
            nos = dv.ev("()=>ES_NOS.slice()")
            base = dv.ev("()=>DATA.filter(r=>pass(r)).map(r=>r[F.NO])")   # FL.q 없이 = 지금 필터
            res[q] = sorted(set(nos) & set(base))
            # ★ physprev(10/1) — A-2-3 미리보기 t 에서 걸린 번호(pvHit · 없으면 빈 목록)
            res[q + '·pv'] = dv.ev("q=>(typeof pvHit==='function')?ES_NOS.filter(n=>{const r=DATA.find(x=>x[F.NO]===n);return !!r&&pvHit(r,q)}):[]", q)
            # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 물리 위 검색이 보이는 제목(titleOf)·고친 제목(pnFix)도 찾음 → 그 둘로 걸린 번호(앱 esPhysHit 글에 titleOf(r) 가 있을 때만 · 바탕 7520d46 은 빈 목록)
            res[q + '·tt'] = dv.ev("q=>(typeof esPhysHit==='function'&&String(esPhysHit).indexOf('titleOf(r)')>=0)?ES_NOS.filter(n=>{const r=DATA.find(x=>x[F.NO]===n);return !!r&&(String(titleOf(r)).includes(q)||String(pnFix(r)||'').includes(q))}):[]", q)
            lst = dv.ev("()=>__S.cnt()")
            res[q + '·목록'] = lst
        else:
            res[q] = dv.ev("q=>{FL.q=q;const a=DATA.filter(r=>pass(r)).map(r=>r[F.NO]);FL.q='';return a}", q)
    return True, res


def g14(dv, who):
    dv.ev("()=>{document.body.classList.remove('fold')}")
    typeq(dv, '플라스미드')
    a = dv.ev("()=>{const s=document.querySelector('.esearch')||document.getElementById('q').parentNode,b=document.getElementById('esres');"
              "const rs=s.getBoundingClientRect(),rb=b.getBoundingClientRect();return {sb:rs.bottom,bt:rb.top,bh:rb.height,vis:getComputedStyle(b).display!=='none'&&!b.classList.contains('hide'),"
              "ow:Math.max(0,Math.max(...[b].concat(Array.from(b.querySelectorAll('*'))).map(e=>Math.ceil(e.getBoundingClientRect().right)))-document.documentElement.clientWidth),"
              "pageow:document.documentElement.scrollWidth-document.documentElement.clientWidth}}")   # 결과 상자 안 넘침 · 쪽 전체 넘침(pageow)은 목록 단원 칩의 옛 결함(바탕도 427) 이라 따로 적는다
    click_at(dv, '#fFoldBtn', phone=True)
    b = dv.ev("()=>({fold:document.body.classList.contains('fold'),vis:getComputedStyle(document.getElementById('esres')).display!=='none'})")
    ok = a['vis'] and a['bt'] >= a['sb'] - 1 and a['bh'] > 0 and a['ow'] <= 0 and b['fold'] and not b['vis']
    return ok, {'펼침': a, '접은 뒤': b}


def g15(dv, who):
    if who != 'NEW':
        return None, '—'
    ts = dv.ev("""()=>{const q=document.getElementById('q'),w='플라스미드복제',t=[];
      for(let k=0;k<10;k++){for(let i=1;i<=w.length;i++){q.value=w.slice(0,i);const a=performance.now();esSearch();t.push(performance.now()-a)}}
      t.sort((a,b)=>a-b);return {med:t[t.length>>1],max:t[t.length-1],n:t.length}}""")
    return ts['med'] < 50, ts


APPS = {}
HU_BR = [None]


def main():
    APPS['NEW'] = open(NEWF, 'rb').read().replace(b'\r\n', b'\n')
    # ★ A-6(d) 9/30 _task_qa_baseline — 헛잣대 바탕(기본값 'HEAD')을 인도 앞 판 5e18424(jagwa_uid)로 박는다 — 인도(eb1113e) 뒤 HEAD 의 pass() 는 FL.q 를 안 봐(A-1) g13 「옛 목록 거름」이 577 전부가 된다
    if QC.GATE:   # regress — 바탕(5e18424 git show · --base 파일) 풀기 0
        APPS['BASE'] = JG.git_HU(GENIE, 'show', '5e18424:jagwa/index.html') if BASEF == 'HEAD' else open(BASEF, 'rb').read().replace(b'\r\n', b'\n')
    t0 = time.time()
    with sync_playwright() as pw:
        for eng in (ENGS if not QC.SMOKE else ([e for e in ENGS if e == 'chromium'] or ENGS[:1])):   # smoke — chromium 한 판(g1)
            br = getattr(pw, eng).launch(); HU_BR[0] = br
            try:
                gate('g1', eng, '생물 「플라스미드」 — 목록 문항 수 무변 · 결과 상자 · 「N건」 = 줄 수', 'bio', g1)
                gate('g2', eng, '생물 「자체 복제원점」 — 💬 · 칸 이름 해설/해설2 · <mark> 하나', 'bio', g2)
                gate('g3', eng, '생물 칸마다 하나씩(선택지·해설·해설2·보기 설명·참고·코멘트) — 조각 칸 이름 맞음 · 〈보기〉 = 본문에 다 있어 표본 없음', 'bio', g3)
                gate('g4', eng, 'ID — B205705·B20-57-05·b20 57 05 → B20-57-05 · B012T·b012t → B012T · G57-05·G20-57-25 → 0', 'bio', g4)
                gate('g4', eng, 'ID — 지학 G1010C → G1-010C', 'earth', g4e)
                gate('g5', eng, '출처 — B20-57-05 의 「N회 N번」 → 걸림', 'bio', g5)
                gate('g6', eng, '「1.1」 — 단원 코드로만 걸리던 행 0', 'bio', g6)
                gate('g7', eng, '필터 무시 — 기출만 + 단원 + 틀린 것 켠 채 「플라스미드」 = 관문 1 건수', 'bio', g7)
                gate('g8', eng, '「플」 — 상자 숨김 · 「두 글자 이상 입력하세요」 · Enter 같음', 'bio', g8)
                gate('g9', eng, '100건 — 줄 100 + 안내 줄', 'bio', g9)
                gate('g10', eng, '누름 — 그 문항 · ▶ = 다음 결과 · VLIST = 결과 · 닫은 뒤 글·상자·개수 그대로', 'bio', g10)
                gate('g11', eng, '근거 모드 빈칸 「근거 N개 ▸」 → 분포 → 단원 → ◀ → 「! K」 → 문제 모드 갔다 오면 풀림', 'earth', g11)
                gate('g12', eng, '근거 모드 ID 하이픈 없이 → 걸림 · 「N건」', 'earth', g12)
                if (not ONLY or 'g13' in ONLY) and QC.want('g13'):
                    (okn, vn), (okb, vb) = both(br, eng, 'phys', g13)
                    if QC.REGRESS:   # regress — 바탕(5e18424 · FL.q 로 거른 옛 집합) 자리 = 기준 스냅샷(앞 인도판 새 판의 말마다 걸린 번호) · 아래 비교 규칙(옛 ⊆ 새 · 더 걸린 것 = 미리보기 t · 제목)은 그대로
                        vb = {q: QC.base('g13.%s@%s' % (q, eng), v) for q, v in (vn or {}).items() if not q.endswith(('·pv', '·tt', '·목록'))} if isinstance(vn, dict) else {}
                    # ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2-3: 옛 ⊆ 새 · 더 걸린 문항이 모두 미리보기 t 에서 걸림(pvHit)이면 뜻한 바뀜
                    # 옛 줄: _pv = lambda q: set(vb.get(q) or []) <= set(vn.get(q) or []) and (set(vn.get(q) or []) - set(vb.get(q) or [])) <= set(vn.get(q + '·pv') or [])
                    _pv = lambda q: set(vb.get(q) or []) <= set(vn.get(q) or []) and (set(vn.get(q) or []) - set(vb.get(q) or [])) <= set(vn.get(q + '·pv') or []) | set(vn.get(q + '·tt') or [])   # ★ 2026-10-07 (_task_jagwa_phys_win §A-45) — 더 걸린 것이 미리보기 t 또는 보이는·고친 제목에서 걸렸으면 뜻한 바뀜
                    diff = {q: [vn.get(q), vb.get(q)] for q in vb if vn.get(q) != sorted(vb[q]) and not _pv(q)}
                    pvmore = {q: len(set(vn.get(q) or []) - set(vb.get(q) or [])) for q in vb if vn.get(q) != sorted(vb[q]) and _pv(q)}
                    same_list = len({v for k, v in vn.items() if k.endswith('·목록')}) == 1
                    R('g13', eng, '물리 20말 — 걸린 집합 = 옛 목록 거름 · 목록 안 거름(목록 수 한 값)', not diff and same_list and len(vb) >= 18, None,
                      {'말 수': len(vb), '다른 말': diff, '미리보기로 더 걸림(physprev)': pvmore, '목록 수': sorted({v for k, v in vn.items() if k.endswith('·목록')}), '말': list(vb)})
                gate('g14', eng, '폰 390 — 접힘 열고 검색 → 상자가 검색 줄 밑 · 상자 안 가로 넘침 0 · 접으면 숨음', 'bio', g14, phone=True)
                gate('g15', eng, '타자 빠르기 — 한 글자마다 esSearch 중앙값 < 50ms(PC)', 'bio', g15)
            finally:
                br.close()
    npass = sum(1 for r in ROWS if r[3]); nfail = sum(1 for r in ROWS if not r[3])
    vac = [r for r in ROWS if r[4] is True]
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS) %d · %.0f초' % (npass, nfail, len(vac), time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_search · NEW %s · 바탕 5e18424 · genie HEAD %s · 엔진 %s ====\n' % (time.strftime('%Y-%m-%d %H:%M'), os.path.basename(NEWF),
                JG.git_HU(GENIE, 'rev-parse', '--short', 'HEAD').decode().strip() if QC.GATE else '(regress · git 0)', ','.join(ENGS)))
        for g, eng, n, okn, okb, v in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, eng, n,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:1500]))
        f.write('== PASS %d · FAIL %d · 헛잣대(바탕도 PASS) %d\n' % (npass, nfail, len(vac)))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
