# -*- coding: utf-8 -*-
"""tt앱 — 격자 아래 foot 왼쪽 「어제」 합계 한 줄 검산.

sheetHTML() 을 직접 불러 나온 HTML 을 잰다(DOM 렌더 대기 없이 결정적).
쓰기 : python _harness_tt_yday.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import json, os, re, subprocess, sys

SRC = _roots.genie(r"timetable\index.html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_yday")
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ANCHOR = "<script>\n/* ============================================================\n   타임테이블 v1"

PIN = ("<script>(function(){const R=Date;const OFF=new R('2026-09-05T12:00:00+09:00').getTime()-R.now();"
       "function D(...a){return a.length?new R(...a):new R(R.now()+OFF)}D.prototype=R.prototype;"
       "D.now=()=>R.now()+OFF;D.parse=R.parse;D.UTC=R.UTC;window.Date=D;})();</script>")

PERSON = '꼬까'
# 어제(09-04) = 60분 + 90분 + nt 30분(합산 제외) → 150분 = 02:30 · 오늘(09-05) = 45분 = 00:45
SESSIONS = [
    {'id': 'y1', 'd': '2026-09-04', 's': '민법', 'a': 600, 'b': 660, 'u': 1},
    {'id': 'y2', 'd': '2026-09-04', 's': '물리', 'a': 700, 'b': 790, 'u': 1},
    {'id': 'y3', 'd': '2026-09-04', 's': '생활', 'a': 800, 'b': 830, 'nt': 1, 'life': 1, 'u': 1},
    {'id': 't1', 'd': '2026-09-05', 's': '민법', 'a': 540, 'b': 585, 'u': 1},
]

SEED = """<script>
localStorage.clear();
localStorage.setItem('tt.cfg',JSON.stringify({person:%s,token:'',lastSync:0}));
localStorage.setItem('tt.f.sessions/%s/2026-09.json',JSON.stringify({data:{v:1,sessions:%s},sha:null,dirty:false}));
</script>""" % (json.dumps(PERSON, ensure_ascii=False), PERSON, json.dumps(SESSIONS, ensure_ascii=False))

TESTS = r"""<script>
(function(){
const R=[];
const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+((i!==undefined&&!c)?' | '+String(i):''));
try{
 const WHO=__PERSON__, D='2026-09-05';
 const sess=sessionsOf(WHO,D);
 const h=sheetHTML(WHO,D,sess);

 /* Y1 — (2026-09-16 add1 보정 갱신) 어제 줄은 왼쪽 Time Table 기둥 아래(.ydtwo) 이고 foot 에는 없다 */
 const mf=h.match(/<div class="foot">([\s\S]*?)<div>Total/);
 T('Y1 (add1 보정 갱신) 어제 줄 = 왼쪽 기둥 .ydtwo · foot 엔 「어제」 없음',/class="ydtwo"/.test(h)&&!!mf&&mf[1].indexOf('어제')<0,'foot앞='+(mf?mf[1].slice(0,90):'foot 없음'));

 /* Y2 — 값이 맞다. 어제 60+90=150분, nt(생활) 30분은 빠진다 */
 T('Y2 어제 합계 = 02:30 (생활 30분 뺀 값)',h.indexOf('어제 <b>02:30</b>')>=0,
   (h.match(/어제 <b>[^<]*<\/b>/)||['어제 줄 없음'])[0]);

 /* Y3 — 헛잣대: 안 고쳤으면 이 문자열이 아예 없다 (add1 보정으로 이름이 ydtwo 가 됐다) */
 T('Y3 (add1 보정 갱신) ydtwo 클래스가 실제로 나온다',h.indexOf('ydtwo')>=0);

 /* Y4 — Total 무변: 오늘 45분 그대로 */
 T('Y4 Total 은 안 흔들렸다 (오늘 00:45)',h.indexOf('>00:45</span>')>=0,
   (h.match(/class="big"[^>]*>([^<]*)</)||[])[1]);

 /* Y5 — Start/Stop 도 그대로 */
 T('Y5 Start 09:00 · Stop 09:45 그대로',h.indexOf('Start <b>09:00</b>')>=0&&h.indexOf('Stop <b>09:45</b>')>=0,
   (h.match(/Start <b>[^<]*<\/b>[\s\S]{0,30}?Stop <b>[^<]*<\/b>/)||[])[0]);

 /* Y6 — 주/월 축에는 안 붙는다(그 축에서 「어제」는 뜻이 없다) */
 const hw=sheetHTML(WHO,D,sess,{axis:'week'});
 T('Y6 주 축에는 안 붙는다',hw.indexOf('ydtwo')<0);

 /* Y7 — 어제 기록이 없는 사람도 안 죽는다 */
 let ok7=true,e7='';
 try{const h2=sheetHTML(WHO,'2026-09-20',sessionsOf(WHO,'2026-09-20'));ok7=h2.indexOf('어제 <b>00:00</b>')>=0;e7=(h2.match(/어제 <b>[^<]*<\/b>/)||[''])[0];}
 catch(e){ok7=false;e7=e.message}
 T('Y7 기록 없는 날 = 00:00 (안 죽는다)',ok7,e7);

}catch(e){T('하네스가 죽었다',false,e.message+' | '+(e.stack||'').split('\n')[1])}
const pre=document.createElement('pre');pre.textContent=R.join('\n');document.body.appendChild(pre);
})();
</script>"""


def main():
    html = open(SRC, encoding='utf-8').read()
    assert ANCHOR in html, 'seed anchor not found'
    html = html.replace(ANCHOR, PIN + SEED + ANCHOR, 1)
    tests = TESTS.replace('__PERSON__', json.dumps(PERSON, ensure_ascii=False))
    html = html.replace('</body>', tests + '</body>', 1)
    app = os.path.join(OUT, 'app.html')
    open(app, 'w', encoding='utf-8', newline='\n').write(html)

    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--user-data-dir=' + os.path.join(OUT, 'prof'),
                        '--allow-file-access-from-files', '--window-size=1280,900',
                        '--virtual-time-budget=8000', '--dump-dom',
                        'file:///' + app.replace('\\', '/')],
                       capture_output=True, timeout=180)
    dom = r.stdout.decode('utf-8', 'replace')
    open(os.path.join(OUT, 'dom.html'), 'w', encoding='utf-8').write(dom)
    lines = []
    for ln in dom.replace('\r', '').split('\n'):
        s = re.sub(r'^.*?<pre[^>]*>', '', ln)
        s = re.sub(r'</pre>.*$', '', s).strip()
        if s.startswith(('PASS | ', 'FAIL | ')):
            lines.append(s)
    if not lines:
        print('결과 줄 없음 — 부팅 사망? dom %d bytes → %s' % (len(dom), os.path.join(OUT, 'dom.html')))
        return 1
    for ln in lines:
        print('   ' + ln)
    f = sum(1 for ln in lines if ln.startswith('FAIL'))
    print('\n합계  PASS %d · FAIL %d' % (len(lines) - f, f))
    return 0 if f == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
