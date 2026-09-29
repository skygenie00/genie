# -*- coding: utf-8 -*-
"""민법OX 메모 → 근거 흡수 검산 (minbeop/task/_task_ox_memo_merge.md §F).

같은 시나리오를 두 판에 돌린다.
  NEW  = 작업트리 `genie/minbeop/index.html`
  HEAD = git HEAD 판(고치기 전) — **헛잣대**. 같은 게이트가 여기서 몇이 나오는지 나란히 적는다.
실물 = studyplandata 클론 `minbeop/기록.json` 의 data 17키를 **헤드리스 크롬의 빈 프로필** localStorage 에 심는다
(사람 기기의 기록은 읽기만 한다). 網은 막는다(fetch 거절).

쓰기 : python _harness_memo_merge.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'minbeop', 'index.html')
REC = _roots.spd(r"minbeop\기록.json")
# ⚠ 산출·크롬 프로필은 로컬 디스크에 둔다(N: 는 마이박스 — 잇단 쓰기가 이웃 파일을 바꾼 적이 있다)
OUT = os.path.join(tempfile.gettempdir(), 'h_memo_merge')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
G2_TOKENS = ('암기 메모', 'memo-input-', 'link-search-memo-', 'refmemo-')
G9_FUNCS = ('function mergeExcelRecords(', 'async function exportExcelFile(', 'function migrateLegacyRecords(',
            'function refPut(', 'function ggReply(', 'function ggSaveList(',
            'function refTextOf(', 'function refBoxHTML(', 'function refBtnsHTML(', 'function refChipsHTML(',
            'function logicOf(', 'function logicCount(')
CS_LINK_LINE = ('                <button type="button" onclick="ggCsLink(this)" title="이 댓글에서 연결 걸기 — 근거에서 찾기"'
                ' class="ml-auto flex-none self-start text-[11px] leading-4 text-gray-400 hover:text-blue-600">🔗</button>\n')


def head_src():
    r = subprocess.run(['git', '-C', GENIE, 'show', 'HEAD:minbeop/index.html'], capture_output=True)
    assert r.returncode == 0, r.stderr.decode('utf-8', 'replace')
    return r.stdout.decode('utf-8')


def fn_block(text, head):
    """최상위 함수 한 덩이 — 이 파일은 최상위를 8칸 들여쓰고 닫는 괄호도 8칸이다."""
    i = text.index(head)
    ls = text.rfind('\n', 0, i) + 1
    j = text.find('\n', i)
    first = text[ls:j]
    if first.rstrip().endswith('}') and first.count('{') == first.count('}'):
        return first
    end = text.find('\n        }\n', j)
    return text[ls:end + len('\n        }')]


def between(text, a, b, start=0):
    i = text.index(a, start)
    return text[i:text.index(b, i + len(a))]


def md5s(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def build_and_run(tag, src, seed, tests):
    html = src
    k = html.index('<script>', html.index('<body'))          # 앱 스크립트 앞 · meta charset 뒤
    html = html[:k] + seed + html[k:]
    b = html.rindex('</body>')                               # ⚠ </body> 가 둘 — 첫 것은 SheetJS 안 문자열
    html = html[:b] + tests + html[b:]
    app = os.path.join(OUT, 'app_%s.html' % tag)
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)
    prof = os.path.join(OUT, 'prof_%s' % tag)
    shutil.rmtree(prof, ignore_errors=True)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
                        '--user-data-dir=' + prof, '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=20000', '--dump-dom', 'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=300)
    dom = r.stdout.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'dom_%s.html' % tag), 'w', encoding='utf-8').write(dom)
    io.open(os.path.join(OUT, 'stderr_%s.txt' % tag), 'w', encoding='utf-8').write(r.stderr.decode('utf-8', 'replace'))
    m = re.search(r'<pre id="hz-out">(.*?)</pre>', dom, re.S)
    if not m:
        return None
    txt = m.group(1).replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&amp;', '&')
    return [ln for ln in txt.split('\n') if ln.strip()]


def vals(lines):
    out = {}
    for ln in lines or []:
        if ln.startswith('VAL | '):
            _, key, js = ln.split(' | ', 2)
            out[key] = json.loads(js)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    new = io.open(SRC, encoding='utf-8', newline='').read()
    base = head_src()
    rec = json.load(io.open(REC, encoding='utf-8'))
    data = rec['data']

    sk = re.search(r"const SYNC_KEYS = (\[[^\]]*\]);", base).group(1)
    sync_keys = json.loads(sk.replace("'", '"'))

    # ── 원본에서 고르는 표본 (sorted 로 순회를 못박는다)
    memos = data.get('ox_q_memos') or {}
    gg = data.get('ox_q_geunge') or {}
    rl = data.get('ox_q_reflinks') or {}
    logic = data.get('ox_q_logic') or {}
    rl_targets = sorted({t for o in rl for b in ('memo', 'geunge', 'logic') for t in ((rl[o] or {}).get(b) or [])})
    gg_uids = sorted(u for u in gg if gg[u])
    with_cs = [u for u in gg_uids if any((g.get('cs') or []) for g in gg[u]) and u not in memos and u not in rl_targets and u not in rl]
    free = [u for u in gg_uids if u not in memos and u not in rl_targets and u not in rl and u not in with_cs]
    P = {
        'U6': 'Q5001', 'O8': 'Q5002', 'O7': 'Q5003', 'O83': 'Q5004',
        'U8': with_cs[0], 'U7': with_cs[1] if len(with_cs) > 1 else with_cs[0],
        'T82': free[0], 'T83': free[1], 'U83': free[2],
        'UC': 'Q0105' if ('Q0105' in memos and 'Q0105' in gg) else sorted(set(memos) & set(gg_uids))[0],
        'tok': 'ZQ댓글전용',
        'termQ': '더미 지문 Q01',
        'termL': next((str(v).strip()[:4] for k, v in sorted(logic.items()) if len(str(v).strip()) >= 4), '논리'),
        'syncKeys': sync_keys,
    }
    P['termT82'], P['termT83'] = P['T82'].lower(), P['T83'].lower()
    uids = sorted(set(memos) | set(gg_uids) | set(rl) | set(rl_targets) | {'Q5001', 'Q5002', 'Q5003', 'Q5004', 'Q5005'})
    quiz = [{'id': u, 'q': '더미 지문 ' + u + ' 가나다라마바사아자차카타파하', 'exp': '더미 해설 ' + u, 'a': 'O',
             'subject': '민법총칙', 'chapter': '1. 총칙', 'subChapter': '1.1 민법의 법원',
             'displayNo': i + 1, 'probNum': i + 1, 'subNum': '', 'source': '변리사 %02d' % (i % 20),
             'pending': False, 'examMeta': [], 'caseText': '', 'stem': '', 'status': '', 'excelLogic': ''}
            for i, u in enumerate(uids)]
    assert not any(P['tok'] in json.dumps(v, ensure_ascii=False) for v in data.values()), '토큰이 실물에 있다'

    seed_ls = {k: json.dumps(data.get(k) if data.get(k) is not None else {}, ensure_ascii=False, separators=(',', ':'))
               for k in sync_keys}
    seed_ls['ox_uid_migrated'] = '1'      # 구버전 id 이식은 이 판과 무관 — 끈다
    seed_ls['ox_gg_okreset'] = '1'        # 칩 색 한 번 되돌리기(add2 §3)도 끈다 — ok 값이 실물 그대로 남게
    # §B 시동 이관이 붙은 판은 부팅 때 이미 옮긴다 — 확인한 뒤 이 원문으로 되돌려 아래 검사를 옛 차례대로 한다
    P['seedGG'], P['seedRL'] = seed_ls['ox_q_geunge'], seed_ls['ox_q_reflinks']
    P['nLinks'] = len([u for u in rl if ((rl[u] or {}).get('memo') or [])])
    P['nMemo'] = len([u for u in memos if str(memos[u] if memos[u] is not None else '').strip()])
    seed = ('<script>'
            'window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});'
            'window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});'
            'window.fetch=function(){return Promise.reject(new Error("net blocked by harness"))};'
            'localStorage.clear();var __S=' + json.dumps(seed_ls, ensure_ascii=False).replace('</', '<\\/') +
            ';for(var __k in __S)localStorage.setItem(__k,__S[__k]);'
            '</script>')
    # 심는 JSON 안의 `</` 만 가린다(스크립트가 중간에 닫히지 않게). 시험 스크립트 자체는 그대로.
    js_json = lambda v: json.dumps(v, ensure_ascii=False).replace('</', '<\\/')
    tests = TESTS.replace('__QUIZ__', js_json(quiz)).replace('__P__', js_json(P))

    print('표본', json.dumps({k: P[k] for k in ('U6', 'U8', 'O8', 'T82', 'T83', 'U7', 'O7', 'U83', 'O83', 'UC', 'termL')}, ensure_ascii=False))
    print('기록.json savedAt', rec.get('savedAt'), '· ox_q_memos md5(심은 문자열)', md5s(seed_ls['ox_q_memos']))
    print()

    # ── 소스 대조 (파이썬 · 앱을 안 돌린다)
    print('=== G2 소스 토큰 (NEW / HEAD=헛잣대) ===')
    g2 = {t: (new.count(t), base.count(t)) for t in G2_TOKENS}
    for t in G2_TOKENS:
        print('  %-20s NEW %d · HEAD %d' % (t, g2[t][0], g2[t][1]))
    g2_ok = all(v[0] == 0 for v in g2.values())
    print('  G2 : %s' % ('PASS 0회' if g2_ok else 'FAIL'))
    print()
    print('=== C 부르는 자리 (NEW) ===')
    for t in ('memoVal', 'memoText', 'userMemos', 'toggleMemoView', 'updateMemoButton(', 'paintMemoImages(',
              'attachMemoImage(', 'renderMemoThumbs(', "refBoxHTML(item.id,'memo')", "refBtnsHTML(item.id,'memo')",
              'memo-display-', 'reflink-memo-', 'memo-view-btn-', '📝 메모 보기', '메모 및 유사문제 연결'):
        print('  %-30s NEW %d · HEAD %d  %s' % (t, new.count(t), base.count(t), 'PASS' if new.count(t) == 0 else 'FAIL'))
    print()
    print('=== G9 문자 무변 블록 (NEW vs HEAD) ===')
    nbad = 0
    for h in G9_FUNCS:
        same = fn_block(new, h) == fn_block(base, h)
        nbad += (not same)
        print('  %-36s %s  %d자' % (h, 'PASS 문자까지 같다' if same else 'FAIL 달라졌다', len(fn_block(new, h))))
    cs_new, cs_base = fn_block(new, 'function ggCsHTML('), fn_block(base, 'function ggCsHTML(')
    cs_ok = (cs_new.count(CS_LINK_LINE) == 1 and cs_new.replace(CS_LINK_LINE, '') == cs_base)
    nbad += (not cs_ok)
    print('  %-36s %s' % ('function ggCsHTML(', 'PASS 붙은 것 = 🔗 버튼 한 줄뿐' if cs_ok else 'FAIL'))
    # A-5 — 검색 q · l 갈래 문자 그대로
    rq_new = between(fn_block(new, 'function runSearch('), "            if (searchMode === 'q') {", '            } else {')
    rq_base = between(fn_block(base, 'function runSearch('), "            if (searchMode === 'q') {", '            } else {')
    a5 = rq_new == rq_base
    nbad += (not a5)
    print('  %-36s %s' % ("runSearch q·l 갈래", 'PASS 문자까지 같다' if a5 else 'FAIL'))
    lf = "                if (kind && !String(extra).trim()) continue;       /* 비어 있으면 후보가 아니다 */"
    lf_ok = new.count(lf) == 1 and base.count(lf) == 1
    nbad += (not lf_ok)
    print('  %-36s %s' % ('linkSearch 후보 거르기 줄', 'PASS 그대로' if lf_ok else 'FAIL'))
    sk_new = re.search(r"const SYNC_KEYS = (\[[^\]]*\]);", new).group(1)
    sk_ok = sk_new == sk and len(sync_keys) == 17 and 'ox_gg_memo_merged' not in sk_new
    nbad += (not sk_ok)
    print('  %-36s %s' % ('SYNC_KEYS 17키 · 표시키 밖', 'PASS' if sk_ok else 'FAIL'))
    bline = "            syncRecords().then(ggMemoMergeBoot, ggMemoMergeBoot);"
    rbk = fn_block(new, 'function recBoot(')
    boot_src_ok = (new.count(bline) == 1 and bline in rbk and new.count('ggMemoMergeOnce(') == 2 and new.count('ggMemoMergeBoot') == 3)
    nbad += (not boot_src_ok)
    print('  %-36s %s' % ('§B 시동 줄 = recBoot 첫 동기화 뒤 한 곳', 'PASS' if boot_src_ok else 'FAIL (%d/%d/%d)' % (
        new.count(bline), new.count('ggMemoMergeOnce('), new.count('ggMemoMergeBoot'))))
    print('  G9 소스 : %s' % ('ALL OK' if not nbad else '%d개 어긋남' % nbad))
    print()

    # ── 앱 두 판
    res = {}
    for tag, src in (('NEW', new), ('HEAD', base)):
        lines = build_and_run(tag, src, seed, tests)
        res[tag] = lines
        print('=== %s 판 ===' % tag)
        if lines is None:
            print('  결과 줄 없음 → %s' % os.path.join(OUT, 'dom_%s.html' % tag))
            continue
        for ln in lines:
            if not ln.startswith('VAL | '):
                print('   ' + ln)
        p = sum(1 for ln in lines if ln.startswith('PASS'))
        f = sum(1 for ln in lines if ln.startswith('FAIL'))
        print('  합계 PASS %d · FAIL %d' % (p, f))
        print()

    # ── B-4 시동 순서 — 첫 동기화에서 받은 원격 판(이미 옮긴 한 문항)을 이관이 보고 건너뛰는가.
    #    헛잣대 = 같은 판에서 시동 줄만 「동기화 전에 옮김」으로 바꾼 것. 순서가 틀리면 이 기기 판이 원격을 칸째로 덮는다.
    bline = "            syncRecords().then(ggMemoMergeBoot, ggMemoMergeBoot);"
    if new.count(bline) == 1:
        RU = P['UC']
        u_seed = {k + '|' + c: 1000 for k in sync_keys for c in (data.get(k) or {})}
        rlist = [dict(g) for g in (gg.get(RU) or [])]
        rlist.append({'k': 'g_' + RU + '_REMOTE', 'i': max([int(g.get('i') or 0) for g in rlist] or [0]) + 1,
                      't': memos[RU], 'ok': None, 'ts': 1500, 'cs': [], 'src': 'memo'})
        remote = {'v': 1, 'savedAt': '2026-09-14T00:00:00.000Z', 'by': '원격(하네스)',
                  'data': {'ox_q_geunge': {RU: rlist}}, 'u': {'ox_q_geunge|' + RU: 2000}, 'gone': {}}
        seed_b = dict(seed_ls)
        seed_b['ox_sync_u'] = json.dumps(u_seed, ensure_ascii=False, separators=(',', ':'))
        seed_b['ox_sync_gone'] = '{}'
        seed_b['ox_sync_shadow'] = json.dumps({k: (data.get(k) if data.get(k) is not None else {}) for k in sync_keys},
                                              ensure_ascii=False, separators=(',', ':'))
        seed_b['ox_sync_meta'] = json.dumps({'lastSync': 1000, 'remoteSha': 'remote-sha-0'})
        seed_b['tt.cfg'] = json.dumps({'token': 'harness-token', 'person': '하네스'}, ensure_ascii=False)
        seed_boot = ('<script>'
                     'window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.lineno||""))});'
                     'window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});'
                     'window.__NET=[];window.__PUTS=[];window.__REMOTE=' + js_json(json.dumps(remote, ensure_ascii=False)) + ';'
                     'window.fetch=function(url,opt){url=String(url);var m=(opt&&opt.method)||"GET";var h=(opt&&opt.headers)||{};var acc=String(h.Accept||"");'
                     'var rec=url.indexOf("/contents/"+encodeURI("minbeop/기록.json"))>=0;'
                     '__NET.push(m+" "+(rec?"기록":url.split("?")[0].split("/").pop())+(acc.indexOf("raw")>=0?"(raw)":""));'
                     'function RS(st,b){return Promise.resolve(new Response(typeof b==="string"?b:JSON.stringify(b),{status:st,headers:{"Content-Type":"application/json"}}));}'
                     'if(rec&&m==="GET"&&acc.indexOf("raw")>=0)return RS(200,__REMOTE);'
                     'if(rec&&m==="GET")return RS(200,{sha:"remote-sha-1"});'
                     'if(rec&&m==="PUT"){__PUTS.push(String(opt.body||""));return RS(200,{content:{sha:"remote-sha-"+(__PUTS.length+1)}});}'
                     'return RS(404,{message:"Not Found"});};'
                     'localStorage.clear();var __S=' + json.dumps(seed_b, ensure_ascii=False).replace('</', '<\\/') +
                     ';for(var __k in __S)localStorage.setItem(__k,__S[__k]);'
                     '</script>')
        btests = BOOT_TESTS.replace('__P__', js_json(P))
        before_src = new.replace(bline, "            ggMemoMergeBoot(); syncRecords();   /* 헛잣대 — 동기화 전에 옮긴다 */")
        for tag, src in (('BOOT', new), ('BOOT-BEFORE', before_src)):
            lines = build_and_run(tag, src, seed_boot, btests)
            res[tag] = lines
            print('=== %s 판 %s===' % (tag, '(헛잣대 · 동기화 전에 옮김) ' if tag != 'BOOT' else '(첫 동기화 뒤) '))
            if lines is None:
                print('  결과 줄 없음 → %s' % os.path.join(OUT, 'dom_%s.html' % tag))
                continue
            for ln in lines:
                if not ln.startswith('VAL | '):
                    print('   ' + ln)
            print('  합계 PASS %d · FAIL %d' % (sum(1 for x in lines if x.startswith('PASS')), sum(1 for x in lines if x.startswith('FAIL'))))
            print()
    vn, vh = vals(res.get('NEW')), vals(res.get('HEAD'))
    print('=== 기준값 (NEW 판이 잰 것) ===')
    for k in sorted(vn):
        if k.startswith(('A3.', 'B.', 'G1.', 'A2.', 'G5.', 'C.')):
            print('  %-24s %s' % (k, json.dumps(vn[k], ensure_ascii=False)))
    print()

    # 드라이런 교차 — 앱 함수(dry) 와 파이썬 독립 계산
    py_moved = sorted(u for u in memos if str(memos[u] if memos[u] is not None else '').strip()
                      and not any((g or {}).get('src') == 'memo' for g in (gg.get(u) or [])))
    py_over = sorted([[u, len(str(memos[u]))] for u in py_moved if len(str(memos[u])) > 200])
    py_links = sorted(u for u in rl if ((rl[u] or {}).get('memo') or []))
    cross = (vn.get('B.dry.moved') == len(py_moved) and sorted(vn.get('B.dry.over') or []) == py_over
             and sorted(vn.get('B.dry.links') or []) == py_links and vn.get('B.dry.uids30') == py_moved[:30])
    print('=== B-5 드라이런 교차 (앱 dry 함수 vs 파이썬 독립 계산) === %s' % ('PASS 일치' if cross else 'FAIL'))
    print('  옮길 문항 %s · 200자 초과 %s · memo 갈래 연결 문항 %s' % (len(py_moved), py_over, len(py_links)))
    print()

    print('=== G10 A-5 무변 — 문제·논리 갈래 결과 (NEW vs HEAD) ===')
    g10 = True
    for k in ('G10.q', 'G10.l', 'G10.logicCount', 'G10.fieldItems_l', 'G10.dist_l'):
        same = (k in vn and vn.get(k) == vh.get(k))
        g10 &= same
        print('  %-18s %s  NEW %s · HEAD %s' % (k, 'PASS' if same else 'FAIL', vn.get(k), vh.get(k)))
    print()

    def gate(lines, prefix):
        ls_ = [ln for ln in (lines or []) if ln.split(' | ')[1:2] and ln.split(' | ')[1].startswith(prefix)]
        return '%dP/%dF' % (sum(1 for x in ls_ if x.startswith('PASS')), sum(1 for x in ls_ if x.startswith('FAIL')))

    print('=== 헛잣대 표 — 같은 게이트를 고치기 전(HEAD) 판에 ===')
    print('  G1  NEW %-18s HEAD %s' % (json.dumps(vn.get('G1.btn'), ensure_ascii=False), json.dumps(vh.get('G1.btn'), ensure_ascii=False)))
    print('  G2  NEW %-18s HEAD %s' % ('/'.join(str(g2[t][0]) for t in G2_TOKENS), '/'.join(str(g2[t][1]) for t in G2_TOKENS)))
    print('  G6  NEW %-18s HEAD %s   (t 안 \\n 수 · 칸 태그)' % ('nl=%s %s' % (vn.get('G6.nl'), vn.get('G6.tag')), 'nl=%s %s' % (vh.get('G6.nl'), vh.get('G6.tag'))))
    print('  G6  NEW %-18s HEAD %s' % (gate(res.get('NEW'), 'G6'), gate(res.get('HEAD'), 'G6')))
    print('  G8  NEW %-18s HEAD %s' % (gate(res.get('NEW'), 'G8'), gate(res.get('HEAD'), 'G8')))
    total_f = sum(1 for ln in (res.get('NEW') or []) if ln.startswith('FAIL'))
    boot_f = sum(1 for ln in (res.get('BOOT') or []) if ln.startswith('FAIL'))
    print('  B-4 NEW %-15s 헛잣대(동기화 전에 옮김) %s' % (gate(res.get('BOOT'), 'B-4'), gate(res.get('BOOT-BEFORE'), 'B-4')))
    ok = (res.get('NEW') is not None and total_f == 0 and g2_ok and not nbad and cross and g10
          and res.get('BOOT') is not None and boot_f == 0)
    print()
    print('종합 : %s' % ('ALL PASS' if ok else 'FAIL 있음'))
    return 0 if ok else 1


TESTS = r"""<script>
/* ⚠ 결과는 documentElement 에 붙인다(앱이 body 를 갈아치운다).
   ⚠ 앱 onload(IndexedDB → 동기화 시동)는 헤드리스 가상 시계와 경합한다 — 9/14 실측: 검사 시점에 안 끝나 있었다
     (덤프의 데이터 라벨이 검사가 넣은 더미 문항 수로 찍혔다 = onload 가 검사 뒤에 끝났다).
     그래서 onload 를 끄고 검사가 recBoot 를 직접 부른다. 이 판이 바꾼 시동 코드는 recBoot 안(첫 동기화 뒤 이관)이다. */
