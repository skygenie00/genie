# -*- coding: utf-8 -*-
"""_task_jo_p8up §A-1·§A-2 — 해례 7판 원장(jimun_7pan.json)에 8판 바뀐 것 얹기(원장 판올림) · ⚙ 단계 [6d] · 멱등

  ⚙ = jo_build [6d](빈칸 갈래 [6b] · 조합 선지 [6c] 뒤) 가 build(dump, 검산, OUT) 를 부른다 — 이번 산출 넷을 고쳐 다시 쓴다.
      ⚠ 정리OMR 빈칸 갈래([6b])는 제7판 책 차례로 걷는다 — 그래서 그 뒤에 얹는다(8판 줄·지운 줄이 토막을 흔들지 않게).
  재료 = 특상디\\_p8up\\_ref_p8up.json(채팅 8판 대조 표 · 9/27 · md5 39ddc4c2 · task\\ 사본과 바이트 같음)
       + 특상디\\_p8up\\_p8up_fill.json(Code 9/28 — 8판 글자층·쪽 그림으로 찾은 셋 P7-1153·1601·1879 · 새 19 답 대조)
       ⚠ 이 스크립트는 8판 PDF 를 읽지 않는다(구매자 워터마크가 든 글자층을 거치지 않는다 · 두 표만 쓴다)
  바꾸는 것 = 산출 넷
    jimun_7pan.json  — 지운 둘 · 글 8판(문장만 · 꼬리 태그/답/편 줄 그대로) · 답 셋 · 판8 칸 · 새 19(P8-·T8N) · 리담 34 표시(판8_리담) · 판/판8_기준/건수 · 연도색인
    mokcha_병합.json — 마디 지문: 지운 둘 빼고 새 19 넣음(표 마디id)
    p7_목차.json      — 지운 둘 빼기
    uid_alias.json    — 지운 둘(id·uid)을 가리키는 칸 빼기
  판8 칸 = {cat, t7?, a7?, pdf8?, p8?, no8?, 모아보기?} · cat = 명칭 · 기관 · 오류 · 자리 · 문장 · 답 · 없음 · 새(리담 표 = 있음)
  줄 대조 — 표의 uid · 책번호7 · a7 이 이번 원장 줄과 다르면 멈춘다(원장이 그 사이 바뀐 것 · 짐작해 얹지 않는다)

    python _p8up_apply.py [--data <jo/data>] [--out <폴더>] [--write]     (따로 돌리기 — ⚙ 밖에서 클론 데이터에 바로 얹기)
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import collections, hashlib, json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
MAT = os.path.join(HERE, '특상디', '_p8up')
REF = os.path.join(MAT, '_ref_p8up.json')
FILL = os.path.join(MAT, '_p8up_fill.json')
BASIS = '해례 8판 · 94f115f0 · 2026-09-27'
OFF = 10   # 8판 인쇄쪽 = PDF쪽 − 10
CAT = {'명칭만': '명칭', '기관 명칭(법 개정)': '기관', '우리 원장 글 오류': '오류', '자리만 옮김(글 같음)': '자리', '문장 바뀜 · 답 같음': '문장', '문장 바뀜 · 답 바뀜': '답'}
FILES = ('jimun_7pan.json', 'mokcha_병합.json', 'p7_목차.json', 'uid_alias.json')
WANT = {'명칭': 156, '기관': 7, '오류': 5, '자리': 3, '문장': 23, '답': 3, '없음': 6, '새': 19}   # 지시서 §B-1 · revfix0928pm §A-4 P7-1153 문장 → 자리


def dump_b(o):
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


def jload(p):
    return json.loads(open(p, 'rb').read().decode('utf-8'))


# ── 문장 / 꼬리 가르기 — 꼬리 = 문장 뒤 태그 [21 변리]·[미기출] · 「답 I x I」 · 「제N편 …」 줄(앱 p7Text 가 걷는 것) · 앞 빈칸·줄바꿈 포함 그대로 ──
TAILS = (re.compile(r'\s*\[\s*\d{2}(?:[\s·,]+\d{2})*\s*[가-힣]{1,4}\s*\]'), re.compile(r'\s*\[\s*미기출\s*\]'),
         re.compile(r'\s*답\s*[I|]\s*[OX]\s*[I|]'), re.compile(r'\n[ \t]*제\d+편[ \t]'))


def split_tail(t):
    cut = len(t)
    for rx in TAILS:
        m = rx.search(t)
        if m and m.start() < cut:
            cut = m.start()
    return t[:cut], t[cut:]


def p7text(t):   # 앱 p7Text 그대로(파이썬)
    x = re.sub(r'\[\s*\d{2}(?:[\s·,]+\d{2})*\s*변리\s*\]', '', t)
    x = re.sub(r'(^|\n)[ \t]*답[ \t]*[I|][^\n]*', '', x)
    x = re.sub(r'(^|\n)[ \t]*제\d+편[ \t]+[^\n]*$', '', x)
    return re.sub(r'[ \t]{2,}', ' ', re.sub(r'\s*\n\s*', ' ', x)).strip()


ws = lambda s: re.sub(r'\s+', '', s or '')


def no8n(s):
    """8판 번호 — 「14.」 → 14 · 「[유제]」 → 유제 · 「[유제2]」 → 유제2(괄호·끝 점 걷음)"""
    return re.sub(r'^\[|\]$', '', str(s or '').strip().rstrip('.'))


def apply(objs, ref, fill):
    """objs = {파일 이름: 읽은 dict}(자리에서 고친다) → (log, bad) · 이미 얹은 원장이면 (None, [])"""
    J, MK, TOC, AL = objs['jimun_7pan.json'], objs['mokcha_병합.json'], objs['p7_목차.json'], objs['uid_alias.json']
    if J.get('판') == '7+8':
        return None, []
    Z = J['지문']
    by = {z['id']: z for z in Z}
    log = collections.OrderedDict()
    bad, junk = [], []
    # ── 1 지우기 둘 ──
    dele = ref['delete']
    for i in dele:
        if i not in by:
            bad.append([i, '지울 줄이 원장에 없다'])
    if bad:
        return log, bad
    duid = {i: by[i]['uid'] for i in dele}
    J['지문'] = Z = [z for z in Z if z['id'] not in dele]
    for y, L in J['연도색인'].items():
        J['연도색인'][y] = [x for x in L if x not in dele]
    rm = collections.Counter()
    for m in MK['마디']:
        n0 = len(m['지문']); m['지문'] = [x for x in m['지문'] if x not in dele]; rm['마디'] += n0 - len(m['지문'])

    def walk(o):   # p7_목차 — 안쪽 목록까지(마디 열쇠 → 지문 id 목록)
        if isinstance(o, dict):
            for k in o:
                if isinstance(o[k], list) and any(x in dele for x in o[k] if isinstance(x, str)):
                    n0 = len(o[k]); o[k] = [x for x in o[k] if x not in dele]; rm['p7_목차'] += n0 - len(o[k])
                else:
                    walk(o[k])
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(TOC)
    for k in list(AL.get('map', {})):
        v = AL['map'][k]
        if any(('P7:' + i) == k for i in dele) or v in duid.values():
            del AL['map'][k]; rm['uid_alias.map'] += 1
    log['지움'] = {'id': dele, 'uid': duid, '빼낸 자리': dict(rm)}
    # ── 2 바뀐 197(+ 채팅이 못 뽑은 셋 = fill) ──
    cnt = collections.Counter()
    for i, v in ref['changed'].items():
        z = by.get(i)
        if not z:
            bad.append([i, '원장에 없는 줄']); continue
        if v.get('uid') and z.get('uid') != v['uid']:
            bad.append([i, 'uid 다름', z.get('uid'), v['uid']]); continue
        if v.get('책번호7') and str(z.get('책번호') or '') != str(v['책번호7']):
            bad.append([i, '책번호 다름', z.get('책번호'), v['책번호7']]); continue
        if v.get('a7') and z.get('ox') != v['a7']:
            bad.append([i, '7판 답 다름', z.get('ox'), v['a7']]); continue
        c = CAT[v['cat']]; t0 = z['t']
        p8 = {'cat': c}
        t8 = v.get('t8')
        f = fill['fill'].get(i)
        if not t8 and f:
            t8 = f['t8']
        pdf8 = v.get('pdf8') or (f and f.get('pdf8'))
        if c == '자리':
            m = re.search(r'p\.(\d+)', v.get('note') or '')
            if m:
                p8['p8'] = int(m.group(1)); p8['pdf8'] = p8['p8'] + OFF
            m2 = re.search(r'8판 (\d+)번', v.get('note') or '')
            if m2:
                p8['no8'] = m2.group(1)
        elif i == 'P7-2052':   # 우리 원장 글 오류 — 「답 I O I」 뒤 비교표 찌꺼기 걷기
            m = re.search(r'답\s*[I|]\s*[OX]\s*[I|]', t0)
            z['t'] = t0[:m.end()]
            p8['t7'] = t0
        elif t8:
            head, tail = split_tail(t0)
            z['t'] = t8 + tail
            p8['t7'] = t0
            if ws(split_tail(z['t'])[0]) != ws(t8):
                bad.append([i, '꼬리 가르기', repr(tail[:40])])
            rest = p7text(tail).strip()
            if rest and not re.fullmatch(r'\[[^\]]*\]', rest):
                junk.append([i, rest[:30]])   # 옛 원장 꼬리에 원래 붙은 것(답 뒤 장 제목 등) — 꼬리 그대로 · 목록만
        else:
            bad.append([i, 't8 없음'])
        if pdf8:
            p8['pdf8'] = int(pdf8)
        if f:
            p8['p8'] = f['p8']; p8['no8'] = no8n(f['no8'])
        if c == '답':
            p8['a7'] = z['ox']; z['ox'] = v['a8']
        z['판8'] = p8
        cnt[c] += 1
    # ── 3 8판에 없음 ──
    for i in ref['not_in_8']:
        if i not in by:
            bad.append([i, '원장에 없는 줄(없음)']); continue
        by[i]['판8'] = {'cat': '없음'}; cnt['없음'] += 1
    # ── 4 새 카드 19(8판 차례) ──
    new = [x for x in ref['new'] if x['할일'] == '새 카드']
    ans = {(a['p8'], a['no8']): a for a in fill['new19_ans']}
    mk = {m['id']: m for m in MK['마디']}
    uids = {z['uid'] for z in Z}
    n19 = []
    for k, x in enumerate(new, 1):
        a = ans.get((x['p8'], x['no8']))
        if not a or not a.get('same'):
            bad.append(['8판 p.%s %s' % (x['p8'], x['no8']), '답 대조 없음/다름']); continue
        nid, nuid = 'P8-%04d' % k, 'T8N%04d' % k
        if nid in by or nuid in uids:
            bad.append([nid, '새 열쇠가 겹친다', nuid]); continue
        # 글 = 8판 문장만(기존 미기출 줄처럼 태그 꼬리 없음 · 출처 칩 = 태그) · 쪽·pdf쪽·책번호 = 제7판 칸이라 비움(8판 자리는 판8 칸)
        e = {'id': nid, 'uid': nuid, 't': x['t8'], 'sol': '', '쪽': '', 'pdf쪽': '', '태그': x['tag8'].strip('[]'), '연도들': [],
             '책번호': '', 'ox': x['a8'], '유제': '유제' in x['no8'], '차례마디': x['마디'], '배지': '8판', '순': 9000 + k,
             '판8': {'cat': '새', 'p8': x['p8'], 'pdf8': x['pdf8'], 'no8': no8n(x['no8']), '모아보기': x.get('모아보기') or []}}
        Z.append(e); n19.append(nid); cnt['새'] += 1
        if x['마디id'] not in mk:
            bad.append([nid, '마디 없음', x['마디id']]); continue
        mk[x['마디id']]['지문'].append(nid)
    # ── 5 이미 앱 리담 카드 34 — 원장 안 작은 표(판8_리담 · uid → 8판 자리) ──
    lid = collections.OrderedDict()
    for x in ref['new']:
        if x['할일'] == '새 카드':
            continue
        L = x['lid'] or {}
        u = L['q'] if L.get('문항') else L.get('uid')   # 문항 통째(선지형 2026-63-2)면 그 문항 열쇠 · uid 다섯은 곁에
        e = {'cat': '있음', 'p8': x['p8'], 'pdf8': x['pdf8'], 'no8': no8n(x['no8']), 'q': L.get('q'), '마디id': x['마디id'], '모아보기': x.get('모아보기') or []}
        if L.get('문항'):
            e['문항'] = True; e['uids'] = L.get('uid') or []
        lid[u] = e
    J['판8_리담'] = lid
    # ── 6 머리 ──
    J['건수'] = len(Z)
    J['판'] = '7+8'
    J['판8_기준'] = BASIS
    log['판8.cat'] = dict(cnt)
    log['지문 수'] = [len(by), len(Z)]
    log['새 19'] = [n19[0], n19[-1]] if n19 else None
    log['리담 표시'] = len(lid)
    log['꼬리에 원래 붙은 글(그대로 · 목록)'] = junk
    return log, bad


def build(dump, 검산, out):
    """⚙ jo_build [6d] — 이번 산출(out) 넷에 8판을 얹어 dump 로 다시 쓴다 · 어긋나면 멈춘다(예외 → ⚙ NG · 아무것도 안 나감)"""
    objs = {f: jload(os.path.join(out, f)) for f in FILES}
    log, bad = apply(objs, jload(REF), jload(FILL))
    if log is None:
        검산.chk('P8', '해례 8판 판올림(p8up)', 'INFO', '이미 얹은 원장 — 그대로', '판 7+8')
        return
    if bad:
        raise RuntimeError('p8up — 표와 원장이 어긋난다 %d: %s' % (len(bad), json.dumps(bad[:6], ensure_ascii=False)))
    for f in FILES:
        dump(f, objs[f])
    c = log['판8.cat']
    ok = c == WANT and log['지문 수'][1] == log['지문 수'][0] - 2 + 19 and log['리담 표시'] == 34
    검산.gate('P8', '해례 8판 판올림(p8up)', ok,
              '지문 %d → %d · %s · 리담 표시 %d' % (log['지문 수'][0], log['지문 수'][1], ' '.join('%s %d' % kv for kv in c.items()), log['리담 표시']),
              '지움 2 · 새 19 · 명칭 156 기관 7 오류 5 자리 3 문장 23 답 3 없음 6 · 리담 34',
              비고='꼬리 찌꺼기(그대로) %d: %s' % (len(log['꼬리에 원래 붙은 글(그대로 · 목록)']), ', '.join(x[0] for x in log['꼬리에 원래 붙은 글(그대로 · 목록)'])))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    A = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    data = A('--data', _roots.genie(r'jo\data'))
    out = A('--out', data)
    write = '--write' in sys.argv
    raws = {f: open(os.path.join(data, f), 'rb').read() for f in FILES}
    objs = {f: json.loads(raws[f].decode('utf-8')) for f in FILES}
    for f in FILES:
        if dump_b(objs[f]) != raws[f]:
            sys.exit('NG %s json 왕복이 바이트가 다르다 — 멈춤' % f)
    log, bad = apply(objs, jload(REF), jload(FILL))
    if log is None:
        print('이미 얹은 원장(판 7+8 · %s) — 그대로(멱등)' % objs['jimun_7pan.json'].get('판8_기준'))
        return
    log['어긋남'] = bad
    for k, v in log.items():
        print('%s: %s' % (k, json.dumps(v, ensure_ascii=False)))
    if bad:
        sys.exit('NG 어긋남 %d — 안 씀' % len(bad))
    os.makedirs(out, exist_ok=True)
    for f in FILES:
        b = dump_b(objs[f])
        print('%s %d → %d B · md5 %s → %s%s' % (f, len(raws[f]), len(b), hashlib.md5(raws[f]).hexdigest()[:8], hashlib.md5(b).hexdigest()[:8], '' if b != raws[f] else ' (같음)'))
        if write and b != raws[f]:
            p = os.path.join(out, f)
            for _ in range(5):
                open(p, 'wb').write(b); time.sleep(0.5)
                if open(p, 'rb').read() == b:
                    break
            else:
                sys.exit('NG %s 되읽기가 다르다' % p)
    if not write:
        print('(재기만 · --write 로 쓴다)')


if __name__ == '__main__':
    main()
