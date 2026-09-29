# -*- coding: utf-8 -*-
"""tt 작은 창(PiP) 삭제 — 헤드리스 검산
(2026-09-20 · timetable/_task_tt_pip_delete.md §B)

  D  본창 세션 모달 — 한 번 = 「정말 삭제?」 · 두 번 = 지움 · 3초 뒤 되돌림
  P  흉내 PiP 문서 — 같은 두 번 누름 · `window.confirm` 호출 0회(스파이) · pipPaint 뒤따름
  L  생활 블록 모달 같은 결과 · 프리셋 삭제는 `doc.defaultView.confirm`
  K  저장·취소 무변
  S  원본 대조(파이썬) · 헛잣대(HEAD 에서 FAIL)

    PYTHONIOENCODING=utf-8 python _harness_tt_pip_delete.py
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import hashlib
import http.server
import io
import os
import shutil
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse

GENIE = _roots.genie()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(GENIE, 'timetable', 'index.html')
BASE = os.path.join(HERE, '_tt_before.html')
OUT = os.path.join(os.environ.get('TEMP', '.'), 'httdel')
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

STUB = """<script>
window.__err=[];
window.addEventListener('error',e=>{window.__err.push((e.message||'')+' @'+e.lineno)});
window.addEventListener('unhandledrejection',e=>{window.__err.push('reject: '+((e.reason&&e.reason.message)||e.reason))});
/* ⚠ 헤드리스에서 confirm 은 **그대로 멈춰 선다**(2026-09-20 실측 — 헛잣대가 시간 초과로 끝났다).
   그 멈춤 자체가 이 결함의 증거지만, 잣대를 끝까지 돌리려면 스텁이 있어야 한다.
   고친 판은 이 갈래를 아예 안 타므로 스텁이 있어도 재는 것이 달라지지 않는다. */
