# -*- coding: utf-8 -*-
r"""_task_jo_toc_fuse_add1 §C 관문 — 1차객 🔍 검색 결과 누름 = 지문 팝업(민법 문항 팝업 그대로)

  NEW  = --new <파일>(없으면 genie 작업트리 jo/index.html) · BASE = genie HEAD(f497f05 · md5 6db2c79a)
  데이터 = genie 작업트리 jo/data(BASE·NEW 같은 데이터)
  헛잣대 = BASE 에서 FAIL(관문 규칙 3) · C2 는 「popCard 만 부르는 시안」(바탕 + r.onclick 한 줄) 에서도 FAIL 이어야 한다
  누름 = page.mouse.click(x, y) · 글자 = page.type(진짜 키) · 보임 = display ≠ none 그리고 높이 > 0
쓰기 : python _harness_jo_toc_fuse_add1.py [--new 파일] [--out 폴더]
"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _harness_jo_toc_fuse as HT          # noqa: E402 — 같은 서버·쪽(Pg)·도구(__HT)
import _qa_jo_common as QJ   # noqa: E402 — _task_qa_slim(10/4) A-1 · HT(toc_fuse)가 먼저 QJ 를 불러 --mode · --snap-in · --snap-out 을 뗐다 · gate = 인자 없음 = 이 판 앞과 같다
from playwright.sync_api import sync_playwright   # noqa: E402

OUT = HT.ARG('--out', HERE)
RES = HT.RES
Q1 = '공유'
GGW = '토크퓨즈근거말'   # 근거 모드 검색어(하네스가 심는다 · 앱 글에 없는 낱말)


def T(g, n, ok, d=''):
    HT.T(g, n, ok, d)


def scen(br, src, tag):
    g = '%s 책상' % tag
    p = HT.Pg(br, tag, src, 1440, 700)

    def sec(name, fn):
        try:
            fn()
        except Exception as ex:
            T(g, name + ' 묶음 예외', False, repr(ex)[:400])

    def search(q):
        p.ev("async()=>await __HT.home()")
        at = p.ev("()=>__HT.srInput()")
        p.pg.mouse.click(at['cx'], at['cy']); p.pg.wait_for_timeout(150)
        p.pg.keyboard.press('Control+A'); p.pg.keyboard.press('Delete')
        p.pg.type('input[placeholder="검색어를 입력하세요"]', q, delay=25)
        p.pg.wait_for_timeout(700)
        return p.until("()=>{const r=__HT.srRows();return r&&r.rows.length?r:null}", None, 10000)

    def c12():
        rs = search(Q1)
        k = p.ev("()=>__HT.srRowKey(0)")
        st0 = p.ev("()=>__HT.state()")
        at = p.ev("()=>__HT.srRow(0)")
        c = p.click(at, 900)
        qp = p.until("k=>{const q=__HT.qPop(k);return q&&q.vis?q:null}", k, 8000)
        st1 = p.ev("()=>__HT.state()"); rs1 = p.ev("()=>__HT.srRows()"); inp = p.ev("()=>__HT.srInput()")
        T(g, 'C1 「%s」 → 결과 첫 줄 mouse.click → 그 지문 팝업(.pop.mbqp) 보임 · 결과 목록 보임 · 검색 칸 「%s」 · S.mok·S.tab 무변(헛잣대: 바탕은 단원으로 감)' % (Q1, Q1),
          c and bool(qp) and qp['mbqp'] and bool(rs1) and rs1['vis'] and len(rs1['rows']) == len(rs['rows']) and (inp or {}).get('v') == Q1 and
          st1['mok'] == st0['mok'] == '' and st1['tab'] == st0['tab'] == 'jimun' and st1['jt'] == 'ox',
          {'key': k, 'pop': qp, '목록': rs1 and [rs1['vis'], len(rs1['rows'])], 'q': inp and inp.get('v'), 'mok': [st0['mok'], st1['mok']], 'tab': st1['tab']})
        if tag == 'NEW' and QJ.GATE:
            p.shot('NEW_C1_popup')
        if QJ.SMOKE:   # smoke — C1 · Z 만(C2 · C4 · C3 · C5 는 안 잰다)
            return
        z0 = (p.ev("k=>__HT.qPop(k)", k) or {}).get('z', 0)
        p.ev("()=>{const p=POPS[POPS.length-1];return 1}")
        # 다른 창을 하나 더 띄워 맨 앞을 뺏은 뒤 같은 줄을 다시 누른다(맨 앞으로 오는지)
        k2 = p.ev("()=>__HT.srRowKey(1)")
        p.click(p.ev("()=>__HT.srRow(1)"), 700)
        z1 = p.ev("()=>__HT.maxZ()")
        c2 = p.click(p.ev("()=>__HT.srRow(0)"), 700)
        qp2 = p.ev("k=>__HT.qPop(k)", k)
        T(g, 'C2 같은 결과 줄을 다시 누름 → 팝업이 여전히 보이고(닫히지 않음 · 한 벌) z 가 가장 큼(헛잣대: popCard 만 부르면 닫힘)',
          c2 and bool(qp2) and qp2['vis'] and qp2['n'] == 1 and qp2['z'] >= z1 and qp2['z'] > z0 and k2 != k,
          {'z 처음': z0, '다른 창 뒤 최대': z1, '다시 누른 뒤': qp2})
        # C4 — 이동 단추(단원에 붙은 결과 줄로 — 미분류 리담은 옛 판도 「마디를 찾지 못했다」 토스트)
        p.ev("()=>{try{closeAllPops()}catch(e){}return 1}")
        im = p.ev("()=>__HT.srFirstMg()")
        k = p.ev("i=>__HT.srRowKey(i)", im)
        p.click(p.ev("i=>__HT.srRow(i)", im), 900)
        p.until("k=>{const q=__HT.qPop(k);return q&&q.vis?q:null}", k, 8000)
        go = p.ev("k=>__HT.qPopGo(k)", k)
        exp = p.ev("k=>(MBK2M[k]||{}).sel||null", k)
        c4 = p.click(go, 1200)
        st4 = p.until("m=>__HT.state().mok===m?__HT.state():null", exp, 10000)
        qp4 = p.ev("k=>__HT.qPop(k)", k)
        T(g, 'C4 팝업 「↪ 이 지문으로 이동」 누름 → 팝업 닫힘 · 그 지문 단원(%s)으로 이동(지금 동작 그대로)' % exp,
          c4 and bool(st4) and (qp4 is None or not qp4['vis']), {'mok': p.ev("()=>__HT.state()")['mok'], 'pop': qp4})

    def c3():
        p.ev("async()=>await __HT.home()")
        k = p.ev("()=>__HT.longP7(500)")
        NL = chr(10)
        p.ev("([k,t])=>__HT.seedGG(k,t)", [k, GGW + ' — 하네스가 심은 긴 근거(팝업 몸통을 굴려 이 근거 줄이 몸통 위로 오는가)' + NL +
              NL.join('근거 %d번째 줄 — 긴 근거라야 몸통을 굴려 윗변을 맞출 자리가 생긴다' % i for i in range(1, 41))])
        sy0 = p.ev("()=>scrollY")
        gb = p.ev("async()=>{const b=[...document.querySelectorAll('.mbsr .mbsb')].find(x=>x.textContent.indexOf('근거')>=0);return b?__HT.hitOn(b):null}")
        p.click(gb, 700)
        p.until("()=>S.oxQMode==='g'&&MBSR&&MBSR.box&&MBSR.box.isConnected", None, 8000)
        at = p.ev("()=>__HT.srInput()")
        p.pg.mouse.click(at['cx'], at['cy']); p.pg.wait_for_timeout(100)
        p.pg.keyboard.press('Control+A'); p.pg.keyboard.press('Delete')
        p.pg.type('input[placeholder="검색어를 입력하세요"]', GGW, delay=25); p.pg.wait_for_timeout(700)
        p.until("()=>{const r=__HT.srRows();return r&&r.rows.length?r:null}", None, 10000)
        kk = p.ev("()=>__HT.srRowKey(0)")
        sy1 = p.ev("()=>scrollY")
        c = p.click(p.ev("()=>__HT.srRow(0)"), 900)
        p.until("k=>{const q=__HT.qPop(k);return q&&q.vis?q:null}", kk, 8000)
        p.pg.wait_for_timeout(300)
        sc = p.ev("k=>__HT.qPopScroll(k)", kk)
        sy2 = p.ev("()=>scrollY")
        top_ok = bool(sc) and sc['gg'] and sc['off'] is not None and 0 <= sc['off'] <= 16
        end_ok = bool(sc) and sc['gg'] and sc['off'] is not None and sc['st'] > 0 and sc['st'] >= sc['sh'] - sc['ch'] - 1 and 0 <= sc['off'] and sc['off'] + sc['ggh'] <= sc['bodyH']
        T(g, 'C3 「🔗 근거」 모드 · 글이 긴 지문(%s) 누름 → 팝업 몸통만 굴려 근거 줄(.ggbox)이 몸통 안에 보임 — 윗변 몸통 위 0~16px, 뒤 글이 짧으면 굴림 끝(scrollTop 최대)에서 멈춤 · 뒤 페이지 scrollY 무변(헛잣대: 바탕 팝업 없음 · 시안 굴림 0 → 근거 줄이 몸통 밖)' % kk,
          c and kk == k and (top_ok or end_ok) and sy2 == sy1,
          {'scroll': sc, '윗변 0~16': top_ok, '굴림 끝': end_ok, 'scrollY': [sy0, sy1, sy2]})
        if tag == 'NEW' and QJ.GATE:
            p.shot('NEW_C3_gg')

    def c5():
        p.ev("async()=>await __HT.home()")
        p.ev("async()=>{await popPan('90후250','',{clientX:700,clientY:200});return 1}")
        p.pg.wait_for_timeout(1500)
        at = p.ev("()=>{const r=[...document.querySelectorAll('.pop .lnkrow')].find(x=>x.offsetParent);return r?__HT.hitOn(r):null}")
        n0 = len(p.ev("()=>__HT.popsInfo()"))
        c1 = p.click(at, 800)
        n1 = p.ev("()=>__HT.popsInfo()")
        at2 = p.ev("()=>{const r=[...document.querySelectorAll('.pop .lnkrow')].find(x=>x.offsetParent);return r?__HT.hitOn(r):null}")
        c2 = p.click(at2, 800)
        n2 = p.ev("()=>__HT.popsInfo()")
        qk = [x['k'] for x in n1 if x['k'] and x['k'].startswith('q|📝 지문 ')]
        T(g, 'C5 판례 팝업 「같은 지문」 줄 누름 → 지문 팝업 · 다시 누름 → 닫힘(popCard 토글 그대로)',
          c1 and c2 and len(n1) == n0 + 1 and bool(qk) and not any(x['k'] == qk[0] for x in n2), {'창 수': [n0, len(n1), len(n2)], '지문 창': qk[:1]})

    for nm, fn in (('C1·C2·C4', c12), ('C3', c3), ('C5', c5)):
        if QJ.SMOKE and nm != 'C1·C2·C4':
            continue
        sec(nm, fn)
    es = p.errs_all()
    T(g, 'Z 페이지 오류 0', not es, es[:5])
    p.close()


def report():
    head = ['# _harness_jo_toc_fuse_add1 결과 — %s' % time.strftime('%Y-%m-%d %H:%M'),
            'NEW = %s (md5 LF %s) · BASE = genie %s (md5 %s) · 시안(바탕 + popCard 한 줄) · 데이터 = %s' % (
                HT.NEWF, hashlib.md5(io.open(HT.NEWF, encoding='utf-8', newline='').read().replace('\r\n', '\n').encode('utf-8')).hexdigest()[:8], HT.BASE_REV, HT.BASE_MD5[:8], HT.DATA)]
    lines = []
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False, default=str)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:900]))
    npass = sum(1 for r in RES if r[2] is True and r[0].startswith('NEW'))
    nfail = sum(1 for r in RES if r[2] is False and r[0].startswith('NEW'))
    bfail = sum(1 for r in RES if r[2] is False and not r[0].startswith('NEW'))
    bpass = sum(1 for r in RES if r[2] is True and not r[0].startswith('NEW'))
    head.append('새 판 PASS %d · FAIL %d · 바탕·시안(헛잣대) PASS %d · FAIL %d' % (npass, nfail, bpass, bfail))
    f = os.path.join(OUT, '_harness_jo_toc_fuse_add1_result.txt')
    txt = '\n'.join(head + [''] + lines) + '\n'
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(head))


def main():
    os.makedirs(HT.WORK, exist_ok=True)
    if QJ.GATE:   # regress — 바탕 앱 풀기 · 시안 짓기 0(바탕 · 시안 판은 헛잣대 몫 · gate 만)
        QJ.sub('git:show-app')
        base_src = HT.git('show', 'f497f05:jo/index.html').decode('utf-8')   # A-6(d) 9/30 — 바탕 앱 = 인도 때 HEAD f497f05(docstring · 인도 결과 머리)
        assert hashlib.md5(base_src.encode('utf-8')).hexdigest() == HT.BASE_MD5
    new_src = io.open(HT.NEWF, encoding='utf-8', newline='').read()
    if QJ.GATE:
        # 시안 — 바탕에 r.onclick 한 줄만(채팅 index_sr.html 과 같은 꼴 · C2 헛잣대)
        b = base_src.replace('\r\n', '\n')
        old = "    r.onclick = () => linkGo(k);\n    box.appendChild(r);\n  });\n  if (hit.length > 200)"
        assert b.count(old) == 1
        sian = b.replace(old, "    r.onclick = ev => popCard(k, ev);\n    box.appendChild(r);\n  });\n  if (hit.length > 200)")
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        if QJ.GATE:   # regress — 바탕(BASE) · 시안(SIAN) 장면은 안 돈다(헛잣대 칸 몫)
            scen(br, base_src, 'BASE')
            scen(br, sian, 'SIAN')
        with QJ.stage('scen NEW'):
            scen(br, new_src, 'NEW')
        br.close()
    report()


if __name__ == '__main__':
    main()
