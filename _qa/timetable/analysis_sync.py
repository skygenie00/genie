# -*- coding: utf-8 -*-
r"""시험분석 md 동기화 (2026-09-05 · timetable/_task_tt_exam_pan2.md · §A 답 ④ 파일 규약)
    python analysis_sync.py [--dry]
N:\개인\claude\timetable\_분석_*.md · _전략.md(채팅이 낸다 · 읽기만) → <SPD_ROOT>\exam\analysis\… 로 복사 + index.json 갱신(회차 · 사람 · 꼴 · 파일 · 강사 criteria 목록).
「md 를 떨구면 뜬다」 = 이 스크립트 한 번 + studyplandata push(사람이 mb_push 또는 Code 가 git).
채점(9/16 · jopangi/_task_cha2_report.md §D) — genie jo/data/2cha_채점_<과목>.json(⚙ 산출)을 기출 회차별로 exam/analysis/<회>-2/채점_<과목>.json 에 복사 · 색인 = index 최상위 grades[](9/17 — items[].files[] 에 두면 새로고침 안 된 옛 tt 가 JSON 을 글 md 로 그린다) ·
그 회차·과목·사람의 v2 레코드가 있으면 <과목>_<사람>.md 를 pred_md_from_grade() 로 덮어쓴다 · v2 가 없으면 md 그대로.
⚠ 2026-09-18 — 볼트 쓰기 방향은 껐다(`VAULT_WRITE=False` · add1 §A-2). 볼트 md 는 **읽기만** 한다.
이름 규약: _분석_1차_63회.md → 63-1/분석.md · _분석_2차_62회_민문1.md → 62-2/민문1.md · _분석_2차_62회_머리.md → 62-2/머리.md · _전략.md → strategy.md
사람 = md 머리 「사람: 햄찌」 줄 > 제목에 든 이름 > 꼬까. 예측 = 「예측: true」 줄. 꼴(2차 문제 md) = 「## 요소」 절 + 표 있으면 table · 없으면 text.
멱등 · 같은 md 면 바이트 무변."""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import os, re, sys, json, glob, hashlib, time
N = r'N:\개인\claude\timetable'; SPD = _roots.spd(r'exam'); ANA = os.path.join(SPD, 'analysis')
PEOPLE = ['꼬까', '햄찌']
def rel(p): return p.replace('\\', '/')
def parse_name(fn):
    m = re.match(r'_분석_(\d)차_(\d+)회(?:_(.+))?\.md$', fn)
    if m:
        cha, no, tail = int(m.group(1)), int(m.group(2)), m.group(3)
        if cha == 1: return no, cha, '분석.md'
        return no, cha, (tail or '머리') + '.md'
    if re.match(r'_(시험)?전략\.md$', fn): return 0, 0, 'strategy.md'
    return None
def head_info(txt):
    lines = txt.split('\n'); who = None; pred = False; title = ''
    for ln in lines[:12]:
        m = re.match(r'^사람:\s*(\S+)', ln)
        if m: who = m.group(1)
        if re.match(r'^예측:\s*(true|예|1)', ln, re.I): pred = True
        if ln.startswith('# ') and not title: title = ln[2:].strip()
    if not who:
        for p in PEOPLE:
            if p in title: who = p; break
    if not who: who = PEOPLE[0]
    kind = 'table' if re.search(r'^## 요소', txt, re.M) and '|---' in txt else 'text'
    return who, pred, title, kind
# ── 9/16 채점결과분석(jopangi/_task_cha2_report.md §D-1·§D-3) ─────────────────────────────
GENIE_DATA = _roots.genie(r'jo\data')          # ⚙ 산출(조판기가 읽는 것) — 원천 하나
VAULT = os.path.join(os.path.expanduser('~'), 'Documents', "PA's archive", '변리사 시험')
GRADE_LAWS = ('특허', '상표', '민소', '디보')
GRADE_RX = re.compile(r'^2차(\d{2})-(\d+)-(\d+)$')
PRED_BAN = ('보완 시', '×0.6', '실점', '실수령', '보정 규칙')
GEN_BODY = '정본 = 볼트 채점표(v2) · 화면 = 채점 탭 · 실제점수환산은 계수 판 뒤'   # 생성기 본문 한 줄 — 이 줄이 든 md 는 이미 생성된 것(옮길 산문 없음)


