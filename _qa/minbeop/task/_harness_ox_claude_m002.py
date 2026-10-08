# -*- coding: utf-8 -*-
"""민법OX Claude 답에 M002 더하기(데이터만) — _task_ox_claude_m002 §C(C1~C8).

  앱   = genie HEAD(7b9e214 · 앞 판 Claude 칸 · 이 판은 앱 코드 무접촉)
  NEW  = studyplandata origin/main 의 minbeop/claude.json(**push 한 원격 blob** · M001+M002)
  BASE = 앞 커밋 ac1b7d06 의 같은 파일(M001 하나) — 헛잣대
  엔진 = playwright webkit · chromium · 아이패드 1024×768 · 진짜 터치(앞 판 하네스 `_harness_ox_claude_answers` 의 도구를 그대로 쓴다)

쓰기 : python _harness_ox_claude_m002.py
"""
import hashlib, importlib.util, io, json, os, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('hca', os.path.join(HERE, '_harness_ox_claude_answers.py'))
h = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(h)
import _qa_common as QC   # noqa: E402 — _task_qa_slim2(10/8) 실행 모드 --mode gate|regress|smoke(없으면 gate = 이 판 앞과 같음) · 이 파일엔 5줄 머리가 없어 _harness_ox_claude_answers(그 머리가 _roots 자리를 sys.path 에 넣음)를 부른 바로 뒤에 둔다 · 이 파일은 인자를 안 읽는다
from playwright.sync_api import sync_playwright

SPD = h.SPD
WORK = os.path.join(tempfile.gettempdir(), 'h_claude_m002')
WANT_MD5, WANT_LEN = '459c976db3a5ef15a89354f41d56a470', 3996
ORANGE, GRAY = 'rgb(180, 83, 9)', 'rgb(107, 114, 128)'
EXTRA = r"""() => {
  const txt = n => (n ? n.textContent : '').replace(/\s+/g, ' ').trim();
  __HZT.tbl = function (uid) {
    const w = document.getElementById('oxwin-cl-' + uid), t = w && w.querySelector('[data-clmdbox] table');
    if (!t) return JSON.stringify(null);
    const rows = [...t.querySelectorAll('tr')];
    return JSON.stringify({ head: [...rows[0].querySelectorAll('th')].map(txt), body: rows.slice(1).map(r => r.querySelectorAll('td').length), tables: w.querySelectorAll('[data-clmdbox] table').length });
  };
  __HZT.jnBtnKey = async function (subj, key) {
    document.querySelectorAll('.oxwin').forEach(w => w.remove());
    goHome(); await new Promise(r => setTimeout(r, 200));
    renderDashboard(); await new Promise(r => setTimeout(r, 200));
    const b = [...document.querySelectorAll('button[data-jn]')].find(x => (x.getAttribute('onclick') || '').indexOf("openJeongni('" + subj + "','" + key + "'") >= 0);
    if (!b) return JSON.stringify(null);
    b.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 150));
    const r = b.getBoundingClientRect();
    return JSON.stringify({ cx: r.left + r.width / 2, cy: r.top + r.height / 2, on: r.width > 0 && r.top >= 0 && r.bottom <= innerHeight });
  };
  __HZT.jnRows = function (uid) {
    const w = [...document.querySelectorAll('.oxwin')].find(x => /^oxwin-jn-/.test(x.id));
    if (!w) return JSON.stringify({ jn: false });
    const rows = [...w.querySelectorAll('[data-jnrow]')];
    const vis = r => [...r.querySelectorAll('[data-clchip]')].filter(c => !c.hidden && c.tagName === 'BUTTON');
    const r0 = rows.find(r => r.getAttribute('data-jnrow') === uid);
    const ans = r0 ? [...r0.querySelectorAll(':scope > button')].find(b => /정답·해설/.test(txt(b))) : null;
    const chip = r0 ? vis(r0)[0] : null;
    return JSON.stringify({ jn: true, sub: txt(w.querySelector('.oxwin-head')), rows: rows.length,
      withChip: rows.filter(r => vis(r).length).map(r => r.getAttribute('data-jnrow') + ' ' + vis(r).map(txt).join(',')),
      main: r0 ? { chip: chip ? txt(chip) : null, afterAns: !!(chip && ans && chip.previousElementSibling === ans) } : null });
  };
  return true;
}"""


