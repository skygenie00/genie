# -*- coding: utf-8 -*-
"""tt 시험분석 = 채점결과분석 세 구간 · 예측 md 생성기 (2026-09-16 · jopangi/_task_cha2_report.md §D · G-9 · G-7)

A. G-9 생성기 픽스처 — 판정·점수를 손으로 채운 가짜 v2 채점표 한 장(볼트 밖 임시 자리)으로 ⚙ build_all → analysis_sync.grade_sync → pred_sync
   → md = 제목·메타 세 줄·한 줄뿐 · 금지어 0 · 문항별 = 설문 합 · 옛 md 산문 줄 → 가짜 볼트 코멘트 끝(멱등) · 헤드리스 tt mdParse·anaQvals 가 그 md 를 읽는다
B. tt 화면 — 시드(index · 63-2 특허 예측 md · 채점 JSON)로 시험분석 2차 63회 햄찌 · 문항 칸 「특허2」 → .c2r 세 구간 · 칸 요약 줄 = v2 누락·답틀 · 채점 JSON 이 글 md 로 안 그려짐
   · 채점 파일을 빼면 종전 화면(.c2r 0)
C. (9/17) 채점 색인 = index 최상위 grades[] — 옛 앱(72c5c1d · 새로고침 안 된 기기)·9/16 판(d5729f0)이 새 index 에서 JSON 을 글로 안 그림 ·
   헛잣대 = 옛 앱 + 9/16 판 index 꼴(files[] kind grade) → JSON 날글자(사용자 신고 재현) · 캐시 sha ≠ index md5 면 그 캐시로 안 그림

쓰기 : python _harness_cha2_report_tt.py --new <패치 tt.html> --head <9/16 판 tt.html(d5729f0)> --old <옛 tt.html(72c5c1d)> --v2 <변환본 뿌리(2차채점\…_v2.md)> [--out 폴더]
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import argparse, html as HT, json, os, re, subprocess, sys, shutil, hashlib, io
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'N:\개인\claude\jopangi'); sys.path.insert(0, r'N:\개인\claude\timetable')
import grade_build as GB
import analysis_sync as AS

ap = argparse.ArgumentParser()
ap.add_argument('--new', required=True); ap.add_argument('--head', required=True); ap.add_argument('--old', required=True); ap.add_argument('--v2', required=True)
ap.add_argument('--out', default=os.path.join(os.environ['TEMP'], 'c2r_tt_h'))
A = ap.parse_args()
OUT = os.path.abspath(A.out); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ANCHOR = "<script>\n/* ============================================================\n   타임테이블 v1"
SPD = _roots.spd(r'exam\analysis')
R = []
T = lambda n, c, i=None: R.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c or i is None else ' | ' + str(i)[:300]))
I = lambda n, v: R.append('INFO | ' + n + ' | ' + str(v)[:400])

# ───────── A. G-9
real_md5 = {f: hashlib.md5(open(os.path.join(SPD, '63-2', f), 'rb').read()).hexdigest() for f in sorted(os.listdir(os.path.join(SPD, '63-2')))}
vault = os.path.join(OUT, 'vault'); ana = os.path.join(OUT, 'analysis'); data = os.path.join(OUT, 'data')
src_v2 = os.path.join(A.v2, '2차채점', '특허', '특기출채 26-63-260809-햄찌꼬까_v2.md')
dst = os.path.join(vault, '2차채점', '특허', '특기출채 26-63-260809-햄찌꼬까.md')     # 교체 뒤 꼴(접미 없음)
os.makedirs(os.path.dirname(dst)); s = io.open(src_v2, encoding='utf-8', newline='').read()
# 손으로 채운 판정·점수 — 햄찌 문1 설문(1) 목차 첫 세 줄 O/△/X · 점수 5.5→6 · 꼬까 문3 설문(2) 6.5→7
L = s.split('\n'); k = L.index('> [!목차 햄찌] ← [[특기출 26-63-1-침해금지(진보성 항변·자백)·손해배상(128조 종합)#햄찌과거문]] Ⅰ. 설문(1) (10점)')
for off, m in ((1, 'O'), (2, '△'), (3, 'X')):
    L[k + off] = L[k + off] + ' ' + m
j = L.index('- 점수 햄찌: 5.5', k); L[j] = '- 점수 햄찌: 6'
kk = next(i for i, x in enumerate(L) if x.startswith('## 설문(2) (10점)') and i > next(t for t, y in enumerate(L) if y.startswith('# 문제3')))
j2 = L.index('- 점수 꼬까: 6.5', kk); L[j2] = '- 점수 꼬까: 7'
io.open(dst, 'w', encoding='utf-8', newline='').write('\n'.join(L))
DATA = _roots.genie(r'jo\data')
cards, board, precs = GB.load_data(DATA)
final, RR = GB.build_all(vault, cards, board, {law: GB.prec_index(rows) for law, rows in precs.items()})
os.makedirs(data)
json.dump(final['특허'], open(os.path.join(data, '2cha_채점_특허.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
items = {}
made, gw, gs, gents0 = AS.grade_sync(items, False, data_dir=data, ana=ana)
T('G-9 픽스처 ⚙ → 채점_특허.json 63-2 · v2 레코드 4', len(made) == 1 and made[0][0] == 63 and sum(1 for r in made[0][2] if r.get('v') == 2) == 4, [(m[0], m[1], len(m[2])) for m in made])
g0 = gents0[0] if len(gents0) == 1 else {}
T('D-1(9/17) index 최상위 grades[] 1건 — no 63 · cha 2 · subj 특허 · who 꼬까·햄찌 · v2 4 · md5 = 쓴 파일 · 사람 항목 둘 files[] 빈 채(grade 0)',
  g0.get('no') == 63 and g0.get('cha') == 2 and g0.get('subj') == '특허' and g0.get('who') == ['꼬까', '햄찌'] and g0.get('v2') == 4 and g0.get('kind') == 'grade'
  and g0.get('md5') == hashlib.md5(open(os.path.join(ana, '63-2', '채점_특허.json'), 'rb').read()).hexdigest()[:8]
  and sorted(items) == ['63-2-꼬까', '63-2-햄찌'] and all(x['files'] == [] for x in items.values()), [gents0, items])
os.makedirs(os.path.join(ana, '63-2'), exist_ok=True)
old_md = io.open(r'N:\개인\claude\timetable\_분석_2차_63회_특허_햄찌.md', encoding='utf-8').read().replace('\r\n', '\n')
io.open(os.path.join(ana, '63-2', '특허_햄찌.md'), 'w', encoding='utf-8', newline='\n').write(old_md)
vault_before = open(dst, 'rb').read()
rep1 = AS.pred_sync(items, made, False, ana=ana, vault=vault)
md = io.open(os.path.join(ana, '63-2', '특허_햄찌.md'), encoding='utf-8', newline='').read()
lines = md.split('\n')
I('G-9 생성 md', ' ⏎ '.join(lines))
T('G-9 md = 제목 · 메타 세 줄 · 빈 줄 · 본문 한 줄(끝 줄바꿈)', len(lines) == 7 and lines[0].startswith('# ') and lines[1].startswith('사람: ') and lines[2] == '예측: true' and lines[3].startswith('문항별: ') and lines[4] == '' and lines[5] == '정본 = 볼트 채점표(v2) · 화면 = 채점 탭 · 실제점수환산은 계수 판 뒤' and lines[6] == '', lines)
T('G-9 제목 꼴 「63회 2차 · 특허 예측 (햄찌) — 원점수 문항별 a/b/c/d · 합 N」', bool(re.match(r'^# 63회 2차 · 특허 예측 \(햄찌\) — 원점수 문항별 [\d.]+/[\d.]+/[\d.]+/[\d.]+ · 합 [\d.]+$', lines[0])), lines[0])
bad = [w for w in ('보완 시', '×0.6', '실점', '실수령', '보정 규칙') if w in md]
T('G-9 「보완 시」·「×0.6」·「실점」·「실수령」·「보정 규칙」 0', not bad, bad)
recs = {int(re.search(r'-(\d+)$', r['기출']).group(1)): r for r in made[0][2] if r.get('v') == 2}
want = [round(sum(v['v'] for v in recs[q]['점수']['햄찌'].values()), 2) for q in (1, 2, 3, 4)]
got = [float(x) for x in lines[3].split(':', 1)[1].split('/')]
T('G-9 문항별 = 설문 점수 합(손으로 바꾼 문1 설(1) 6 반영) %s' % want, got == want and want[0] == 15, [got, want])
T('G-9 합 = 문항별 합', abs(float(lines[0].rsplit('합 ', 1)[1]) - sum(want)) < 0.01, lines[0])
r_h = next((x for x in rep1 if x['md'].endswith('특허_햄찌.md')), None); moved = r_h['옮김'] if r_h else -1; skipped = r_h['안 옮김'] if r_h else []
vt = open(dst, encoding='utf-8').read()
tail = [x for x in vt.split('\n') if x.endswith('← 63-2 예측 md')]
T('G-9 옛 md 산문 줄 중 볼트에 없는 줄 → 볼트 코멘트 끝 「← 63-2 예측 md」 %d줄 · 안 옮긴 줄 %d(점수·보완·헤딩·메타·표)' % (moved, len(skipped)), moved > 0 and len(tail) == moved and vt.rstrip('\n').endswith('← 63-2 예측 md'), [moved, len(tail)])
kinds = {}
for s1, why in skipped:
    kinds[why] = kinds.get(why, 0) + 1
I('G-9 안 옮긴 줄 갈래', kinds)
T('G-9 옮긴 줄에 보완·×0.6·점수 숫자 줄 0', not any(('보완' in x or '×0.6' in x or re.search(r'점수\s*=', x)) for x in tail), [x for x in tail if '보완' in x or '×0.6' in x][:3])
vault_after1 = open(dst, 'rb').read(); md1 = md
io.open(os.path.join(ana, '63-2', '특허_햄찌.md'), 'w', encoding='utf-8', newline='\n').write(old_md)   # 다음 동기화 = 원천 md 가 다시 복사된 꼴
rep2 = AS.pred_sync(items, made, False, ana=ana, vault=vault)
T('G-9 멱등 — 두 번째 돌리면(햄찌 = 원천 md 다시 복사된 꼴 · 꼬까 = 이미 생성된 md) 볼트 바이트 무변 · md 같음 · 옮긴 줄 0', all(x['옮김'] == 0 for x in rep2) and open(dst, 'rb').read() == vault_after1 and io.open(os.path.join(ana, '63-2', '특허_햄찌.md'), encoding='utf-8', newline='').read() == md1, [x['옮김'] for x in rep2])
T('G-9 v2 레코드 없는 과목(민소)은 생성 안 함', AS.pred_md_from_grade([], 63, '민소', '햄찌') is None and all(r['md'].endswith('특허_햄찌.md') or r['md'].endswith('특허_꼬까.md') for r in rep1), [r['md'] for r in rep1])
json.dump({'md': md1, 'items': items, 'moved_tail': tail, 'skipped': skipped}, open(os.path.join(OUT, 'g9.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ───────── B. tt 화면(헤드리스 · 시드)
fx = {law: json.load(open(os.path.join(A.v2, '..', 'fx2', '2cha_채점_%s.json' % law), encoding='utf-8')) for law in ('특허', '민소')}
idx = json.load(open(os.path.join(SPD, 'index.json'), encoding='utf-8'))
seed_files = {'exam/analysis/index.json': None}
it = next(x for x in idx['items'] if x['id'] == '63-2-햄찌')
md_ent = {f['name']: f for f in it['files'] if f.get('kind') != 'grade'}
for name, f in md_ent.items():
    seed_files[f['path']] = (io.open(os.path.join(SPD, '63-2', name), encoding='utf-8', newline='').read().replace('\r\n', '\n'), f['md5'])
gfiles = []; gents = []
for law in ('특허', '민소'):
    sp = AS.grade_split(fx[law]).get(63) or {}
    obj = {k: sp[k] for k in sorted(sp)}; obj['_meta'] = {'법': law, '회': 63}
    b = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    m5 = hashlib.md5(b.encode('utf-8')).hexdigest()[:8]
    ent = {'name': '채점_%s.json' % law, 'path': 'exam/analysis/63-2/채점_%s.json' % law, 'kind': 'grade', 'pred': False, 'title': '', 'bytes': len(b.encode('utf-8')), 'md5': m5}   # 9/16 판 꼴(files[])
    gfiles.append(ent); seed_files[ent['path']] = (b, m5)
    gents.append({'no': 63, 'cha': 2, 'subj': law, 'name': ent['name'], 'path': ent['path'], 'kind': 'grade', 'who': ['꼬까', '햄찌'], 'v2': 4, 'title': '', 'bytes': ent['bytes'], 'md5': m5})   # 9/17 꼴(최상위 grades[])


def page(src_html, layout, prob, tag, sha_ok=True):
    """layout = None(채점 없음) · 'grades'(9/17 꼴) · 'files'(9/16 판 꼴 = 햄찌 항목 files[] 에 kind grade) · sha_ok False = 채점 JSON 캐시 sha 없음(9/16 판 anaJSON 꼴)"""
    idx2 = json.loads(json.dumps(idx)); idx2.pop('grades', None)
    for x in idx2['items']:
        x['files'] = [f for f in x['files'] if f.get('kind') != 'grade']
        if x['id'] == '63-2-햄찌' and layout == 'files':
            x['files'] = x['files'] + gfiles
    if layout == 'grades':
        idx2['grades'] = gents
    seeds = {}
    for p, v in seed_files.items():
        if p == 'exam/analysis/index.json':
            seeds['tt.f.' + p] = {'data': idx2, 'sha': None, 'dirty': False}
        elif '/채점_' in p:
            if layout:
                seeds['tt.f.' + p] = {'data': v[0], 'sha': v[1] if sha_ok else None, 'dirty': False}
        else:
            seeds['tt.f.' + p] = {'data': v[0], 'sha': v[1], 'dirty': False}
    ui = {'view': 'arch', 'archTab': 'exam', 'exTab': 'ana', 'exAna': 2, 'ana': {'sel2': '63-2-햄찌', 'prob': prob}}
    seed = ("<script>localStorage.clear();window.__errs=[];addEventListener('error',e=>__errs.push(String(e.message)));"
            "window.fetch=()=>Promise.reject(new Error('harness: network blocked'));"
            "localStorage.setItem('tt.cfg',JSON.stringify({person:'햄찌',token:'',lastSync:0}));"
            "localStorage.setItem('tt.ui',%s);const __S=%s;Object.keys(__S).forEach(k=>localStorage.setItem(k,JSON.stringify(__S[k])));</script>") % (json.dumps(json.dumps(ui, ensure_ascii=False)), json.dumps(seeds, ensure_ascii=False))
    test = r"""<script>(function(){const out={};try{render();const m=document.getElementById('main');const c=m.querySelectorAll('.c2r');out.c2r=c.length;
 out.sec=c.length?c[0].querySelectorAll(':scope>section').length:0;out.sl=c.length?c[0].querySelectorAll('div.c2r-sl').length:0;
 out.slLeft=c.length?[...c[0].querySelectorAll('div.c2r-sl')].every(x=>getComputedStyle(x).textAlign==='left'):false;
 out.cur=c.length&&c[0].querySelector('table.c2r-st th.c2r-cur')?c[0].querySelector('table.c2r-st th.c2r-cur').textContent:'';
 out.tg=c.length?c[0].querySelectorAll('.c2r-tg b').length:0;out.cmp=c.length?c[0].querySelectorAll('.c2r-cmp').length:0;
 const cells=[...m.querySelectorAll('table.anagrid tr')].map(tr=>[...tr.children].map(td=>td.textContent.replace(/\s+/g,' ').trim()));out.grid=cells;
 const sums=[...m.querySelectorAll('table.anagrid td .anasum')].map(x=>x.textContent);out.sums=sums;
 out.anatext=m.querySelectorAll('.anatext').length;out.anaprob=m.querySelectorAll('.anaprob').length;out.jsonText=/"회차":\[|"_meta"/.test(m.textContent);
 out.qv=(typeof mdParse==='function'&&window.__G9MD)?anaQvals(mdParse(window.__G9MD)):null;out.title=(typeof mdParse==='function'&&window.__G9MD)?mdParse(window.__G9MD).title:'';
 out.meta=(typeof mdParse==='function'&&window.__G9MD)?mdParse(window.__G9MD).meta:null;
 out.fn=typeof cha2ReportEl==='function'?String(cha2ReportEl).length:0;}catch(e){out.exc=String(e&&e.stack||e)}
 out.errs=window.__errs||[];const pre=document.createElement('pre');pre.id='C2RTT';pre.textContent=JSON.stringify(out);document.body.appendChild(pre);})();</script>"""
    src = open(src_html, encoding='utf-8').read(); assert ANCHOR in src
    h = src.replace(ANCHOR, seed + "<script>window.__G9MD=%s;</script>" % json.dumps(md1, ensure_ascii=False) + ANCHOR, 1).replace('</body>', test + '</body>', 1)
    app = os.path.join(OUT, 'app_%s.html' % tag); open(app, 'w', encoding='utf-8', newline='\n').write(h)
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + os.path.join(OUT, 'prof_' + tag), '--allow-file-access-from-files',
                        '--window-size=1280,900', '--virtual-time-budget=15000', '--dump-dom', 'file:///' + app.replace('\\', '/')], capture_output=True, timeout=300)
    dom = r.stdout.decode('utf-8', 'replace'); open(os.path.join(OUT, 'dom_%s.html' % tag), 'w', encoding='utf-8').write(dom)
    mm = re.search(r'<pre id="C2RTT">(.*?)</pre>', dom, re.S)
    return json.loads(HT.unescape(mm.group(1))) if mm else {'exc': '결과 없음 dom %d B' % len(dom)}


n1 = page(A.new, 'grades', '특허2', 'new_g')
I('B NEW 특허2 + 채점', {k: n1.get(k) for k in ('c2r', 'sec', 'sl', 'cur', 'tg', 'cmp', 'anatext', 'anaprob', 'jsonText', 'sums', 'exc', 'errs')})
T('D-2 NEW — 문항 칸 「특허2」 = cha2ReportEl 세 구간(.c2r 1 · section 3) · 이 문항 열 강조 문2 · 해설 단추 2', n1.get('c2r') == 1 and n1.get('sec') == 3 and n1.get('cur') == '문2 (20)' and n1.get('tg') == 2, n1)
T('D-2 NEW — 점수 표 설문 줄 text-align:left(%s개)' % n1.get('sl'), n1.get('sl', 0) > 0 and n1.get('slLeft'), n1.get('slLeft'))
sums = n1.get('sums') or []
T('D-2 NEW — 격자 특허 칸 요약 줄 = v2 「설(n) 답틀 · 조1판1 누락」 꼴(4칸)', len([x for x in sums if re.match(r'^설\S+ ', x)]) >= 4 and all(re.match(r'^(설\S+ (ok|답틀|(답틀 · )?(조\d+)?(판\d+)?(사\d+)?(\?\d+)? 누락))( \| 설\S+ (ok|답틀|(답틀 · )?(조\d+)?(판\d+)?(사\d+)?(\?\d+)? 누락))*$', x) for x in sums), sums)
T('D-2 NEW — 채점 JSON 이 격자 아래 글 md 로 안 그려짐(.anatext 0 · JSON 글자 0)', n1.get('anatext') == 0 and not n1.get('jsonText'), [n1.get('anatext'), n1.get('jsonText')])
T('G-9 헤드리스 tt mdParse·anaQvals 가 생성 md 를 읽는다 — 문항별 %s' % want, n1.get('qv') == want and (n1.get('meta') or {}).get('예측') == 'true' and (n1.get('meta') or {}).get('사람') == '햄찌' and n1.get('title', '').startswith('63회 2차 · 특허 예측 (햄찌)'), [n1.get('qv'), n1.get('meta'), n1.get('title')])
T('D-2 NEW JS 오류 0', not n1.get('errs') and not n1.get('exc'), [n1.get('errs'), n1.get('exc')])
n2 = page(A.new, 'grades', '민소3', 'new_m')
T('D-2 NEW — 「민소3」 = 세 구간 · 해설 못 찾음 단추 2 · 비교 표 1', n2.get('c2r') == 1 and n2.get('sec') == 3 and n2.get('tg') == 2 and n2.get('cmp') == 1 and not n2.get('errs'), {k: n2.get(k) for k in ('c2r', 'sec', 'tg', 'cmp', 'cur', 'errs', 'exc')})
n3 = page(A.new, None, '특허2', 'new_nog')
T('D-2 NEW — 채점 파일 없으면 종전 화면(.c2r 0 · 예측 md 패널 .anaprob 1)', n3.get('c2r') == 0 and n3.get('anaprob') == 1 and not n3.get('errs'), {k: n3.get(k) for k in ('c2r', 'anaprob', 'errs', 'exc')})
n4 = page(A.new, 'grades', '특허2', 'new_stale', sha_ok=False)
T('D-2(9/17) NEW — 채점 JSON 캐시 sha ≠ index md5(9/16 판이 sha 없이 담은 캐시)면 그 캐시로 안 그림 → 종전 화면(.c2r 0 · .anaprob 1 · JSON 글자 0)', n4.get('c2r') == 0 and n4.get('anaprob') == 1 and n4.get('anatext') == 0 and not n4.get('jsonText') and not n4.get('errs') and not n4.get('exc'), {k: n4.get(k) for k in ('c2r', 'anaprob', 'anatext', 'jsonText', 'errs', 'exc')})
n5 = page(A.new, 'files', '특허2', 'new_files')
T('D-2(9/17) NEW — 9/16 판 index 꼴(files[] kind grade)이 캐시에 남아도 JSON 글자 0 · 채점 안 읽음(.c2r 0 · .anatext 0) · 격자 = 채점 없는 시드', n5.get('c2r') == 0 and n5.get('anatext') == 0 and not n5.get('jsonText') and n5.get('grid') == n3.get('grid') and not n5.get('errs'), {k: n5.get(k) for k in ('c2r', 'anatext', 'jsonText', 'errs', 'exc')})
o3 = page(A.old, None, '특허2', 'old_nog')
o1 = page(A.old, 'grades', '특허2', 'old_g')
T('C 옛 앱(72c5c1d · 새로고침 안 된 기기) + 9/17 index — JSON 글자 0 · .anatext 0 · 격자 칸 글자 = 채점 없는 시드 · 예측 md 패널 1', o1.get('anatext') == 0 and not o1.get('jsonText') and o1.get('grid') == o3.get('grid') and o1.get('anaprob') == 1 and not o1.get('errs'), {k: o1.get(k) for k in ('c2r', 'fn', 'anatext', 'jsonText', 'anaprob', 'errs', 'exc')})
o2 = page(A.old, 'files', '특허2', 'old_files')
T('헛잣대 C — 옛 앱 + 9/16 판 index 꼴(files[] kind grade) = 채점 JSON 이 격자 아래 글 md 로 그려짐(.anatext ≥1 · JSON 글자 · 사용자 신고 재현)', o2.get('c2r') == 0 and o2.get('fn') == 0 and o2.get('anatext', 0) >= 1 and o2.get('jsonText'), {k: o2.get(k) for k in ('c2r', 'fn', 'anatext', 'jsonText', 'errs')})
h1 = page(A.head, 'grades', '특허2', 'head_g')
T('C 9/16 판(d5729f0 · 지금 Pages · 새로고침 전) + 9/17 index — .c2r 0 · JSON 글자 0 · .anatext 0 · 예측 md 패널 1(files[] 에서 채점을 못 찾아 종전 화면)', h1.get('c2r') == 0 and h1.get('anatext') == 0 and not h1.get('jsonText') and h1.get('anaprob') == 1 and not h1.get('errs'), {k: h1.get(k) for k in ('c2r', 'anatext', 'jsonText', 'anaprob', 'errs', 'exc')})
h3 = page(A.head, None, '특허2', 'head_nog')
T('HEAD ↔ NEW 채점 파일 없는 시드 — 격자 칸 글자 같음(종전 화면 무변)', h3.get('grid') == n3.get('grid'), [h3.get('grid'), n3.get('grid')])
T('옛 앱 ↔ NEW 채점 파일 없는 시드 — 격자 칸 글자 같음', o3.get('grid') == n3.get('grid'), [o3.get('grid'), n3.get('grid')])
after = {f: hashlib.md5(open(os.path.join(SPD, '63-2', f), 'rb').read()).hexdigest() for f in sorted(os.listdir(os.path.join(SPD, '63-2')))}
T('G-9 실제 studyplandata exam/analysis/63-2 파일 바이트 무변(하네스 전후)', after == real_md5, [real_md5, after])
for l in R:
    print('   ' + l)
p = sum(1 for l in R if l.startswith('PASS')); f = sum(1 for l in R if l.startswith('FAIL'))
print('\n합계  PASS %d · FAIL %d' % (p, f))
sys.exit(0 if not f else 1)