def grade_split(G):
    """⚙ 산출 한 법 → {회: {카드키: {'회차': [레코드…]}}} — 기출 레코드만(사례·GS 는 시험 회차가 아니다)"""
    out = {}
    for ck, v in G.items():
        if ck == '_meta':
            continue
        for r in v.get('회차', []):
            m = GRADE_RX.match(r.get('기출') or '')
            if m:
                out.setdefault(int(m.group(2)), {}).setdefault(ck, {'회차': []})['회차'].append(r)
    return out


def grade_sync(items, dry, data_dir=GENIE_DATA, ana=None):
    """§D-1 — ⚙ 채점 JSON 을 exam/analysis/<회>-2/채점_<과목>.json 으로 복사(기출 회차별로 가름) · 멱등
       → (made, 씀, 같음, grades) · grades = index 최상위 항목 {no, cha, subj, name, path, kind 'grade', who[], v2, title, bytes, md5}
       ⚠ items[].files[] 에는 넣지 않는다(9/17) — 72c5c1d 까지의 tt 는 files[] 중 머리·문항·과목 md 밖을 전부 「글 md」로 격자 아래에 그려
         새로고침 안 된 기기(열어 둔 탭·아이패드 PWA 는 visibilitychange 로 데이터만 새로 받는다)에서 JSON 이 날글자로 떴다. 사람 항목(회차 칩)만 만든다(files 빈 채)."""
    ana = ana or ANA; made = []; grades = []; n_w = n_same = 0
    for law in GRADE_LAWS:
        p = os.path.join(data_dir, '2cha_채점_%s.json' % law)
        if not os.path.isfile(p):
            continue
        G = json.load(open(p, encoding='utf-8'))
        for no, cards in sorted(grade_split(G).items()):
            recs = [r for k in sorted(cards) for r in cards[k]['회차']]
            meta = {'원천': 'genie jo/data/2cha_채점_%s.json' % law, '법': law, '회': no, '카드': len(cards), '레코드': len(recs),
                    'v2': sum(1 for r in recs if r.get('v') == 2), '시각': (G.get('_meta') or {}).get('시각', ''), '원본': sorted(set(r.get('원본', '') for r in recs))}
            obj = {k: cards[k] for k in sorted(cards)}; obj['_meta'] = meta
            b = json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
            name = '채점_%s.json' % law; dst = os.path.join(ana, '%d-2' % no, name)
            if os.path.isfile(dst) and open(dst, 'rb').read() == b:
                n_same += 1
            else:
                if not dry:
                    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(b)
                n_w += 1
            ent = {'no': no, 'cha': 2, 'subj': law, 'name': name, 'path': 'exam/analysis/%d-2/%s' % (no, name), 'kind': 'grade',
                   'who': sorted(set(x for r in recs for x in (r.get('사람') or []))), 'v2': meta['v2'],
                   'title': '%d회 2차 %s 채점(⚙ 산출 · v2 %d/%d)' % (no, law, meta['v2'], len(recs)), 'bytes': len(b), 'md5': hashlib.md5(b).hexdigest()[:8]}
            grades.append(ent)
            for who in ent['who']:
                key = '%d-2-%s' % (no, who)
                items.setdefault(key, {'id': key, 'no': no, 'cha': 2, 'who': who, 'files': []})
            made.append((no, law, recs))
            print('채점 %s → %s (카드 %d · 레코드 %d · v2 %d) %d B' % (os.path.basename(p), ent['path'], len(cards), len(recs), meta['v2'], len(b)))
    return made, n_w, n_same, grades


def pred_md_from_grade(recs, no, subj, who):
    """§D-3 — 그 회차·과목·사람의 v2 레코드 → 예측 md 글(제목 · 메타 세 줄 · 본문 한 줄) · v2 레코드가 없으면 None
       문항별 = ⚙ 가 설문 점수에서 계산한 문제 합(레코드 `합계`) · 「보완 시」·「×0.6」·「실점」·「보정 규칙」·「실수령」 없음 · 예측점수(환산)는 계수 판 뒤"""
    by_q = {}
    for r in recs:
        m = GRADE_RX.match(r.get('기출') or '')
        if r.get('v') == 2 and who in (r.get('사람') or []) and m and int(m.group(2)) == int(no):
            by_q[int(m.group(3))] = r
    if not by_q:
        return None
    vals = [((by_q.get(q) or {}).get('합계') or {}).get(who) for q in (1, 2, 3, 4)]
    vals = [None if not h or h.get('점수') is None else h['점수'] for h in vals]
    f = lambda v: '—' if v is None else ('%g' % v)
    tot = sum(v for v in vals if v is not None)
    # ★ 2026-09-18 (_task_cha2_all_add1 §B-2) — 제목에서 「원점수」를 뺐다(제목에 점수 이름표를 안 붙인다 · 2-6)
    return '\n'.join(['# %d회 2차 · %s 예측 (%s) — 문항별 %s · 합 %s' % (int(no), subj, who, '/'.join(f(v) for v in vals), f(tot)),
                      '사람: %s' % who, '예측: true', '문항별: %s' % ' / '.join(f(v) for v in vals), '',
                      GEN_BODY, ''])