window.onload=null;
function __MAIN(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,260):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v===undefined?null:v));
const H=s=>{let h=0x811c9dc5;s=String(s);for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0;}return ('00000000'+h.toString(16)).slice(-8)+':'+s.length;};
window.confirm=()=>true; window.alert=()=>{};
const errs=(window.__ERR||[]).filter(x=>x.indexOf('net blocked')<0);
say('부팅 오류 '+errs.length+'건 : '+(errs.slice(0,3).join(' / ')||'없음'));
const tw=document.createElement('div');tw.className='hidden';document.body.appendChild(tw);say('tailwind 적재 = '+(getComputedStyle(tw).display==='none'));tw.remove();
const NEWAPP=(typeof ggMemoMergeOnce==='function');
say('판 = '+(NEWAPP?'NEW':'HEAD'));
const ls=k=>localStorage.getItem(k);
const ggS=()=>{try{return JSON.parse(ls('ox_q_geunge')||'{}')||{}}catch(e){return {}}};
const rlS=()=>{try{return JSON.parse(ls('ox_q_reflinks')||'{}')||{}}catch(e){return {}}};
const nItems=st=>Object.keys(st).reduce((a,k)=>a+(Array.isArray(st[k])?st[k].length:0),0);
const nUids=st=>Object.keys(st).filter(k=>Array.isArray(st[k])&&st[k].length).length;
const el=id=>document.getElementById(id);
const box=document.createElement('div');box.id='hz-box';box.style.cssText='width:760px;background:#fff';document.body.appendChild(box);
const g6box=document.createElement('div');g6box.id='hz-g6';g6box.style.cssText='width:760px;background:#fff';document.body.appendChild(g6box);
const put=(uid,host)=>(host||box).insertAdjacentHTML('beforeend','<div class="question-box p-3" id="hz-card-'+uid+'">'+ggLineHTML(uid)+'</div>');
const btnText=(root,txt)=>root?[...root.querySelectorAll('button')].find(x=>x.textContent.trim()===txt):null;
const kd=(node,shift)=>{const e=new KeyboardEvent('keydown',{key:'Enter',shiftKey:!!shift,bubbles:true,cancelable:true});node.dispatchEvent(e);return e;};
try{
 const QZ=__QUIZ__; quizData.length=0; QZ.forEach(q=>quizData.push(q));
 const P=__P__;
 /* ── B-4 시동 이관(토큰 없음 — 동기화가 곧바로 끝나고 이관이 돈다). 확인한 뒤 심은 판으로 되돌려 아래 검사를 옛 차례대로 한다 */
 if(NEWAPP){
  const bootG=ggS(), bootFlag=ls('ox_gg_memo_merged');
  const memosB=JSON.parse(ls('ox_q_memos')||'{}'), mB=Object.keys(memosB).filter(k=>String(memosB[k]==null?'':memosB[k]).trim());
  const nMemoB=Object.keys(bootG).reduce((a,k)=>a+(bootG[k]||[]).filter(g=>g&&g.src==='memo').length,0);
  V('B4.boot.flag',bootFlag);
  T('B-4 시동 때 이관이 한 번 돌았다(토큰 없음 · 표시키 · src=memo = 메모 칸)',!!bootFlag&&nMemoB===mB.length,'flag='+bootFlag+' memo='+nMemoB+'/'+mB.length);
  T('B-4 시동 이관 뒤 검색줄 수가 새 N',(el('search-mode-m')||{}).innerText==='🔗 근거 ('+nUids(bootG)+')',(el('search-mode-m')||{}).innerText);
  localStorage.setItem('ox_q_geunge',P.seedGG); localStorage.setItem('ox_q_reflinks',P.seedRL); localStorage.removeItem('ox_gg_memo_merged');
  if(typeof useIdxDrop==='function') useIdxDrop();
 }
 const G9K=['ox_q_tags','ox_q_logic','ox_q_links','ox_q_coords','ox_mem_cards'];
 const g9a={}; G9K.forEach(k=>g9a[k]=ls(k));
 const keys0=Object.keys(localStorage).sort();
 const memosRaw0=ls('ox_q_memos');
 const memos=JSON.parse(memosRaw0||'{}');
 const memoUids=Object.keys(memos).filter(k=>String(memos[k]==null?'':memos[k]).trim()).sort();
 const gg0=ggS(), ggRaw0=ls('ox_q_geunge'), rl0=rlS();
 const ggUids0=Object.keys(gg0).filter(k=>Array.isArray(gg0[k])&&gg0[k].length);
 V('A3.before.gg_uids',ggUids0.length); V('A3.before.gg_items',nItems(gg0));
 V('A3.before.gg_comments',Object.keys(gg0).reduce((a,k)=>a+(gg0[k]||[]).reduce((b,g)=>b+((g&&g.cs)||[]).length,0),0));
 V('A3.before.memo_uids',memoUids.length); V('A3.before.overlap',memoUids.filter(u=>ggUids0.indexOf(u)>=0).length);
 V('A3.before.rl_memo_owners',Object.keys(rl0).filter(k=>rl0[k]&&Array.isArray(rl0[k].memo)&&rl0[k].memo.length).length);
 V('A3.before.rl_geunge_owners',Object.keys(rl0).filter(k=>rl0[k]&&Array.isArray(rl0[k].geunge)&&rl0[k].geunge.length).length);
 V('A3.before.gg_max_t',Object.keys(gg0).reduce((m,k)=>Math.max(m,...(gg0[k]||[]).map(g=>String((g&&g.t)||'').length)),0));

 /* ── §B 드라이런 · G3 · G4 (NEW 만 — HEAD 에는 함수가 없다) */
 if(NEWAPP){
  const plan=ggMemoMergeOnce(true);
  V('B.dry.moved',plan.moved.length); V('B.dry.uids30',plan.moved.slice(0,30)); V('B.dry.over',plan.over); V('B.dry.links',plan.links);
  T('B-5 드라이런은 아무것도 안 쓴다(근거·연결·표시키)',ls('ox_q_geunge')===ggRaw0&&JSON.stringify(rlS())===JSON.stringify(rl0)&&!ls('ox_gg_memo_merged'));
  ggMemoMergeOnce();
  const gg1=ggS(), rl1=rlS();
  const srcMemo=o=>Object.keys(o).reduce((a,k)=>a+(o[k]||[]).filter(g=>g&&g.src==='memo').length,0);
  T('G3 src=memo 항목 수 = 이관 전 ox_q_memos 칸 수',srcMemo(gg1)===memoUids.length,srcMemo(gg1)+' vs '+memoUids.length);
  T('G3 첫 이관 항목 수 = 전 + 메모 칸',nItems(gg1)===nItems(gg0)+memoUids.length,nItems(gg1)+' vs '+(nItems(gg0)+memoUids.length));
  const r2=ggMemoMergeOnce();
  T('G3 두 번째(표시키 켜짐) — 안 돈다 · 항목 수 무변',r2===null&&nItems(ggS())===nItems(gg1));
  localStorage.removeItem('ox_gg_memo_merged');
  const r3=ggMemoMergeOnce();
  T('G3 세 번째(표시키 지움) — src:memo 로 전부 건너뜀 · 항목 수 무변',!!r3&&r3.moved.length===0&&r3.skipped.length===memoUids.length&&nItems(ggS())===nItems(gg1),JSON.stringify(r3&&{m:r3.moved.length,s:r3.skipped.length}));
  const bad=[];
  memoUids.forEach(u=>{
   const a0=Array.isArray(gg0[u])?gg0[u]:[], a1=gg1[u]||[], last=a1[a1.length-1]||{};
   const mx=a0.reduce((m,x)=>Math.max(m,Number(x&&x.i)||0),0);
   const ok=a1.length===a0.length+1&&JSON.stringify(a1.slice(0,a0.length))===JSON.stringify(a0)
     &&JSON.stringify(Object.keys(last))==='["k","i","t","ok","ts","cs","src"]'
     &&last.i===mx+1&&last.t===String(memos[u])&&last.ok===null&&Array.isArray(last.cs)&&last.cs.length===0&&last.src==='memo'
     &&String(last.k).indexOf('g_'+u+'_')===0&&typeof last.ts==='number';
   if(!ok)bad.push(u);
  });
  T('B-1 꼴 — 맨 뒤 · i=최대+1 · t 통째(자르지 않음) · ok=null · cs=[] · src=memo · 앞 항목 문자 무변',bad.length===0,bad.slice(0,5).join(','));
  const others=Object.keys(gg0).filter(u=>memoUids.indexOf(u)<0);
  T('B-1 메모 없는 문항의 근거는 문자까지 그대로',others.every(u=>JSON.stringify(gg1[u])===JSON.stringify(gg0[u])),others.length);
  const rbad=[];
  Object.keys(rl0).forEach(o=>{
   const a=rl0[o]||{}, b=rl1[o];
   if(Array.isArray(a.memo)&&a.memo.length){
    const want=Array.from(new Set((a.geunge||[]).concat(a.memo))).filter(x=>x&&x!==o);
    if(!b||b.memo!==undefined||JSON.stringify(b.geunge)!==JSON.stringify(want)||JSON.stringify(b.logic)!==JSON.stringify(a.logic))rbad.push(o+':'+JSON.stringify(b));
   } else if(JSON.stringify(a)!==JSON.stringify(b)) rbad.push(o+'≠');
  });
  T('B-2 memo 갈래 → geunge 합집합 · memo 비움 · 나머지 문항 무변',rbad.length===0,rbad.slice(0,3).join(' '));
  T('G4 ox_q_memos 이관 전후 문자 동일(md5 동일)',ls('ox_q_memos')===memosRaw0);
  V('B.flag',ls('ox_gg_memo_merged'));
 }
 const ggNow=ggS(), N=nUids(ggNow);
 V('A3.after.N',N); V('A3.after.gg_items',nItems(ggNow));

 /* ── G1 · A-2 · A-3 */
 refreshModeCounts();
 const mb=el('search-mode-m');
 V('G1.btn',mb?mb.innerText:null);
 T('G1 첫 화면 버튼 = 🔗 근거 (N) · N = 근거 항목이 하나라도 있는 문항 수',!!mb&&mb.innerText==='🔗 근거 ('+N+')',mb&&mb.innerText);
 setSearchMode('m');
 const si=el('search-input'); si.value=''; runSearch();
 V('A2.placeholder',si.placeholder); V('A2.short',el('search-count').textContent); V('A2.modeLabel',modeLabel('m'));
 T('A-2 안내 — placeholder · 두 글자 미만 문구 · modeLabel',si.placeholder==='근거·댓글에서 검색'&&el('search-count').textContent==='근거 '+N+'개 ▸'&&modeLabel('m')==='🔗 근거',si.placeholder+' / '+el('search-count').textContent);
 const fmWant=quizData.filter(q=>Array.isArray(ggNow[q.id])&&ggNow[q.id].length).length, fm=fieldItems('m').length;
 V('A3.fieldItems_m',fm);
 T('A-3 fieldItems(m) = quizData 중 근거가 있는 문항',fm===fmWant,fm+' vs '+fmWant);
 showFieldDistribution('m'); const distTxt=el('search-results').innerText;
 T('A-3 단원 분포 머리 = 🔗 근거 N건',distTxt.indexOf('🔗 근거 '+fmWant+'건')>=0,distTxt.slice(0,80));
 showFieldList('m',0); const flHtml=el('search-results').innerHTML;
 T('A-3 단원 목록 줄 = 근거 글 · 파랑',flHtml.indexOf('text-blue-900 bg-blue-50 border-blue-400')>=0&&flHtml.indexOf('🔗')>=0&&flHtml.indexOf('undefined')<0,flHtml.slice(0,160));

 /* ── G10 · A-5 — 문제·논리 갈래(두 판 결과를 파이썬이 맞댄다) */
 setSearchMode('q'); si.value=P.termQ; runSearch(); V('G10.q',H(el('search-results').innerHTML)+'|'+el('search-count').textContent);
 setSearchMode('l'); si.value=P.termL; runSearch(); V('G10.l',H(el('search-results').innerHTML)+'|'+el('search-count').textContent);
 V('G10.logicCount',logicCount()); V('G10.fieldItems_l',fieldItems('l').length);
 showFieldDistribution('l'); V('G10.dist_l',H(el('search-results').innerHTML));

 /* ── G6 · D-1 */
 put(P.U6,g6box);
 const inp=el('gg-in-'+P.U6);
 V('G6.tag',inp&&inp.tagName);
 inp.value='첫 줄';
 const e1=kd(inp,true);
 T('G6 shift+enter — 저장하지 않고 기본 동작(줄바꿈)을 막지 않는다',ggOf(P.U6).length===0&&!e1.defaultPrevented,'items='+ggOf(P.U6).length+' prevented='+e1.defaultPrevented);
 inp.value='첫 줄\n둘째 줄';
 kd(inp,false);
 const l6=ggOf(P.U6), g6=l6[l6.length-1];
 const nl=g6?(String(g6.t).match(/\n/g)||[]).length:-1;
 V('G6.t',g6?g6.t:null); V('G6.nl',nl);
 T('G6 enter 저장 → t 안에 \\n 이 하나',!!g6&&nl===1,g6&&JSON.stringify(g6.t));
 if(g6){
  ggToggle(P.U6,g6.k);
  window.__G6={uid:P.U6,k:g6.k,ws1:getComputedStyle(el('gg-t-'+P.U6+'-'+g6.k)).whiteSpace};   /* 재는 것은 2단계(한 틱 뒤) */
 } else T('G6 펼침 판에 두 줄로 보인다',false,'항목 없음');
 const q0=inp.getBoundingClientRect(); inp.value='가\n나\n다'; inp.dispatchEvent(new Event('input',{bubbles:true})); const q1=inp.getBoundingClientRect();
 V('D1.grow',{h0:q0.height,h1:q1.height,dtop:q1.top-q0.top});
 T('D-1 칸이 아래로 넓어진다(위 모서리 그대로)',q1.height>q0.height+8&&Math.abs(q1.top-q0.top)<1,JSON.stringify({h0:q0.height,h1:q1.height,dtop:q1.top-q0.top}));
 kd(inp,false);
 const q2=inp.getBoundingClientRect();
 T('D-1 저장하면 칸이 한 줄 높이로 돌아온다',Math.abs(q2.height-q0.height)<1,JSON.stringify({h0:q0.height,h2:q2.height}));
 T('D-1 resize:none',getComputedStyle(inp).resize==='none',getComputedStyle(inp).resize);
 if(g6){
  const ein=el('gg-ein-'+P.U6+'-'+g6.k);
  T('D-2 고치는 칸 = textarea · 초기값에 줄바꿈 그대로',!!ein&&ein.tagName==='TEXTAREA'&&ein.value===g6.t,ein&&(ein.tagName+' '+JSON.stringify(ein.value)));
  const cin=el('gg-cin-'+P.U6+'-'+g6.k);
  T('D-3 댓글 칸 = textarea',!!cin&&cin.tagName==='TEXTAREA',cin&&cin.tagName);
  cin.value='댓글 첫 줄'; const e4=kd(cin,true);
  T('D-3 댓글 shift+enter 는 달지 않는다',((ggItem(P.U6,g6.k)||{}).cs||[]).length===0&&!e4.defaultPrevented);
  ggEdit(P.U6,g6.k); ein.value='고친 첫 줄\n고친 둘째'; const e5=kd(ein,true);
  T('D-2 고치기 shift+enter 는 저장하지 않는다',(ggItem(P.U6,g6.k)||{}).t===g6.t&&!e5.defaultPrevented);
  kd(ein,false);
  T('D-2 고치기 enter → 여러 줄로 저장 · 판 글자 갱신',(ggItem(P.U6,g6.k)||{}).t==='고친 첫 줄\n고친 둘째'&&el('gg-t-'+P.U6+'-'+g6.k).textContent==='고친 첫 줄\n고친 둘째',JSON.stringify((ggItem(P.U6,g6.k)||{}).t));
 }

 /* ── G8 · 댓글에만 있는 글자로 두 자리 검색 */
 const TOK=P.tok;
 put(P.U8); put(P.O8);
 const g8=ggOf(P.U8)[0];
 if(g8){
  ggToggle(P.U8,g8.k);
  el('gg-cin-'+P.U8+'-'+g8.k).value=TOK+' 댓글';
  const rb=btnText(el('gg-pan-'+P.U8+'-'+g8.k),'달기'); if(rb) rb.click();
 }
 T('G8 준비 — 댓글 달기',!!g8&&((ggItem(P.U8,g8.k)||{}).cs||[]).some(c=>String(c.t).indexOf(TOK)>=0));
 const stNow=ggS();
 T('G8 준비 — 그 글자는 근거 본문·지문 어디에도 없다',!Object.keys(stNow).some(u=>(stNow[u]||[]).some(g=>String(g&&g.t).indexOf(TOK)>=0))&&!quizData.some(q=>String(q.q).indexOf(TOK)>=0));
 setSearchMode('m'); si.value=TOK; runSearch();
 const sr=el('search-results').innerHTML;
 V('G8.home.count',el('search-count').textContent);
 T('G8-① 첫 화면 검색 — 그 문항이 나온다',sr.indexOf('ID '+P.U8)>=0,el('search-count').textContent);
 T('G8-① 미리보기 줄에 ↳ 댓글(걸린 글자 표시)',sr.indexOf('↳ ')>=0&&sr.indexOf('<mark')>=0,sr.slice(0,260));
 const pv=el('search-results').querySelector('div[class*="border-l-2"]'), pvc=pv?pv.className.split(/\s+/):[];
 T('G8-① 미리보기 색 = 근거 파랑(노랑 아님)',['text-blue-900','bg-blue-50','border-blue-400'].every(c=>pvc.indexOf(c)>=0)&&sr.indexOf('bg-yellow-50')<0,pv?pv.className:'미리보기 줄 없음');
 ggSearchToggle(P.O8); el('link-search-geunge-'+P.O8).value=TOK; linkSearch(P.O8,'geunge');
 const lr=el('link-results-geunge-'+P.O8).innerHTML;
 T('G8-② 카드 안 🔍 — 그 문항이 나온다',lr.indexOf('ID '+P.U8)>=0,lr.slice(0,160));
 T('G8-② 미리보기 줄에 ↳ 댓글',lr.indexOf('↳ ')>=0,lr.slice(0,260));
 ggSearchToggle(P.O8);

 /* ── G8-2 댓글 🔗 로 연결 — 본문 🔍 로 건 것과 같은 칸 · 같은 칩 · 새 키 0 */
 const keys82=Object.keys(localStorage).sort();
 const lk=g8?btnText(el('gg-cs-'+P.U8+'-'+g8.k),'🔗'):null;
 T('G8-2 댓글 줄에 🔗 버튼',!!lk);
 if(lk){
  lk.click();
  const sp=el('gg-search-'+P.U8);
  T('G8-2 🔗 → 본문 줄 🔍 와 같은 찾기 칸이 열린다',!!sp&&!sp.classList.contains('hide'));
  el('link-search-geunge-'+P.U8).value=P.termT82; linkSearch(P.U8,'geunge');
  const pick=[...el('link-results-geunge-'+P.U8).querySelectorAll('button')].find(b=>(b.getAttribute('onclick')||'').indexOf("'"+P.T82+"'")>=0);
  T('G8-2 찾기 결과에 대상이 있다',!!pick,P.T82);
  if(pick) pick.click();
 }
 T('G8-2 결과가 ox_q_reflinks[uid].geunge 한 곳에 들어간다',((rlS()[P.U8]||{}).geunge||[]).indexOf(P.T82)>=0&&Object.keys(rlS()[P.U8]||{}).join()==='geunge',JSON.stringify(rlS()[P.U8]));
 ggSearchToggle(P.U8); el('link-search-geunge-'+P.U8).value=P.termT83; linkSearch(P.U8,'geunge');
 const pick2=[...el('link-results-geunge-'+P.U8).querySelectorAll('button')].find(b=>(b.getAttribute('onclick')||'').indexOf("'"+P.T83+"'")>=0);
 if(pick2) pick2.click();
 const chipC=el('gg-refchip-'+P.U8+'-'+P.T82), chipB=el('gg-refchip-'+P.U8+'-'+P.T83);
 T('G8-2 칩 모양 = 본문 🔍 로 건 칩과 같다',!!chipC&&!!chipB&&chipC.outerHTML.split(P.T82).join('#')===chipB.outerHTML.split(P.T83).join('#'),chipC&&chipB?chipC.outerHTML.slice(0,120)+' / '+chipB.outerHTML.slice(0,120):'칩 없음');
 const keys82b=Object.keys(localStorage).sort();
 T('G8-2 새 localStorage 키 0',JSON.stringify(keys82)===JSON.stringify(keys82b),keys82b.filter(k=>keys82.indexOf(k)<0).join(','));

 /* ── G7 연결 상자에서 그 자리 고치기 */
 put(P.U7); put(P.O7);
 ggRefAdd(P.O7,P.U7); ggRefToggle(P.O7,P.U7);
 const bx=()=>el('refgg-box-'+P.O7+'-'+P.U7);
 const L0=JSON.parse(JSON.stringify(ggOf(P.U7))), k0=L0[0]&&L0[0].k;
 const edBtns=bx()?[...bx().querySelectorAll('button')].filter(b=>b.textContent.trim()==='✎ 여기서 고치기'):[];
 T('G7 연결 상자 = 항목별(✎ 수 = 항목 수 + 댓글 수)',edBtns.length>0&&edBtns.length===L0.length+L0.reduce((a,g)=>a+((g&&g.cs)||[]).length,0),edBtns.length+' vs '+L0.length);
 const pansNode=el('gg-pans-'+P.U7), chipNode=k0?el('gg-chip-'+P.U7+'-'+k0):null;
 if(edBtns.length){
  edBtns[0].click();
  const ta=el('refgg-ein-'+P.O7+'-'+P.U7+'-'+k0);
  T('G7 ✎ → 그 자리에 textarea(초기값 = 본문)',!!ta&&ta.tagName==='TEXTAREA'&&!ta.closest('.hide')&&ta.value===L0[0].t);
  if(ta){
   ta.value='고친 본문 '+TOK;
   const sb=btnText(ta.parentElement,'저장'); if(sb) sb.click();
   const L1=ggOf(P.U7);
   const strip=g=>{const o=Object.assign({},g);delete o.t;return JSON.stringify(o);};
   T('G7 대상 t 만 바뀐다 — k·i·ok·ts·cs 무변 · 다른 항목 무변',L1.length===L0.length&&L1[0].t==='고친 본문 '+TOK&&strip(L1[0])===strip(L0[0])&&JSON.stringify(L1.slice(1))===JSON.stringify(L0.slice(1)),JSON.stringify(L1[0]));
   T('G7 대상 카드 제자리 — gg-t 글자 · gg-ein 값',el('gg-t-'+P.U7+'-'+k0).textContent==='고친 본문 '+TOK&&el('gg-ein-'+P.U7+'-'+k0).value==='고친 본문 '+TOK);
   T('G7 대상 카드는 다시 그리지 않는다(같은 노드)',el('gg-pans-'+P.U7)===pansNode&&el('gg-chip-'+P.U7+'-'+k0)===chipNode);
   T('G7 이쪽 상자 — 다시 그리고 펼침 유지',!!bx()&&!bx().classList.contains('hide')&&bx().textContent.indexOf('고친 본문 '+TOK)>=0);
  }
  const cIdx=L0.findIndex(g=>g&&g.cs&&g.cs.length);
  if(cIdx>=0){
   const g0=L0[cIdx], c0=g0.cs[0];
   const cb=[...bx().querySelectorAll('button')].find(b=>b.textContent.trim()==='✎ 여기서 고치기'&&(b.getAttribute('onclick')||'').indexOf("'"+c0.k+"'")>=0);
   T('E-4③ 댓글 줄에도 ✎',!!cb);
   if(cb){
    cb.click();
    const cta=el('refgg-cein-'+P.O7+'-'+P.U7+'-'+g0.k+'-'+c0.k);
    cta.value='고친 댓글 '+TOK;
    const sb2=btnText(cta.parentElement,'저장'); if(sb2) sb2.click();
    const g2=ggOf(P.U7)[cIdx], c2=g2.cs[0];
    const stripC=c=>{const o=Object.assign({},c);delete o.t;return JSON.stringify(o);};
    T('G7 댓글 — cs[n].t 만 바뀐다(k·ts 무변) · 항목 k·i·ok·ts 무변',c2.t==='고친 댓글 '+TOK&&stripC(c2)===stripC(c0)&&g2.k===g0.k&&g2.i===g0.i&&g2.ok===g0.ok&&g2.ts===g0.ts&&g2.cs.length===g0.cs.length,JSON.stringify(c2));
    T('G7 댓글 — 대상 카드 댓글 줄 제자리 갱신',el('gg-cs-'+P.U7+'-'+g0.k).textContent.indexOf('고친 댓글 '+TOK)>=0);
   }
   const lb=btnText(bx(),'🔗');
   if(lb) lb.click();
   T('E-4③ 연결 상자 댓글 줄 🔗 → 이 카드의 찾기 칸이 열린다',!!lb&&!el('gg-search-'+P.O7).classList.contains('hide'));
  } else say('G7 대상에 댓글이 없어 댓글 고치기는 건너뜀');
 }

 /* ── G8-3 빈 경우 둘 */
 put(P.U83); put(P.O83);
 ggRefAdd(P.O83,P.U83);
 ggOf(P.U83).slice().forEach(g=>ggDel(P.U83,g.k));
 ggRefPaint(P.O83);
 const b83=el('refgg-box-'+P.O83+'-'+P.U83);
 T('G8-3 연결 뒤 대상 근거를 다 지우면 「그 문항에 근거가 없습니다」',!!b83&&b83.textContent.indexOf('그 문항에 근거가 없습니다')>=0&&b83.textContent.indexOf('지금 데이터에 없음')<0,b83&&b83.textContent.slice(0,120));
 refPut(P.O83,[],[],refOf(P.O83,'geunge').concat(['Q9999'])); ggRefPaint(P.O83);
 const b99=el('refgg-box-'+P.O83+'-Q9999');
 T('G8-3 quizData 에 없는 uid 는 「지금 데이터에 없음」',!!b99&&b99.textContent.indexOf('지금 데이터에 없음')>=0&&b99.textContent.indexOf('근거가 없습니다')<0,b99&&b99.textContent.slice(0,120));

 /* ── G9 안 건드린 저장소 (근거·연결만 만진 지점) */
 const g9bad=G9K.filter(k=>ls(k)!==g9a[k]);
 T('G9 ox_q_tags · ox_q_logic · ox_q_links · ox_q_coords · ox_mem_cards 문자 무변',g9bad.length===0,g9bad.join(','));
 T('G4 ox_q_memos 끝까지 문자 무변',ls('ox_q_memos')===memosRaw0);

 /* ── §C 카드 화면 · 저장 두 자리 */
 let cErr='';
 try{
  currentSubject='민법총칙'; currentChapterLabel='1. 총칙 > 1.1 민법의 법원'; isExamMode=false; currentPageIndex=0; currentSessionMarks={}; resumePicks={};
  currentFilteredData=quizData.filter(q=>q.id===P.UC).concat(quizData.filter(q=>q.id!==P.UC&&q.id.indexOf('Q50')!==0).slice(0,3));
  if(el('home-screen')) el('home-screen').classList.add('hide');
  if(el('quiz-screen')) el('quiz-screen').classList.remove('hide');
  box.innerHTML='';
  renderQuizPage();
 }catch(e){cErr=e.message+' | '+(e.stack||'').split('\n')[1];}
 T('C 카드 그리기 오류 없음',!cErr,cErr);
 const card=el('q-box-'+P.UC);
 if(card){
  const ids=[...card.querySelectorAll('[id]')].map(x=>x.id);
  const memoIds=ids.filter(i=>/^(memo-input-|memo-display-|memo-view-btn-|reflink-memo-|refmemo-|link-search-memo-|link-results-memo-)/.test(i));
  T('C-1·C-2 카드에 메모 자리 0(입력·표시·보기 버튼·연결 상자·찾아서 넣기)',memoIds.length===0,memoIds.join(','));
  T('C-1 카드에 「암기 메모」·「메모 보기」 글자 0',card.textContent.indexOf('암기 메모')<0&&card.textContent.indexOf('메모 보기')<0);
  const pbtn=[...card.querySelectorAll('button')].find(b=>(b.getAttribute('onclick')||'').indexOf('toggleMemoPanel')>=0);
  T('C-1 패널 여는 버튼 = 「논리 및 유사문제 연결」',!!pbtn&&pbtn.textContent.trim()==='논리 및 유사문제 연결',pbtn&&pbtn.textContent.trim());
  const pan=el('memo-panel-'+P.UC);
  T('C-1 남는 것 — 논리 칸 · 논리 찾아서 넣기 · 문제 연결 · 닫기/저장하기',!!pan&&!!el('logic-input-'+P.UC)&&!!el('link-search-logic-'+P.UC)&&!!el('link-input-'+P.UC)&&!!btnText(pan,'저장하기')&&!!btnText(pan,'닫기'));
  const gin=el('gg-in-'+P.UC);
  T('D-1 카드 근거 칸 = textarea',!!gin&&gin.tagName==='TEXTAREA',gin&&gin.tagName);
  const chips=el('gg-chips-'+P.UC);
  V('C.chips',chips?chips.children.length:null);
  T('B 옛 메모 글이 그 문항의 근거 칩 하나로 들어가 있다',!!chips&&chips.children.length===ggOf(P.UC).length&&ggOf(P.UC).some(g=>g&&g.src==='memo'),chips&&chips.children.length);
  const m0=ls('ox_q_memos');
  toggleMemoPanel(P.UC);
  const mi=el('memo-input-'+P.UC); if(mi) mi.value='ZZ 카드에서 저장하면 안 되는 메모';
  saveMemoAndLink(P.UC);
  T('C-3 saveMemoAndLink — ox_q_memos 에 안 쓴다 · memo 갈래 없음',ls('ox_q_memos')===m0&&!((rlS()[P.UC]||{}).memo),JSON.stringify(rlS()[P.UC]||null));
 } else T('C 카드가 그려졌다',false,'q-box 없음');
 const ce=cmpExtraHTML(P.UC), cd=cmpEditHTML(P.UC);
 T('C-3 띄운 창 — 「📝 메모 보기」 없음 · 「✏️ 논리 및 유사문제 연결」',ce.indexOf('메모 보기')<0&&ce.indexOf('✏️ 논리 및 유사문제 연결')>=0);
 T('C-3 띄운 창 편집기 — 메모 칸 없음 · 논리 칸 있음',cd.indexOf('memo-input')<0&&cd.indexOf('암기 메모')<0&&cd.indexOf('cmp-logic-input-'+P.UC)>=0);
 box.insertAdjacentHTML('beforeend','<div id="cmp-edit-'+P.UC+'">'+cd+'</div>');
 const m1=ls('ox_q_memos'); const cmi=el('cmp-memo-input-'+P.UC); if(cmi) cmi.value='ZZ 창에서 저장하면 안 되는 메모';
 cmpSave(P.UC);
 T('C-3 cmpSave — ox_q_memos 에 안 쓴다',ls('ox_q_memos')===m1);

 /* ── G5 */
 T('G5 SYNC_KEYS 17키 무변',JSON.stringify(SYNC_KEYS)===JSON.stringify(P.syncKeys),SYNC_KEYS.length);
 const keysEnd=Object.keys(localStorage).sort();
 const added=keysEnd.filter(k=>keys0.indexOf(k)<0), gone=keys0.filter(k=>keysEnd.indexOf(k)<0);
 V('G5.added',added); V('G5.gone',gone);
 T('G5 새 localStorage 키 = ox_gg_memo_merged 하나뿐',JSON.stringify(added)===JSON.stringify(NEWAPP?['ox_gg_memo_merged']:[])&&gone.length===0,added.join(',')+' / gone '+gone.join(','));
 const errs2=(window.__ERR||[]).filter(x=>x.indexOf('net blocked')<0);
 T('검사 중 스크립트 오류 0',errs2.length===errs.length,errs2.slice(errs.length).join(' / '));
}catch(e){T('하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n').slice(1,3).join(' '))}
setTimeout(function(){
 try{
  const G=window.__G6;
  if(G){
   const tv=el('gg-t-'+G.uid+'-'+G.k), cs=getComputedStyle(tv), lh=parseFloat(cs.lineHeight)||(parseFloat(cs.fontSize)*1.5), hh=tv.getBoundingClientRect().height;
   V('G6.render',{ws_same_tick:G.ws1,ws_next_tick:cs.whiteSpace,h:Math.round(hh*10)/10,lh:lh,text:tv.textContent});
   T('G6 펼침 판에 두 줄로 보인다(pre-wrap · 높이 ≥ 줄높이×1.8 · 한 틱 뒤에 잰다)',cs.whiteSpace.indexOf('pre')===0&&hh>=lh*1.8,JSON.stringify({ws:cs.whiteSpace,h:hh,lh:lh,text:tv.textContent}));
  }
 }catch(e){T('2단계가 죽었다',false,e.message)}
 const pre=document.createElement('pre');pre.id='hz-out';pre.textContent=R.join('\n');
 document.documentElement.appendChild(pre);
},800);
}
setTimeout(function(){
 try{ recBoot(); }catch(e){ (window.__ERR=window.__ERR||[]).push('recBoot '+e.message); }
 let n=0;
 (function wait(){
  if(typeof ggMemoMergeBoot==='function'&&!localStorage.getItem('ox_gg_memo_merged')&&n<80){ n++; return setTimeout(wait,50); }
  __MAIN();
 })();
},1500);
</script>
"""

BOOT_TESTS = r"""<script>
window.onload=null;   /* 부팅은 검사가 recBoot 를 직접 부른다(가상 시계 경합 · TESTS 머리 주석) */
function __BOOTCHECK(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i).replace(/\n/g,'⏎').slice(0,260):''));
const say=s=>R.push('INFO | '+String(s).replace(/\n/g,'⏎'));
const V=(k,v)=>R.push('VAL | '+k+' | '+JSON.stringify(v===undefined?null:v));
try{
 const P=__P__;
 const ls=k=>localStorage.getItem(k);
 say('판 = '+(typeof ggMemoMergeBoot==='function'?'시동 이관 있음':'시동 이관 없음'));
 say('網 차례 '+(window.__NET||[]).join(' → '));
 const errs=(window.__ERR||[]);
 say('부팅 오류 '+errs.length+'건 : '+(errs.slice(0,3).join(' / ')||'없음'));
 const G=JSON.parse(ls('ox_q_geunge')||'{}');
 const memos=JSON.parse(ls('ox_q_memos')||'{}');
 const mU=Object.keys(memos).filter(k=>String(memos[k]==null?'':memos[k]).trim());
 const RU=P.UC;
 const rm=(G[RU]||[]).filter(g=>g&&g.src==='memo');
 V('BOOT.RU.memoKeys',rm.map(g=>g.k));
 T('B-4 순서 — 첫 동기화에서 받은 원격 판(이미 옮긴 '+RU+')을 이관이 보고 건너뛰었다(원격 항목만 · src=memo 하나)',rm.length===1&&rm[0].k==='g_'+RU+'_REMOTE',JSON.stringify(rm.map(g=>g.k)));
 const others=mU.filter(u=>u!==RU);
 const moved=others.filter(u=>(G[u]||[]).filter(g=>g&&g.src==='memo').length===1);
 T('B-4 나머지 '+others.length+'문항은 이 기기에서 한 번씩 옮겼다',moved.length===others.length,moved.length+'/'+others.length);
 let flag=null; try{flag=JSON.parse(ls('ox_gg_memo_merged')||'null')}catch(e){}
 V('BOOT.flag',flag);
 T('B-4 표시키 — 옮김 '+others.length+' · 연결 '+P.nLinks,!!flag&&flag.moved===others.length&&flag.links===P.nLinks,JSON.stringify(flag));
 const net=window.__NET||[];
 const shaGets=net.filter(x=>x==='GET 기록').length;
 V('BOOT.net',net);
 T('B-4 옮긴 뒤 곧바로 한 번 더 동기화했다(기록 sha 받기 2번 이상)',shaGets>=2,net.join(' → '));
 const puts=window.__PUTS||[];
 let last=null; try{ const b=JSON.parse(puts[puts.length-1]||'null'); last=JSON.parse(decodeURIComponent(escape(atob(b.content)))); }catch(e){}
 const nPut=last?Object.keys(last.data.ox_q_geunge||{}).reduce((a,k)=>a+(last.data.ox_q_geunge[k]||[]).filter(g=>g&&g.src==='memo').length,0):-1;
 V('BOOT.puts',puts.length); V('BOOT.lastPut.srcMemo',nPut);
 say('올린 판 '+puts.length+'번 · 마지막 판의 src=memo '+nPut+'개');
 T('B-4 옮긴 판을 곧바로 올렸다 — 두 번째 PUT · 그 판에 src=memo '+P.nMemo+'개(force 동기화)',puts.length>=2&&nPut===P.nMemo,'puts='+puts.length+' srcMemo='+nPut);
 T('B-4 ox_q_memos 는 이 기기에서 문자까지 그대로',ls('ox_q_memos')===JSON.stringify(JSON.parse(ls('ox_q_memos')))&&mU.length===P.nMemo,mU.length+' vs '+P.nMemo);
}catch(e){T('하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n')[1])}
const pre=document.createElement('pre');pre.id='hz-out';pre.textContent=R.join('\n');
document.documentElement.appendChild(pre);
}
setTimeout(function(){
 try{ recBoot(); }catch(e){ (window.__ERR=window.__ERR||[]).push('recBoot '+e.message); }
 let n=0;
 (function wait(){
  const gets=(window.__NET||[]).filter(x=>x==='GET 기록').length;
  const puts=(window.__PUTS||[]).length;
  const ready=!!localStorage.getItem('ox_gg_memo_merged')&&((gets>=2&&puts>=2)||n>=60);
  if(!ready&&n<120){ n++; return setTimeout(wait,50); }
  setTimeout(__BOOTCHECK,200);
 })();
},1500);
</script>
"""

if __name__ == '__main__':
    sys.exit(main())