def scenario(s):
    pg, R = s.pg, {}
    R['setup'] = s.js("__HZT.setup(true)")
    pg.evaluate(EXTRA)
    R['load'] = s.js("__HZT.load()")
    R['C2'] = s.js("u=>__HZT.card(u)", 'Q0035')
    R['C2tap'] = s.tap(((R['C2'] or {}).get('btn') or {}).get('at')); pg.wait_for_timeout(300)
    R['C2win'] = s.js("__HZT.win('Q0035')")
    R['C5tbl'] = s.js("u=>__HZT.tbl(u)", 'Q0035')
    R['C5tap'] = s.tap(s.js("([u,sl,t])=>__HZT.winBtn(u,sl,t)", ['Q0035', '[data-clmdbox] button.uid', 'Q0013'])); pg.wait_for_timeout(300)
    R['C5pop'] = s.js("k=>__HZT.hasWin(k)", 'q-Q0013')
    for u in ('Q0013', 'Q0012', 'Q0107', 'Q0014', 'Q0036', 'Q0037', 'Q0089', 'Q0480'):
        R['card_' + u] = s.js("u=>__HZT.card(u)", u)
    R['C6'] = s.js("t=>__HZT.search(t)", '2012다44518')
    R['C7'] = s.js("__HZT.dist()")
    cb = (R['C7'] or {}).get('cBtn') or {}
    R['C7tap'] = s.tap(cb.get('at')); pg.wait_for_timeout(300)
    R['C7after'] = s.js("__HZT.distState()")
    jb = s.js("([a,b])=>__HZT.jnBtnKey(a,b)", ['민법총칙', '1.2'])
    R['C8tapJn'] = s.tap(jb); pg.wait_for_timeout(600)
    R['C8'] = s.js("u=>__HZT.jnRows(u)", 'Q0035')
    R['err'] = s.js("__HZT.errs()")
    return R


def run(eng, cljson):
    h.CLJSON = cljson
    with sync_playwright() as pw:
        br = getattr(pw, eng).launch()
        s, srv, ctx, errs = h.open_page(br, eng, 'NEW', APP, '_m002_' + os.path.basename(cljson))
        try:
            R = scenario(s)
        except Exception as e:
            R = {'exc': str(e)[:600]}
        R['pageerror'] = errs['page']
        br.close(); srv.shutdown()
    return R