def pred_move_lines(old_md, vault_text):
    """덮어쓰기 전 — 옛 예측 md 의 산문 줄 중 볼트 채점표에 없는 줄 → (옮길 줄[], 안 옮긴 줄[(줄, 까닭)]) · 점수 숫자 줄 · 보완/×0.6 줄은 안 옮긴다"""
    norm = lambda s: re.sub(r'\s+', ' ', s or '').strip()
    vt = norm(vault_text); move, skip = [], []
    for ln in (old_md or '').replace('\r\n', '\n').split('\n'):
        s = ln.strip()
        if not s:
            continue
        why = ('헤딩' if s.startswith('#') else '메타' if re.match(r'^(사람|예측|채점기준|문항별):', s) else '표(점수)' if s.startswith('|')
               else '보완·×0.6' if ('보완' in s or '×0.6' in s) else '점수 숫자 줄' if re.search(r'점수\s*=|\d+(?:\.\d+)?\s*/\s*\d+(?:\.\d+)?', s) else '')
        if why:
            skip.append((s, why)); continue
        if norm(s) not in vt:
            move.append(s)
    return move, skip


VAULT_WRITE = False   # ★ 2026-09-18 (_task_cha2_all_add1 §A-2) — 볼트 쓰기 방향을 껐다.
#   9/16 G-9 의 「예측 md 산문 → 볼트 코멘트」는 **옛 6장 변환용**이었다. 지금은 `_v2` 가 정본이고
#   흐름이 볼트 md → 채점 JSON → studyplandata 한쪽뿐이라, 되돌려 쓰면 코멘트 표·산문과 같은 글이
#   꼬리에 한 벌 더 쌓인다(9/18 민소 +20줄 · 특허 +37줄이 실제로 그렇게 생겨 사용자가 되돌리라 했다).
#   함수는 남겨 둔다 — 옛 꼴 변환을 다시 할 일이 생기면 이 값만 True 로.


def vault_append(path, lines, no, dry=False):
    """볼트 v2 채점표 맨 아래(코멘트 산문 끝)에 `<줄> ← <회>-2 예측 md` · 이미 있는 줄은 안 붙인다(멱등)
       ⚠ `VAULT_WRITE` 가 False 면 **아무것도 안 쓴다**(§A-2) — 볼트는 읽기 전용이다."""
    if not VAULT_WRITE:
        return []
    s = open(path, encoding='utf-8').read()
    tail = ['%s ← %d-2 예측 md' % (ln, int(no)) for ln in lines]
    tail = [t for t in tail if t not in s]
    if tail and not dry:
        b = (s.rstrip('\n') + '\n\n' + '\n'.join(tail) + '\n').encode('utf-8')
        open(path, 'wb').write(b); time.sleep(0.5)
        assert open(path, 'rb').read() == b
    return tail