window.confirm=function(){return true};
/* 진짜 網을 막는다 — 이 하네스는 화면만 잰다 */
window.fetch=async function(u,o){return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)}};
</script>
"""

PROBE = r"""<script>
(function(){
 const R=[];const T=(n,c,i)=>R.push((c?'PASS':'FAIL')+' | '+n+(c?'':' | '+JSON.stringify(i===undefined?null:i)));
 const N=(n,i)=>R.push('NOTE | '+n+' | '+JSON.stringify(i===undefined?null:i));
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const grp=async(n,f)=>{try{await f()}catch(e){T(n+' 묶음 예외',false,String(e&&e.stack||e).slice(0,300))}};
 const txt=el=>(el?String(el.textContent||'').replace(/\s+/g,' ').trim():'');
 async function run(){
  const out={lines:R};
  try{
   /* ── 밑준비: 사람·세션 하나를 메모리에 세운다(저장소는 안 건드린다) ── */
   const D=(typeof today==='function')?today():null;
   T('0 앱이 떴다',typeof modal==='function'&&typeof deleteSession==='function'&&!!D,
     [typeof modal,typeof deleteSession,D]);
   const mk=()=>{const s={id:'H'+Math.random().toString(36).slice(2,8),d:D,a:15*60+37,b:15*60+38,
      s:'기타',p:'지학 기본강의 1.2',i:'',u:Date.now()};
     upsertSession(s);return s};
   /* ── D. 본창 ── */
   await grp('D', async()=>{
     const s=mk(); await wait(60);
     editSession(s.id); await wait(200);
     const m=[...document.querySelectorAll('.modal')].pop();
     T('D-1 세션 모달이 떴다',!!m&&!!m.querySelector('#mDel'));
     const db=m.querySelector('#mDel');
     T('D-1 단추 글자가 「삭제」',txt(db)==='삭제',txt(db));
     db.click(); await wait(120);
     T('D-2 ★한 번 누르면 안 지워지고 글자가 「정말 삭제?」',
       txt(db)==='정말 삭제?'&&db.classList.contains('arm')&&!!findSess(s.id)&&!findSess(s.id).del,
       [txt(db),!!findSess(s.id)]);
     T('D-2 무엇을 지우는지 한 줄이 보인다',!!m.querySelector('.delnote')
       &&txt(m.querySelector('.delnote')).indexOf('세션')>=0,txt(m.querySelector('.delnote')));
     db.click(); await wait(250);
     T('D-3 ★두 번째 누름에 지워진다(del:true)',!!findSess(s.id)&&findSess(s.id).del===true,
       findSess(s.id)?findSess(s.id).del:'(없음)');
     T('D-3 모달이 닫힌다',[...document.querySelectorAll('.modal')].length===0);
     /* 3초 뒤에는 첫 누름으로 되돌아간다 */
     const s2=mk(); await wait(60);
     editSession(s2.id); await wait(200);
     const m2=[...document.querySelectorAll('.modal')].pop(), d2=m2.querySelector('#mDel');
     d2.click(); await wait(3200);
     T('D-4 ★3초가 지나면 「삭제」로 되돌아간다',txt(d2)==='삭제'&&!d2.classList.contains('arm'),txt(d2));
     T('D-4 그 사이 안 지워졌다',!findSess(s2.id).del);
     T('D-4 안내 줄도 걷힌다',!m2.querySelector('.delnote'));
     d2.click(); await wait(120); d2.click(); await wait(250);
     T('D-4 다시 두 번 누르면 지워진다',findSess(s2.id).del===true);
   });
   /* ── P. 흉내 PiP 문서 ── */
   await grp('P', async()=>{
     const ifr=document.createElement('iframe');ifr.style.cssText='position:fixed;left:-9999px;width:400px;height:300px';
     document.body.appendChild(ifr);
     const doc=ifr.contentDocument;
     doc.body.innerHTML='';
     let mainConfirm=0, pipConfirm=0;
     const _mc=window.confirm; window.confirm=function(){mainConfirm++;return true};
     ifr.contentWindow.confirm=function(){pipConfirm++;return true};
     let paint=0; const _pp=window.pipPaint; window.pipPaint=function(){paint++;if(_pp)try{return _pp.apply(this,arguments)}catch(e){}};
     const s=mk(); await wait(60);
     editSession(s.id,doc); await wait(220);
     const m=[...doc.querySelectorAll('.modal')].pop();
     T('P-1 모달이 **그 문서**에 그려진다',!!m&&m.ownerDocument===doc);
     const db=m.querySelector('#mDel');
     db.click(); await wait(120);
     T('P-2 한 번 = 「정말 삭제?」',txt(db)==='정말 삭제?'&&!findSess(s.id).del,txt(db));
     db.click(); await wait(250);
     T('P-3 ★두 번 = 지워진다',findSess(s.id).del===true);
     T('P-3 ★본창 window.confirm 호출 0회',mainConfirm===0,mainConfirm);
     T('P-3 ★작은 창 confirm 도 0회(두 번 누름이라 아예 안 부른다)',pipConfirm===0,pipConfirm);
     T('P-4 pipPaint 가 뒤따라 불린다',paint>=1,paint);
     window.confirm=_mc; window.pipPaint=_pp; ifr.remove();
   });
   /* ── L. 생활 블록 · 프리셋 ── */
   await grp('L', async()=>{
     const s={id:'L'+Math.random().toString(36).slice(2,8),d:D,a:9*60,b:9*60+30,life:1,p:'식사',u:Date.now()};
     upsertSession(s); await wait(60);
     const ifr=document.createElement('iframe');ifr.style.cssText='position:fixed;left:-9999px;width:400px;height:300px';
     document.body.appendChild(ifr); const doc=ifr.contentDocument; doc.body.innerHTML='';
     let mainConfirm=0, pipConfirm=0;
     const _mc=window.confirm; window.confirm=function(){mainConfirm++;return true};
     ifr.contentWindow.confirm=function(){pipConfirm++;return true};
     lifeModal(s,doc); await wait(220);
     const m=[...doc.querySelectorAll('.modal')].pop();
     T('L-1 생활 블록 모달이 그 문서에 떴다',!!m&&!!m.querySelector('#mDel'));
     const db=m.querySelector('#mDel');
     db.click(); await wait(120);
     T('L-1 한 번 = 「정말 삭제?」',txt(db)==='정말 삭제?'&&!findSess(s.id).del);
     db.click(); await wait(250);
     T('L-1 ★두 번 = 지워지고 본창 confirm 0회',findSess(s.id).del===true&&mainConfirm===0,
       [findSess(s.id).del,mainConfirm]);
     /* 프리셋 삭제 = 그 창의 confirm */
     settings.lifeTypes=(settings.lifeTypes||[]).concat(['하네스프리셋']);
     lifeDelType(encodeURIComponent('하네스프리셋'),doc); await wait(150);
     T('L-2 ★프리셋 삭제는 **그 창**의 confirm 을 부른다',pipConfirm===1&&mainConfirm===0,[pipConfirm,mainConfirm]);
     T('L-2 프리셋이 지워졌다',(settings.lifeTypes||[]).indexOf('하네스프리셋')<0);
     window.confirm=_mc; ifr.remove();
   });
   /* ── K. 저장·취소 무변 ── */
   await grp('K', async()=>{
     const s=mk(); await wait(60);
     editSession(s.id); await wait(200);
     let m=[...document.querySelectorAll('.modal')].pop();
     m.querySelector('#mNo').click(); await wait(150);
     T('K-1 취소는 그대로 닫는다',[...document.querySelectorAll('.modal')].length===0&&!findSess(s.id).del);
     editSession(s.id); await wait(200);
     m=[...document.querySelectorAll('.modal')].pop();
     const a=m.querySelector('#eA2'), b=m.querySelector('#eB2');
     T('K-2 시간 칸이 있다',!!a&&!!b,[!!a,!!b]);
     if(a&&b){a.value=sessDT(s.d,16*60);b.value=sessDT(s.d,16*60+30);}   /* datetime-local — 앱의 sessDT 로 */
     m.querySelector('#mOk').click(); await wait(250);
     T('K-2 저장이 그대로 먹는다',!!findSess(s.id)&&findSess(s.id).a===16*60&&findSess(s.id).b===16*60+30,
       findSess(s.id)?[findSess(s.id).a,findSess(s.id).b]:null);
     findSess(s.id).del=true;
   });
   T('콘솔 오류 0',(window.__err||[]).length===0,window.__err);
  }catch(e){T('예외',false,String(e&&e.stack||e))}
  try{await (window.__nf||((u,o)=>Promise.resolve()))('/result',{method:'POST',body:R.join(String.fromCharCode(10))})}catch(e){}
 }
 window.__nf=fetch.bind(window);
 if(document.readyState==='complete')setTimeout(run,900);else window.addEventListener('load',()=>setTimeout(run,900));
})();
</script>"""


def build(src_text):
    html = src_text
    # 網 차단 스텁을 맨 앞 script 앞에 · 결과를 보내는 길은 남긴다
    html = html.replace('<body', STUB + '<body', 1)
    html = html.replace('</body>', PROBE + '</body>', 1)
    # 하네스가 결과를 보낼 때 쓸 진짜 fetch
    html = html.replace("window.fetch=async function(u,o){",
                        "window.__realFetch=window.fetch.bind(window);\nwindow.fetch=async function(u,o){"
                        "if(String(u).indexOf('/result')===0)return window.__realFetch(u,o);", 1)
    io.open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(html)


def run(src_text, secs=300):
    build(src_text)
    done = threading.Event(); box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            box['txt'] = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers(); done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof'); shutil.rmtree(prof, ignore_errors=True)
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1400,950',
                          'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs)
    p.terminate()
    try: p.wait(8)
    except Exception: p.kill()
    srv.shutdown()
    if not got:
        return ['FAIL | 시간 안에 안 끝났다']
    return [x for x in box['txt'].replace('\r', '').split('\n') if x.strip()]


def static_checks():
    b = io.open(SRC, 'rb').read()
    s = b.replace(b'\r\n', b'\n').decode('utf-8')
    base = io.open(BASE, 'rb').read().replace(b'\r\n', b'\n').decode('utf-8')
    out = []

    def T2(n, c, i=''):
        out.append(('PASS' if c else 'FAIL') + ' | ' + n + ('' if c else ' | ' + str(i)))

    T2('S-1 modal 의 「삭제」가 두 번 누름이다', "db.textContent='정말 삭제?'" in s and "if(armed){disarm();onDel();close();after();return}" in s)
    T2('S-2 onDel 에서 confirm 을 뗐다 — 다섯 자리',
       s.count('confirm(') == base.count('confirm(') - 5, [s.count('confirm('), base.count('confirm(')])
    T2('S-2 세션·생활 블록 손잡이에 confirm 이 없다',
       "()=>{deleteSession(s);render()},doc,undefined,'이 세션을 지웁니다.'" in s
       and "()=>{deleteSession(s);render()},doc,undefined,'이 생활 블록을 지웁니다.'" in s)
    T2('S-3 lifeDelType 은 그 창의 confirm 을 부른다',
       "if(!((doc&&doc.defaultView)||window).confirm(`프리셋" in s)
    T2('S-4 이미 고쳐져 있던 세 자리는 무접촉',
       s.count("((doc&&doc.defaultView)||window).confirm") == base.count("((doc&&doc.defaultView)||window).confirm") + 1,
       [s.count("((doc&&doc.defaultView)||window).confirm"), base.count("((doc&&doc.defaultView)||window).confirm")])
    T2('S-5 delNote 는 여섯째 선택 인자다(안 주면 종전대로)',
       'function modal(body,onOk,onDel,doc,okLabel,delNote){' in s)
    bb = io.open(BASE, 'rb').read()
    T2('S-6 줄끕이 원본과 같다(이 파일은 LF 다 — jagwa 와 다르다)',
       b.count(b'\r\n') == bb.count(b'\r\n') == 0, [b.count(b'\r\n'), bb.count(b'\r\n')])
    T2('S-7 지운 본판 줄이 손댄 자리뿐이다',
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s) <= 8,
       sum(1 for ln in base.split('\n') if ln.strip() and ln not in s))
    sw = io.open(os.path.join(GENIE, 'timetable', 'sw.js'), encoding='utf-8', newline='').read()
    T2('S-8 서비스워커 판을 올렸다(tt-v30)', "const V='tt-v30';" in sw)
    return out


def main():
    want = sys.argv[1:] or ['new', 'null']
    lines = []
    if 'new' in want:
        print('[new]'); lines += run(io.open(SRC, encoding='utf-8', newline='').read())
        lines += static_checks()
    if 'null' in want:
        print('[null · 헛잣대]')
        ls0 = run(io.open(BASE, encoding='utf-8', newline='').read())
        fails = [x for x in ls0 if x.startswith('FAIL')]
        for pre, ko in (('D', '본창'), ('P', '흉내 PiP'), ('L', '생활 블록')):
            hit = [x for x in fails if x.split(' | ')[1].startswith(pre + '-')
                   or x.split(' | ')[1].startswith(pre + ' 묶음')]
            lines.append(('PASS' if hit else 'FAIL') + ' | 0-헛잣대 HEAD 에서 %s 묶음이 FAIL 한다' % ko
                         + ('' if hit else ' | ' + str([x.split(' | ')[1][:60] for x in fails][:6])))
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    for x in lines: print(x)
    print('\n== tt 작은 창 삭제 %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