def main():
    global APP
    if QC.SMOKE:   # smoke 칸 없음(A-0) — 앱을 띄우기 전에 한 줄 찍고 끝(결과 파일에도)
        print('INFO | smoke 칸 없음 | Claude 답 M002(데이터) 하네스 — smoke 칸 없음(A-0) · 앱 안 띄움', flush=True)
        io.open(os.path.join(HERE, '_harness_ox_claude_m002_result.txt'), 'w', encoding='utf-8').write('INFO | smoke 칸 없음 | Claude 답 M002(데이터) 하네스 — smoke 칸 없음(A-0) · 앱 안 띄움\n')
        sys.exit(0)
    os.makedirs(WORK, exist_ok=True)
    APP = io.open(os.path.join(h.GENIE, h.REL), encoding='utf-8', newline='').read()
    git = lambda *a: subprocess.run(['git', '-C', SPD] + list(a), capture_output=True).stdout
    if QC.GATE:
        QC.sub('git:fetch')
        git('fetch', '-q', 'origin')
        QC.sub('git:show-data', 2)
    newb = git('show', 'origin/main:minbeop/claude.json') if QC.GATE else open(os.path.join(SPD, 'minbeop', 'claude.json'), 'rb').read()   # regress — git fetch · show 0: studyplandata 클론 작업트리 파일(SPD_ROOT · 읽기만 · 사슬이 입력으로 추적)
    oldb = git('show', 'ac1b7d06:minbeop/claude.json') if QC.GATE else b''   # regress — 앞 판 데이터(헛잣대 재료)를 안 읽는다
    pn, po = os.path.join(WORK, 'claude_remote.json'), os.path.join(WORK, 'claude_ac1b7d06.json')
    open(pn, 'wb').write(newb); open(po, 'wb').write(oldb)
    appb = APP.encode('utf-8')
    RES = {}
    for eng in ('webkit', 'chromium'):
        for tag, p in ((('BASE', po), ('NEW', pn)) if QC.GATE else (('NEW', pn),)):   # regress — 새 데이터만(BASE = 앞 판 데이터 ac1b7d06 = 헛잣대 띄움)
            print('… %s/%s' % (eng, tag), flush=True)
            QC.launch('new' if tag == 'NEW' else 'base')
            RES[eng + '/' + tag] = run(eng, p)
    json.dump(RES, io.open(os.path.join(WORK, 'raw.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    L = []
    T = lambda n, c, i=None: L.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + json.dumps(i, ensure_ascii=False)[:700]))
    I = lambda n, v: L.append('INFO | ' + n + ' | ' + json.dumps(v, ensure_ascii=False)[:1200])
    def gg(d, *ks):
        for k in ks:
            if isinstance(d, dict):
                d = d.get(k)
            elif isinstance(d, list) and isinstance(k, int) and -len(d) <= k < len(d):
                d = d[k]
            else:
                return None
        return d
    if QC.GATE:   # C1(push 한 원격 blob md5 = 고정 값) · 헛잣대 재료 md5 · 앱 무접촉(작업트리 · 고정 blob) — 그 판에만 뜻 = 관문만
        T('C1 studyplandata 원격(origin/main) minbeop/claude.json — %d B · md5 %s' % (len(newb), hashlib.md5(newb).hexdigest()),
          len(newb) == WANT_LEN and hashlib.md5(newb).hexdigest() == WANT_MD5, [len(newb), hashlib.md5(newb).hexdigest()])
        T('헛잣대 재료 ac1b7d06 = 앞 판 배달본(2,048 B · 81bfe236…)', len(oldb) == 2048 and hashlib.md5(oldb).hexdigest() == '81bfe23658ede9aef3a876e9ebde387c')
        T('앱 코드 무접촉 — genie 작업트리 깨끗 · 앱 = Pages 실물과 같은 blob(1,087,059 B · a32b4202…)',
          subprocess.run(['git', '-C', h.GENIE, 'status', '--porcelain'], capture_output=True).stdout.strip() == b''
          and len(appb) == 1087059 and hashlib.md5(appb).hexdigest() == 'a32b4202635387d0b76321bf1444fcd9', [len(appb), hashlib.md5(appb).hexdigest()])
    else:
        I('regress — claude.json = studyplandata 클론 작업트리(git fetch · show 0 · 크기 · md5 앞 8)', [len(newb), hashlib.md5(newb).hexdigest()[:8]])
    for eng in ('webkit', 'chromium'):
        n, b = RES.get(eng + '/NEW') or {}, RES.get(eng + '/BASE') or {}
        p = '[%s] ' % eng
        T(p + '부트 · 문항 %s · 받기 %s · 직접 %s · JS 오류 0' % (gg(n, 'setup', 'q'), gg(n, 'load', 'state'), gg(n, 'load', 'by')),
          gg(n, 'setup', 'q') == 5548 and gg(n, 'load', 'state') == 'ok' and gg(n, 'load', 'by') == {'Q0480': ['M001'], 'Q0035': ['M002']}
          and not n.get('err') and not n.get('pageerror') and not n.get('exc'), [n.get('exc'), n.get('err'), n.get('pageerror'), gg(n, 'load', 'by')])
        c2 = gg(n, 'C2', 'btn') or {}
        T(p + 'C2 Q0035 카드 「✏️ 연결」 앞(%s) 주황 「%s」' % (gg(n, 'C2', 'next'), c2.get('text')),
          c2.get('text') == 'Claude1' and c2.get('color') == ORANGE and gg(n, 'C2', 'next') == '✏️ 연결', n.get('C2'))
        T(p + 'C2 톡 → 창 머리 %s' % gg(n, 'C2win', 'head'),
          n.get('C2tap') is True and gg(n, 'C2win', 'head') == ['M002', '2026-09-22 · 민총 1.2 신의칙', 'Q0035'] and gg(n, 'C2win', 'headUidBtn') is True, n.get('C2win'))
        if QC.GATE:   # 헛잣대(앞 판 데이터 ac1b7d06) — 관문만
            T(p + 'C2 헛잣대(앞 판 데이터) — Q0035 는 회색 「%s」' % gg(b, 'C2', 'btn', 'text'),
              gg(b, 'C2', 'btn', 'text') == 'Claude' and gg(b, 'C2', 'btn', 'color') == GRAY, gg(b, 'C2', 'btn'))
        c3 = {u: gg(n, 'card_' + u, 'btn') or {} for u in ('Q0013', 'Q0012', 'Q0107')}
        T(p + 'C3 Q0013·Q0012·Q0107 카드 — 회색 「Claude」 + 주황 「↩」 %s' % {u: v.get('text') for u, v in c3.items()},
          all(v.get('text') == 'Claude↩' and v.get('color') == GRAY and gg(v, 'kids', 0, 'color') == ORANGE for v in c3.values()), c3)
        I(p + '나머지 언급 문항(Q0014·Q0036·Q0037·Q0089) 단추', {u: gg(n, 'card_' + u, 'btn', 'text') for u in ('Q0014', 'Q0036', 'Q0037', 'Q0089')})
        T(p + 'C3+ 언급 일곱 모두 「Claude↩」(Q0014·Q0036·Q0037·Q0089 포함)',
          all(gg(n, 'card_' + u, 'btn', 'text') == 'Claude↩' for u in ('Q0013', 'Q0014', 'Q0012', 'Q0037', 'Q0036', 'Q0089', 'Q0107')),
          {u: gg(n, 'card_' + u, 'btn', 'text') for u in ('Q0013', 'Q0014', 'Q0012', 'Q0037', 'Q0036', 'Q0089', 'Q0107')})
        if QC.GATE:   # 합침→_harness_ox_claude_answers:G1(같은 카드를 더 엄하게 — 11px · 테두리 0 · 높이 ±1.5 · 두 엔진) — regress 에서 끔
            T(p + 'C4 Q0480 카드 — 여전히 「%s」(M001 그대로)' % gg(n, 'card_Q0480', 'btn', 'text'),
              gg(n, 'card_Q0480', 'btn', 'text') == 'Claude1' and gg(n, 'card_Q0480', 'btn', 'color') == ORANGE, gg(n, 'card_Q0480', 'btn'))
        t5 = n.get('C5tbl') or {}
        T(p + 'C5 창 본문 표 — 머리 %s · 몸 %s' % (t5.get('head'), t5.get('body')),
          t5.get('head') == ['갈래', '묻는 것', '답', '근거'] and t5.get('body') == [4, 4, 4] and t5.get('tables') == 1, t5)
        T(p + 'C5 창 본문 Q0013 톡 → openQPopup(\'Q0013\')', n.get('C5tap') is True and n.get('C5pop') is True, [n.get('C5tap'), n.get('C5pop')])
        s6 = n.get('C6') or {}
        T(p + 'C6 근거 검색 「2012다44518」 → %s · %s · 딱지 %s (앞 판 데이터 %s)' % (s6.get('count'), gg(s6, 'rows', 0, 'id'), gg(s6, 'rows', 0, 'badges'), gg(b, 'C6', 'count')),
          gg(s6, 'rows', 0, 'id') == 'Q0035' and 'Claude' in (gg(s6, 'rows', 0, 'badges') or []) and s6.get('count') == '1건' and (gg(b, 'C6', 'count') == '0건' if QC.GATE else True), [s6, b.get('C6')])   # regress — 「앞 판 데이터 0건」 조건은 헛잣대 몫(뗌)
        d7, a7 = n.get('C7') or {}, n.get('C7after') or {}
        T(p + 'C7 단원 목록 머리 「…%s」 (앞 판 데이터 「…%s」)' % ((d7.get('head') or '')[-12:], (gg(b, 'C7', 'head') or '')[-12:]),
          (d7.get('head') or '').endswith(' · C2') and gg(d7, 'cBtn', 't') == 'C2' and ((gg(b, 'C7', 'head') or '').endswith('· C1') if QC.GATE else True), [d7.get('head'), gg(b, 'C7', 'head')])   # regress — 「앞 판 데이터 · C1」 조건은 헛잣대 몫(뗌)
        T(p + 'C7 C2 톡 → 단원 둘 %s' % a7.get('clUnits'),
          n.get('C7tap') is True and a7.get('units') == 2 and sorted(a7.get('clUnits') or []) == ['민법총칙 · 1.2 신의칙 C1', '민법총칙 · 4. 권리의 객체 C1'], a7)
        j8 = n.get('C8') or {}
        T(p + 'C8 정리 창 1.2 신의칙(%s행) — Q0035 행 「정답·해설 ▸」 바로 뒤 「%s」 · C 칩은 이 행 하나' % (j8.get('rows'), gg(j8, 'main', 'chip')),
          n.get('C8tapJn') is True and j8.get('jn') is True and gg(j8, 'main', 'chip') == 'C1' and gg(j8, 'main', 'afterAns') is True
          and [x for x in (j8.get('withChip') or []) if ' C' in x] == ['Q0035 C1'], j8)
        I(p + 'C8 칩이 선 행(§D 규칙 — 직접 C · 언급 ↩)', j8.get('withChip'))
    for l in L:
        print('   ' + l)
    pp = sum(1 for l in L if l.startswith('PASS')); f = sum(1 for l in L if l.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (pp, f))
    io.open(os.path.join(HERE, '_harness_ox_claude_m002_result.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n\n합계  PASS %d · FAIL %d\n' % (pp, f))
    sys.exit(0 if not f else 1)


if __name__ == '__main__':
    main()
