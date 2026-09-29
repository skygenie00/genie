# -*- coding: utf-8 -*-
"""민법OX 쓰임 수 검산 (_task_ox_use_count.md §6).

실물 연결 = studyplandata 클론 `minbeop/기록.json` 의 `ox_q_reflinks`·`ox_q_links`.
정답지(손 세기)는 **파이썬이 JSON.parse 로 따로 돈다** — 앱의 useOwners 를 안 쓴다(G1 단서).

쓰기 : python _harness_use_count.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib, io, json, os, random, re, subprocess, sys

SRC = _roots.genie(r"minbeop\index.html")
REC = _roots.spd(r"minbeop\기록.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_use")
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

KINDS = ('geunge', 'memo', 'logic', 'links')


def hand_index(reflinks, links):
    """손 세기 — 역방향 표를 앱과 무관하게 따로 만든다."""
    idx = {k: {} for k in KINDS}
    for owner in sorted(reflinks):
        r = reflinks[owner] or {}
        for k in ('geunge', 'memo', 'logic'):
            for t in (r.get(k) or []):
                t = str(t).strip()
                if t:
                    idx[k].setdefault(t, []).append(owner)
    for owner in sorted(links):
        for t in (links[owner] or []):
            t = str(t).strip()
            if t:
                idx['links'].setdefault(t, []).append(owner)
    return idx


def main():
    rec = json.load(io.open(REC, encoding='utf-8'))
    data = rec.get('data') or rec
    reflinks = data.get('ox_q_reflinks') or {}
    links = data.get('ox_q_links') or {}
    hand = hand_index(reflinks, links)

    # ── G3 분포 (보고용 · 문턱 5 고정)
    dist = {}
    for k in KINDS:
        c1 = sum(1 for t in hand[k] if len(hand[k][t]) == 1)
        c24 = sum(1 for t in hand[k] if 2 <= len(hand[k][t]) <= 4)
        c5 = sum(1 for t in hand[k] if len(hand[k][t]) >= 5)
        dist[k] = (c1, c24, c5, len(hand[k]))

    # ── G1 표본 20개 (고정 시드 · sorted 로 순회를 못박는다)
    pool = sorted((k, t) for k in KINDS for t in hand[k])
    rnd = random.Random(20260914)
    sample = rnd.sample(pool, min(20, len(pool)))
    want = {'%s|%s' % (k, t): len(hand[k][t]) for k, t in sample}

    # ── G2 표본 — 쓰임 1 / 2 / 4 / 5+ 인 실물 대상
    def pick(n_lo, n_hi):
        for k, t in pool:
            n = len(hand[k][t])
            if n_lo <= n <= n_hi:
                return [k, t, n]
        return None
    g2 = {'n1': pick(1, 1), 'n2': pick(2, 2), 'n4': pick(4, 4), 'n5': pick(5, 10 ** 6)}

    # ── quizData 더미. G4 표본 대상의 owners 는 **반드시 넣고**, 그중 마지막 하나만
    #    일부러 뺀다 — 「지금 보는 문항」(노랑)과 「데이터에 없음」(회색)을 한 창에서 같이 잰다.
    uids = sorted({t for k in KINDS for t in hand[k]} | {o for k in KINDS for t in hand[k] for o in hand[k][t]})
    tgt = g2['n5'] or g2['n4'] or g2['n2'] or g2['n1']
    owners_t = hand[tgt[0]][tgt[1]] if tgt else []
    drop = owners_t[-1] if len(owners_t) >= 2 else None
    me = owners_t[0] if owners_t else None
    keep = [u for u in uids if u != drop]
    missing = drop
    quiz = [{'id': u, 'q': '더미 지문 ' + u + ' 가나다라마바사아자차카타파하' * 3,
             'subject': '민법총칙', 'subChapter': '2.1 권리능력'} for u in keep]

    seed = ('<script>'
            + 'window.__ERR=[];window.addEventListener("error",function(e){__ERR.push(String(e.message)+" @"+(e.filename||"")+":"+e.lineno)});'
            + 'window.addEventListener("unhandledrejection",function(e){__ERR.push("reject "+String(e.reason&&e.reason.message||e.reason))});'
            + 'localStorage.clear();'
            + "localStorage.setItem('ox_q_reflinks',%s);" % json.dumps(json.dumps(reflinks, ensure_ascii=False))
            + "localStorage.setItem('ox_q_links',%s);" % json.dumps(json.dumps(links, ensure_ascii=False))
            + '</script>')

    tests = TESTS.replace('__WANT__', json.dumps(want, ensure_ascii=False)) \
                 .replace('__G2__', json.dumps(g2, ensure_ascii=False)) \
                 .replace('__QUIZ__', json.dumps(quiz, ensure_ascii=False)) \
                 .replace('__MISSING__', json.dumps(missing, ensure_ascii=False))\
                 .replace('__ME__', json.dumps(me, ensure_ascii=False)) \
                 .replace('__TGT__', json.dumps(tgt, ensure_ascii=False))

    html = io.open(SRC, encoding='utf-8', newline='').read()
    anchor = '    <script>\n'
    i = html.index(anchor, html.index('</head>') if '</head>' in html else 0) if anchor in html else -1
    assert '</body>' in html, 'no </body>'
    # 시드는 앱 스크립트 앞(첫 인라인 <script> 앞)에
    k = html.index('<script>', html.index('<body'))
    html = html[:k] + seed + html[k:]
    # ⚠ </body> 가 둘이다 — 첫 것은 SheetJS 안의 **문자열**이라
    #   거기 박히면 스크립트가 아예 안 돌았다(9/14 실측). 마지막 것에 붙인다.
    b = html.rindex('</body>')
    html = html[:b] + tests + html[b:]
    app = os.path.join(OUT, 'app.html')
    io.open(app, 'w', encoding='utf-8', newline='\n').write(html)

    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--user-data-dir=' + os.path.join(OUT, 'prof'),
                        '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=12000', '--dump-dom',
                        'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=180)
    dom = r.stdout.decode('utf-8', 'replace')
    err = r.stderr.decode('utf-8', 'replace')
    io.open(os.path.join(OUT, 'stderr.txt'), 'w', encoding='utf-8').write(err)
    io.open(os.path.join(OUT, 'dom.html'), 'w', encoding='utf-8').write(dom)
    lines = []
    for ln in dom.replace('\r', '').split('\n'):
        s = re.sub(r'^.*?<pre[^>]*>', '', ln)
        s = re.sub(r'</pre>.*$', '', s).strip()
        if s.startswith(('PASS | ', 'FAIL | ', 'INFO | ')):
            lines.append(s)

    # ── G5 무접촉 : git 원본(HEAD)과 블록 단위 문자 대조
    print('=== G5 무접촉 — git HEAD 원본과 블록 대조 ===')
    import subprocess as _sp
    base = _sp.run(['git', 'show', 'HEAD:minbeop/index.html'],
                   cwd=_roots.genie(),
                   capture_output=True).stdout.decode('utf-8', 'replace')
    cur = io.open(SRC, encoding='utf-8', newline='').read()

    def block(text, head):
        i = text.index(head)
        j = text.index('{', i)
        d, k, instr, esc = 0, j, None, False
        while k < len(text):
            c = text[k]
            if instr:
                if esc: esc = False
                elif c == '\\': esc = True
                elif c == instr: instr = None
            elif c in '"\'`': instr = c
            elif c == '{': d += 1
            elif c == '}':
                d -= 1
                if d == 0: return text[i:k + 1]
            k += 1
        raise AssertionError('unbalanced ' + head)

    n_bad = 0
    for nm in ('function ggAdd(', 'function ggToggle(', 'function refBoxHTML(', 'function refPut('):
        b0, b1 = block(base, nm), block(cur, nm)
        if nm == 'function refPut(':
            # 색인 무효화 한 줄만 붙었는지 — 그 줄을 걷어내면 문자까지 같아야 한다
            b1x = b1.replace("            useIdxDrop();                          /* 쓰임 색인 — 저장 로직은 위 그대로다 */\n", '')
            ok = (b0 == b1x)
            print('  %-22s %s  (붙은 것 = useIdxDrop() 한 줄뿐인가)' % (nm.strip('function ('), 'PASS' if ok else 'FAIL'))
        else:
            ok = (b0 == b1)
            print('  %-22s %s  %d자' % (nm.strip('function ('), 'PASS 문자까지 같다' if ok else 'FAIL 달라졌다', len(b1)))
        if not ok: n_bad += 1
    print('  G5 블록 : %s' % ('ALL OK' if not n_bad else '%d개 어긋남' % n_bad))
    print()

    print('=== G3 분포 (실측 · 문턱 5 고정 · 보고용) ==='),
    print('  %-8s %8s %8s %8s %8s' % ('갈래', '1', '2~4', '5이상', '대상수'))
    for k in KINDS:
        c1, c24, c5, tot = dist[k]
        print('  %-8s %8d %8d %8d %8d' % (k, c1, c24, c5, tot))
    print('  (대상수 = 그 갈래에서 「걸린 쪽」으로 한 번이라도 나온 UID 수)')
    print()
    if not lines:
        print('결과 줄 없음 — dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom.html')))
        for ln in [x for x in err.split('\n') if x.strip()][:12]:
            print('   stderr| ' + ln.strip())
        return 1
    for ln in lines:
        print('   ' + ln)
    f = sum(1 for ln in lines if ln.startswith('FAIL'))
    p = sum(1 for ln in lines if ln.startswith('PASS'))
    print('\n합계  PASS %d · FAIL %d' % (p, f))
    return 0 if f == 0 else 1


TESTS = r"""<script>
/* ⚠ 앱이 부팅하며 body 를 갈아치운다 — 결과는 documentElement 에 붙이고, 검사는 부팅 뒤로 늦춘다 */
setTimeout(function(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i):''));
const say=s=>R.push('INFO | '+s);
say('부팅 오류 '+((window.__ERR||[]).length)+'건 : '+((window.__ERR||[]).slice(0,3).join(' / ')||'없음'));
say('전역 확인 : useCount='+(typeof useCount)+' useWin='+(typeof useWin)+' quizData='+(typeof quizData)+' SYNC_KEYS='+(typeof SYNC_KEYS));
try{
 const WANT=__WANT__, G2=__G2__, MISSING=__MISSING__, ME=__ME__, TGT=__TGT__;
 quizData.length=0; __QUIZ__.forEach(q=>quizData.push(q));
 useIdxDrop();

 /* G1 — 색인 값 vs 손 세기 20개 */
 let bad=[];
 for(const key in WANT){
  const p=key.split('|'), got=useCount(p[0],p[1]);
  if(got!==WANT[key])bad.push(key+' 앱'+got+'≠손'+WANT[key]);
 }
 T('G1 색인 20/20 일치',bad.length===0,bad.slice(0,4).join(' · '));
 say('G1 표본 '+Object.keys(WANT).length+'개 · 어긋남 '+bad.length);

 /* G2 — 표시 규칙 */
 const html1=G2.n1?useNumHTML(G2.n1[0],G2.n1[1],''):'(없음)';
 T('G2 쓰임 1 = 아무것도 안 그린다',!G2.n1||html1==='',G2.n1+' → '+html1.slice(0,60));
 const chk=(t,expCol)=>{
  if(!t)return null;
  const h=useNumHTML(t[0],t[1],'');
  return {h:h,okCol:h.indexOf(expCol)>=0,noPill:h.indexOf('border')<0&&h.indexOf('background')<0&&h.indexOf('rounded')<0,
          num:(h.match(/>(\d+)<\/i>/)||[])[1]};
 };
 const c2=chk(G2.n2,'#94a3b8'),c4=chk(G2.n4,'#94a3b8'),c5=chk(G2.n5,'#dc2626');
 T('G2 쓰임 2 = 회색 #94a3b8',!c2||c2.okCol,c2&&c2.h.slice(0,90));
 T('G2 쓰임 4 = 회색 #94a3b8',!c4||c4.okCol,c4&&c4.h.slice(0,90));
 T('G2 쓰임 5이상 = 빨강 #dc2626',!c5||c5.okCol,c5&&c5.h.slice(0,90));
 T('G2 알약·테두리·배경 없음(숫자 글자만)',[c2,c4,c5].every(x=>!x||x.noPill),
   [c2,c4,c5].filter(x=>x&&!x.noPill).map(x=>x.h.slice(0,70)).join(' | '));
 T('G2 글자 크기·굵기 규격',[c2,c4,c5].every(x=>!x||(x.h.indexOf('font-size:10.5px')>=0&&x.h.indexOf('font-weight:900')>=0)));
 /* ⚠ 실물에 쓰임 5 이상이 한 건도 없다(G3 분포) — 위 빨강 검사는 표본이 없으면 헛PASS 다.
    색 규칙 자체는 **인공 색인**으로 정직하게 잰다. 문턱 5 는 고정이므로 규칙만 확인하면 된다. */
 const savedIdx=USE_IDX;
 USE_IDX={geunge:{},memo:{},logic:{},links:{ZZTEST5:['A','B','C','D','E'],ZZTEST4:['A','B','C','D']}};
 const a5=useNumHTML('links','ZZTEST5',''), a4=useNumHTML('links','ZZTEST4','');
 T('G2 [인공] 5 = 빨강 #dc2626',a5.indexOf('#dc2626')>=0&&a5.indexOf('>5</i>')>=0,a5.slice(0,90));
 T('G2 [인공] 4 = 회색 #94a3b8',a4.indexOf('#94a3b8')>=0&&a4.indexOf('>4</i>')>=0,a4.slice(0,90));
 T('G2 [인공] 문턱이 5 다(4 는 빨강이 아니다)',a4.indexOf('#dc2626')<0);
 USE_IDX=savedIdx;
 say('G2 표본 : 1='+JSON.stringify(G2.n1)+' 2='+JSON.stringify(G2.n2)+' 4='+JSON.stringify(G2.n4)+' 5+='+JSON.stringify(G2.n5));

 /* G4 — 창 */
 const tgt=TGT;
 if(tgt){
  const owners=useOwners(tgt[0],tgt[1]);
  const me=ME;                                  /* 파이썬이 고른 것 — quizData 안에 있는 owner */
  useWin(tgt[0],tgt[1],me);
  const win=document.getElementById('oxwin-use-'+tgt[0]+'-'+tgt[1]);
  T('G4-④ 창이 열린다(key = use-갈래-대상)',!!win);
  const body=win?win.querySelector('.oxwin-body').innerHTML:'';
  T('G4-① 대상 머리 칸에 그 대상 UID',body.indexOf(tgt[1])>=0);
  T('G4-② 「지금 보는 문항」 배지 + 연결 끊기',body.indexOf('지금 보는 문항')>=0&&body.indexOf('연결 끊기')>=0,
    'me='+me+' owners='+owners.length);
  T('G4-② 그 줄이 노랑 바탕',body.indexOf('#fefce8')>=0);
  /* 없는 UID 회색 줄 — 표본에 없으면 일부러 만든다 */
  const gone=owners.find(o=>!quizData.some(q=>q.id===o));
  T('G4-③ 데이터에 없는 UID = 회색 줄',!gone||body.indexOf('지금 데이터에 없음')>=0,'gone='+gone);
  useWin(tgt[0],tgt[1],me);
  T('G4-④ 같은 갈래·대상이면 창이 하나',document.querySelectorAll('#oxwin-use-'+tgt[0]+'-'+tgt[1]).length===1);
  say('G4 대상 '+JSON.stringify(tgt)+' · owners '+owners.length+' · me '+me);
 } else { T('G4 쓸 대상이 없다',false); }

 /* G5 — 무접촉 : SYNC_KEYS 17 · 새 localStorage 키 0 */
 T('G5 SYNC_KEYS 17 그대로',SYNC_KEYS.length===17,SYNC_KEYS.length);
 const keys=Object.keys(localStorage).sort();
 const extra=keys.filter(k=>k.indexOf('use')===0||k.indexOf('USE')===0);
 T('G5 새 localStorage 키 0개',extra.length===0,extra.join(','));
 say('G5 localStorage 키 '+keys.length+'개 : '+keys.join(','));

}catch(e){T('하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n')[1])}
const pre=document.createElement('pre');pre.textContent=R.join('\n');
document.documentElement.appendChild(pre);
},2500);
</script>"""

if __name__ == '__main__':
    sys.exit(main())