def pred_sync(items, made, dry, ana=None, vault=VAULT):
    """§D-3 — v2 레코드가 있는 회차·과목·사람만 <과목>_<사람>.md 를 덮어쓴다(옛 산문 줄은 볼트로 먼저) · 없으면 그 md 그대로"""
    ana = ana or ANA; report = []
    for no, law, recs in made:
        for who in PEOPLE:
            md = pred_md_from_grade(recs, no, law, who)
            if md is None:
                continue
            name = '%s_%s.md' % (law, who); dst = os.path.join(ana, '%d-2' % no, name)
            old = open(dst, encoding='utf-8').read() if os.path.isfile(dst) else ''
            src = sorted(set(r.get('원본', '') for r in recs if r.get('v') == 2 and who in (r.get('사람') or [])))
            moved, skipped = [], []
            if old and src and GEN_BODY not in old:
                vp = os.path.join(vault, src[0])
                if os.path.isfile(vp):
                    mv, skipped = pred_move_lines(old, open(vp, encoding='utf-8').read())
                    moved = vault_append(vp, mv, no, dry)
            b = md.encode('utf-8')
            if not dry:
                os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(b)
            it = items.setdefault('%d-2-%s' % (no, who), {'id': '%d-2-%s' % (no, who), 'no': no, 'cha': 2, 'who': who, 'files': []})
            title = md.split('\n')[0][2:]
            ent = {'name': name, 'path': 'exam/analysis/%d-2/%s' % (no, name), 'kind': 'text', 'pred': True, 'title': title, 'bytes': len(b), 'md5': hashlib.md5(b).hexdigest()[:8]}
            it['files'] = [f if f['name'] != name else ent for f in it['files']] if any(f['name'] == name for f in it['files']) else it['files'] + [ent]
            report.append({'md': ent['path'], '옮김': len(moved), '안 옮김': skipped})
            print('예측 md 생성 %s — 볼트로 옮긴 줄 %d · 안 옮긴 줄 %d' % (ent['path'], len(moved), len(skipped)))
    return report


def main():
    dry = '--dry' in sys.argv; os.makedirs(ANA, exist_ok=True); items = {}; copied = 0; same = 0
    for src in sorted(glob.glob(os.path.join(N, '_분석_*.md')) + glob.glob(os.path.join(N, '_전략.md')) + glob.glob(os.path.join(N, '_시험전략.md'))):
        fn = os.path.basename(src); pn = parse_name(fn)
        if not pn: print('이름 규약 밖 · 건너뜀', fn); continue
        no, cha, name = pn; raw = open(src, 'rb').read(); txt = raw.decode('utf-8').replace('\r\n', '\n')
        who, pred, title, kind = head_info(txt)
        if name == 'strategy.md': dst = os.path.join(SPD, 'strategy.md'); path = 'exam/strategy.md'
        else: d = os.path.join(ANA, '%d-%d' % (no, cha)); os.makedirs(d, exist_ok=True); dst = os.path.join(d, name); path = 'exam/analysis/%d-%d/%s' % (no, cha, name)
        b = txt.encode('utf-8')
        if os.path.isfile(dst) and open(dst, 'rb').read() == b: same += 1
        else:
            if not dry: open(dst, 'wb').write(b)
            copied += 1
        print('%s → %s (%s · %s · %s%s) %d B' % (fn, path, who, kind, title[:30], ' · 예측' if pred else '', len(b)))
        if name == 'strategy.md': continue
        key = '%d-%d-%s' % (no, cha, who); it = items.setdefault(key, {'id': key, 'no': no, 'cha': cha, 'who': who, 'files': []})
        it['files'].append({'name': name, 'path': path, 'kind': 'md' if cha == 1 else ('head' if name == '머리.md' else kind), 'pred': pred, 'title': title, 'bytes': len(b), 'md5': hashlib.md5(b).hexdigest()[:8]})
    made, g_w, g_same, grades = grade_sync(items, dry)
    pred = pred_sync(items, made, dry)
    crit = []
    for f in sorted(glob.glob(os.path.join(ANA, 'criteria', '*.json'))):
        m = re.match(r'(\d+)-(\d)-(.+?)-(.+?)\.json$', os.path.basename(f))
        if m: crit.append({'no': int(m.group(1)), 'cha': int(m.group(2)), 'subj': m.group(3), 'by': m.group(4), 'path': 'exam/analysis/criteria/' + os.path.basename(f)})
    idx = {'v': 1, 'items': sorted(items.values(), key=lambda x: (-x['no'], x['cha'], x['who'])), 'criteria': crit, 'strategy': os.path.isfile(os.path.join(SPD, 'strategy.md')), 'grades': grades}
    ip = os.path.join(ANA, 'index.json'); txt = json.dumps(idx, ensure_ascii=False, indent=1) + '\n'
    if not dry and (not os.path.isfile(ip) or open(ip, encoding='utf-8').read() != txt): open(ip, 'w', encoding='utf-8', newline='\n').write(txt); print('index.json 갱신')
    print('회차 %d · 파일 복사 %d · 같음 %d · 채점 JSON 씀 %d · 같음 %d · 예측 md 생성 %d · criteria %d · strategy %s' % (len(items), copied, same, g_w, g_same, len(pred), len(crit), idx['strategy']))
if __name__ == '__main__': main()
