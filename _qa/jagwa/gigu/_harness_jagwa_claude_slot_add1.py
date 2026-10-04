# -*- coding: utf-8 -*-
"""자과앱 카드 층 아랫줄 = 물리 꼴 + 「Claude」 — 헤드리스 검산 (묶음 CL2)
(2026-09-22 · gigu/_task_jagwa_claude_slot_add1.md §B)

  CL2-1  아랫줄 여섯의 차례 · 맨 오른쪽이 #tGpt · 글자 「Claude」
  CL2-2  꼴 — 여섯의 계산 스타일이 물리 #pRow1 의 같은 단추와 같다 (+380px 에서 「+회독」 한 줄)
  CL2-3  동작 — 창 · ✓ 따라오기 · 지우기 · 아랫줄 다섯 동작 회귀
  CL2-4  창 머리 둘째 줄에 undefined·빈 「 · 」 0
  CL2-5  목록 줄 보라 「Claude」 태그 (곁가지 표시는 안 살아난다 · 서랍 무변)
  CL2-6  물리 무변 — DOM 글자 · #pRow1 계산 꼴 · 목록 줄 전수가 바탕과 같다
  CL2-0  헛잣대 — 바탕 판에서 1·2·5 가 하나도 안 통과한다

⚠ 픽셀 게이트는 안 쓴다(CLAUDE.md). 계산 스타일·DOM 개수·글자·getClientRects 로만 잰다.
⚠ 과목 사이·바탕 사이 대조는 **같은 잣대를 두 판에 돌려 파이썬에서 맞댄다**(값을 박지 않는다).

    PYTHONIOENCODING=utf-8 python _harness_jagwa_claude_slot_add1.py
"""
import hashlib
import http.server
import io
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import threading
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _harness_earth_shell as E

GENIE = E.GENIE
SRC = E.SRC
CHROME = E.CHROME
SPDROOT = E.SPDROOT
MOTDIR = os.path.join(GENIE, 'jagwa', 'motion')
OUT = os.path.join(os.environ.get('TEMP', '.'), 'hclaudeadd1')
os.makedirs(OUT, exist_ok=True)

BASE_MD5 = '457fdf6728f9fdd2838340356903387a'      # 고침 전 = 본판을 민 판(genie f810502)
ROW = ['tLayer', 'tLayerAdd', 'tLayerEye', 'tHist', 'tCard', 'tGpt']


def md5lf(b):
    return hashlib.md5(b.replace(b'\r\n', b'\n')).hexdigest()


def base_text():
    keep = os.path.join(os.environ.get('TEMP', '.'), 'jagwa_base_claude_add1.html')
    if os.path.exists(keep):
        b = open(keep, 'rb').read()
        if md5lf(b) == BASE_MD5:
            return b.replace(b'\r\n', b'\n').decode('utf-8')
    for rev in ('f810502', 'HEAD', 'HEAD~1'):
        b = subprocess.run(['git', '-C', GENIE, 'show', rev + ':jagwa/index.html'],
                           capture_output=True).stdout
        if b and md5lf(b) == BASE_MD5:
            open(keep, 'wb').write(b.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
            return b.replace(b'\r\n', b'\n').decode('utf-8')
    raise SystemExit('NG  바탕 판(md5 %s)을 못 찾았다' % BASE_MD5)


# ══════════════════════════════════════════════════════════════════════════
BODY_CL2 = r"""
   await wait(1500);
   const ROW=__ROW__;
   const CARD=(typeof HASBOOK!=='undefined')&&HASBOOK;
   /* ⚠ **원격 기록 동기화가 끝난 뒤에** 잰다. 안 그러면 회독 수가 판마다 갈려
      「물리 무변」이 거짓으로 깨진다(2026-09-22 실측 — 새 판 「2회독」 vs 바탕 「기록」,
       둘 다 같은 `phys/기록.json` 인데 한쪽이 동기화 전에 쟀다).
      끝난 표 = `<과목>_sync_meta.lastSync`(4354 에서 찍는다).
      ⚠ 부팅 때 도는 `syncRecords()`(4432)는 **토큰이 아직 없어** 4329 에서 그냥 돌아간다
        (하네스는 `tt.cfg` 를 그 뒤에 넣는다). 다음 기회는 180초 타이머뿐이라
        판이 3분을 넘겼는지에 따라 회독 수가 갈렸다 — 그래서 **직접 부른다.** */
   if(typeof syncRecords==='function'){
     try{await syncRecords(true)}catch(e){N('CL2 동기화 예외',String(e&&e.message||e))}
   }
   const SYNCED=await until(()=>{try{
     return (JSON.parse(localStorage.getItem(CUR.SYNC_PREFIX+'meta')||'{}').lastSync||0)>0
   }catch(e){return false}},40000);
   N('CL2 밑준비 동기화',{끝났나:SYNCED,ST:Object.keys(ST||{}).length,
     회독1:(typeof reps==='function'&&DATA[0])?reps(DATA[0][F.NO]):null});
   await wait(700);
   if(CARD&&typeof loadEarthData==='function'){try{await loadEarthData()}catch(e){}}
   FL.past='';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';FL.lv='';FL.star=false;FL.year='';
   draw(); await wait(700);
   const NO=(DATA[0]||[])[F.NO], NO2=(DATA[1]||[])[F.NO];
   N('CL2 밑준비',{subj:SUBJ_ID,DATA:DATA.length,NO:NO,NO2:NO2,CARD:CARD,
     DB:(typeof CUR==='object'?CUR.DB:null),REC:(typeof REC_PATH!=='undefined'?REC_PATH:null)});
   const killSheets=()=>{$$$('body>.sheet').forEach(x=>x.remove())};
   const sheetNow=()=>document.getElementById('sh-gpt')||$$$('body>.sheet').pop()||null;
   const vis=el=>!!el&&el.offsetParent!==null;
   /* 아랫줄 — 물리는 #pRow1, 카드 층은 .vbot .tools 가 살아 있는 줄이다 */
   const rowBox=()=>document.querySelector(CARD?'.vbot .tools':'#pRow1');
   const SKEYS=['fontSize','fontWeight','color','borderTopWidth','borderTopStyle','backgroundColor',
                'paddingTop','paddingBottom','paddingLeft','paddingRight','whiteSpace','display',
                'borderRadius','width','height','appearance'];
   const styleOf=el=>{if(!el)return null;const c=getComputedStyle(el);const o={};
     SKEYS.forEach(k=>o[k]=String(c[k]));return o};

   /* ══════════ CL2-1 차례 · 글자 ══════════ */
   await grp('CL2a', async()=>{
     await openView(NO); await wait(1200);
     const box=rowBox();
     T('CL2-1 아랫줄 상자가 있다',!!box,CARD?'.vbot .tools':'#pRow1');
     if(!box)return;
     const shown=[...box.children].filter(vis).map(x=>x.id||('('+x.className+')'));
     N('CL2 실측 아랫줄 보이는 차례',shown);
     if(CARD){
       T('CL2-1 ★보이는 차례가 다섯+Claude 다',
         JSON.stringify(shown)===JSON.stringify(ROW),shown);
       T('CL2-1 ★맨 오른쪽이 #tGpt 다',shown[shown.length-1]==='tGpt',shown.slice(-2));
       T('CL2-1 #tGpt 글자가 「Claude」다',txt(document.getElementById('tGpt'))==='Claude',
         txt(document.getElementById('tGpt')));
       /* DOM 차례도 같아야 한다(보이는 것만 추려서) */
       const dom=[...box.querySelectorAll('#'+ROW.join(',#'))].map(x=>x.id);
       T('CL2-1 DOM 차례도 같다',JSON.stringify(dom)===JSON.stringify(ROW),dom);
     }
     /* 꼴 실측 — 과목 사이 대조는 파이썬이 한다 */
     const st={};ROW.forEach(id=>{st[id]=styleOf(document.getElementById(id))});
     N('CL2 실측 아랫줄 꼴',st);
     /* 「+회독」이 한 줄인가 */
     const la=document.getElementById('tLayerAdd');
     T('CL2-2 「+회독」이 한 줄이다(1500px)',!!la&&la.getClientRects().length===1,
       la?[la.getClientRects().length,txt(la)]:null);
   });

   if(CARD){
   /* ══════════ CL2-4 창 머리 · CL2-3 동작 ══════════ */
   await grp('CL2b', async()=>{
     const g=document.getElementById('tGpt');
     T('CL2-3 #tGpt 가 눌리는 자리에 있다',vis(g)&&g.getBoundingClientRect().width>0,
       g?Math.round(g.getBoundingClientRect().width):null);
     g.click(); await wait(800);
     let sh=sheetNow();
     T('CL2-3 ★누르면 Claude 창이 뜬다',!!sh&&!!sh.querySelector('.panel'));
     const p=sh&&sh.querySelector('.panel>p');
     const pt=txt(p);
     N('CL2 실측 창 머리 둘째 줄',pt);
     T('CL2-4 ★둘째 줄에 undefined 가 없다',pt.indexOf('undefined')<0,pt);
     /* 옛: T('CL2-4 ★둘째 줄이 빈 「 · 」 로 시작하지 않는다', pt.length>2&&pt.charAt(0)!=='·'&&pt.indexOf('·')>0,pt);
        ★ uid_unify §C-2 — 카드 층 창 둘째 줄(#gpSub)은 「코드 · 이름」 이 아니라 왼쪽 QA 줄(없으면 빈칸) + 오른쪽 「▶ 모션」(있을 때만) · 앞이 「 · 」 로 시작하지 않고 빈 「 ·  」 가 없다 + (빈칸 또는 QA 줄 꼴) 로 읽는다 */
     T('CL2-4 ★둘째 줄이 빈 「 · 」 로 시작하지 않는다',
       (sh&&sh.querySelector('.panel>#gpSub'))
         ? (pt.charAt(0)!=='·'&&pt.indexOf(' ·  ')<0&&/^((지학|생물)QA [EB]\d{3} · 질문일 \d{4}-\d{2}-\d{2})?(▶ 모션)?$/.test(pt))
         : (pt.length>2&&pt.charAt(0)!=='·'&&pt.indexOf('·')>0),pt);
     /* 글이 없으니 고치기 판이 먼저다 */
     const ta=sh.querySelector('#gpIn');
     T('CL2-3 글이 없으면 textarea 부터',!!ta);
     ta.value='① 카드 층 시험\n- 한 줄\n- 두 줄';
     sh.querySelector('#gpSave').click(); await wait(900);
     T('CL2-3 ★저장하면 「Claude ✓」',txt(document.getElementById('tGpt'))==='Claude ✓',
       txt(document.getElementById('tGpt')));
     T('CL2-3 ✓ 색이 물리와 같은 var(--teal) 계열이다',
       getComputedStyle(document.getElementById('tGpt')).color!=='',
       getComputedStyle(document.getElementById('tGpt')).color);
     N('CL2 실측 ✓ 색',getComputedStyle(document.getElementById('tGpt')).color);
     killSheets();
     /* 다른 문항으로 → ✓ 사라짐 · 돌아오면 ✓ */
     await openView(NO2); await wait(1200);
     T('CL2-3 ★다른 문항에서는 ✓ 가 없다',txt(document.getElementById('tGpt'))==='Claude',
       txt(document.getElementById('tGpt')));
     await openView(NO); await wait(1200);
     T('CL2-3 ★돌아오면 ✓ 가 다시 붙는다',txt(document.getElementById('tGpt'))==='Claude ✓',
       txt(document.getElementById('tGpt')));
     /* 그 과목 통에만 들어갔나 */
     const kv=await get('kv','gpt');
     /* 옛: T('CL2-3 ★글이 그 과목 IndexedDB 에만 들어갔다', !!kv&&!!kv[NO]&&CUR.DB.indexOf(SUBJ_ID.slice(0,3))>=0&&REC_PATH.indexOf(SUBJ_ID)===0, — ★ uid_unify §A-1 카드 층 kv.gpt 열쇠 = uid(앱 qk) · 옛 판은 번호 */
     T('CL2-3 ★글이 그 과목 IndexedDB 에만 들어갔다',
       !!kv&&!!kv[(typeof qk==='function')?qk(NO):NO]&&CUR.DB.indexOf(SUBJ_ID.slice(0,3))>=0&&REC_PATH.indexOf(SUBJ_ID)===0,
       [CUR.DB,REC_PATH,kv?Object.keys(kv):null]);
   });

   /* ══════════ CL2-5 목록 태그 ══════════ */
   await grp('CL2c', async()=>{
     /* 목록으로 돌아간다 */
     const back=document.getElementById('vBack')||document.querySelector('#view .back,#vTop .back');
     if(back)back.click(); else $('#view').classList.add('hide');
     draw(); await wait(900);
     const rows=$$$('#list .item');
     const gp=$$$('#list .item .tag.gp');
     T('CL2-5 ★글 넣은 줄에 보라 「Claude」 태그가 1개 선다',
       gp.length===1&&txt(gp[0])==='Claude',[gp.length,gp.map(x=>txt(x))]);
     N('CL2 실측 태그 색',gp.length?[getComputedStyle(gp[0]).backgroundColor,
       getComputedStyle(gp[0]).color,getComputedStyle(gp[0]).borderTopColor]:null);
     T('CL2-5 글 없는 줄에는 0개',rows.length>1&&gp.length===1,[rows.length,gp.length]);
     /* 곁가지 표시가 살아나지 않았나 */
     const side={nog:$$$('#list .num.nog').length,tw:$$$('#list .tag.tw').length,
                 lk:$$$('#list .tag.lk').length,qt:$$$('#list .tag.qt').length,
                 star:$$$('#list .star').length,vlt:$$$('#list .tag.vlt').length,
                 lv:$$$('#list .tag[class*="lv"]').length};
     N('CL2 실측 곁가지 표시',side);
     /* 상주 서랍 */
     const dr=document.getElementById('navdr');
     N('CL2 실측 서랍',{있나:!!dr,gp:dr?dr.querySelectorAll('.tag.gp').length:null,
       줄:dr?dr.querySelectorAll('.ndrow').length:null});
     T('CL2-5 상주 서랍 줄에는 태그가 안 붙는다',
       !dr||dr.querySelectorAll('.tag.gp').length===0,
       dr?dr.querySelectorAll('.tag.gp').length:'서랍 없음');
     /* 지우면 떨어진다 */
     await openView(NO); await wait(1100);
     document.getElementById('tGpt').click(); await wait(800);
     let sh=sheetNow();
     if(sh.querySelector('#gpEdit')){sh.querySelector('#gpEdit').click(); await wait(400); sh=sheetNow()}
     sh.querySelector('#gpDel').click(); await wait(900);
     T('CL2-5 지우기 → 단추 ✓ 가 사라진다',txt(document.getElementById('tGpt'))==='Claude',
       txt(document.getElementById('tGpt')));
     draw(); await wait(700);
     T('CL2-5 ★지우기 → 목록 태그가 0개',$$$('#list .item .tag.gp').length===0,
       $$$('#list .item .tag.gp').length);
   });

   /* ══════════ CL2-3 아랫줄 다섯 동작 회귀 ══════════ */
   await grp('CL2d', async()=>{
     await openView(NO); await wait(1100);
     const eye=document.getElementById('tLayerEye'), add=document.getElementById('tLayerAdd'),
           sel=document.getElementById('tLayer'), hist=document.getElementById('tHist'),
           card=document.getElementById('tCard');
     T('CL2-3 다섯이 다 눌리는 자리에 있다',
       [eye,add,sel,hist,card].every(x=>vis(x)&&x.getBoundingClientRect().width>0),
       [eye,add,sel,hist,card].map(x=>x?Math.round(x.getBoundingClientRect().width):null));
     const opt0=sel?sel.options.length:0;
     add.click(); await wait(700);
     T('CL2-3 「+회독」이 회독을 늘린다',sel.options.length===opt0+1,[opt0,sel.options.length]);
     const on0=eye.classList.contains('on');
     eye.click(); await wait(300);
     T('CL2-3 「👁」가 토글된다',eye.classList.contains('on')!==on0,
       [on0,eye.classList.contains('on')]);
     eye.click(); await wait(300);
     killSheets();
     hist.click(); await wait(700);
     T('CL2-3 「기록」이 창을 연다',$$$('body>.sheet').length>0,$$$('body>.sheet').length);
     killSheets(); await wait(200);
     card.click(); await wait(800);
     T('CL2-3 「암기카드」가 창을 연다',
       $$$('body>.sheet').length>0||!!document.querySelector('.mcwin,#mcw'),
       [$$$('body>.sheet').length,!!document.querySelector('.mcwin,#mcw')]);
     killSheets();
   });
   }

   /* ══════════ CL2-6 물리 무변 실측 (파이썬이 바탕과 맞댄다) ══════════ */
   await grp('CL2e', async()=>{
     const back=document.getElementById('vBack')||document.querySelector('#view .back,#vTop .back');
     if(back)back.click(); else $('#view').classList.add('hide');
     FL.past='';FL.q='';FL.unit='';FL.bigs=[];FL.subs=[];FL.round='';FL.mark='';FL.lv='';FL.star=false;FL.year='';
     draw(); await wait(900);
     /* ★ physprev(10/1 하위 에이전트 C) — _task_jagwa_physprev A-2: 물리만 미리보기 칸(.prev · .pvfig)을 두 판 모두 떼고 잰다(그 칸은 physprev 관문 B3 이 잰다) */
     N('CL2 실측 목록 25줄',$$$('#list .item').slice(0,25).map(x=>{if(typeof HASBOOK!=='undefined'&&!HASBOOK){const c=x.cloneNode(true);c.querySelectorAll('.prev,.pvfig').forEach(e=>e.remove());return txt(c)}return txt(x)}).join(' || '));
     await openView(NO); await wait(1200);
     N('CL2 실측 아랫줄 글',txt(document.querySelector('.vbot')));
     const box=rowBox();
     N('CL2 실측 아랫줄 전수 꼴',box?[...box.children].map(x=>[x.id||('.'+x.className),
       vis(x)?1:0,styleOf(x).fontSize,styleOf(x).fontWeight,styleOf(x).color,
       styleOf(x).borderTopWidth,styleOf(x).backgroundColor,styleOf(x).paddingLeft]):null);
   });

   /* ══════════ CL2-2 좁은 폭(380px) — 「+회독」 한 줄 ══════════ */
   await grp('CL2f', async()=>{
     const ifr=document.createElement('iframe');
     ifr.id='cl2phone';
     ifr.style.cssText='position:fixed;left:0;top:0;width:380px;height:860px;border:0;z-index:99999;background:#fff';
     ifr.src='phone.html';
     document.body.appendChild(ifr);
     const ok=await until(()=>{try{return ifr.contentWindow&&ifr.contentWindow.__phready}catch(e){return false}},45000);
     T('CL2-2 380px 판이 떴다',!!ok,ok?null:(()=>{try{return ifr.contentWindow.__pherr||'시간 초과'}catch(e){return String(e)}})());
     if(ok){
       const d=ifr.contentDocument;
       const la=d.getElementById('tLayerAdd');
       T('CL2-2 ★380px 에서도 「+회독」이 한 줄이다',
         !!la&&la.getClientRects().length===1,
         la?[la.getClientRects().length,String(la.textContent).trim(),
             Math.round(la.getBoundingClientRect().width),
             Math.round(la.getBoundingClientRect().height)]:null);
       const g=d.getElementById('tGpt');
       if(CARD)T('CL2-2 380px 에서도 #tGpt 가 보인다',!!g&&g.offsetParent!==null,
         g?[g.offsetParent!==null,String(g.textContent).trim()]:null);
       N('CL2 실측 380px 아랫줄',[...(d.querySelector(CARD?'.vbot .tools':'#pRow1')||{children:[]}).children]
         .filter(x=>x.offsetParent!==null).map(x=>x.id));
     }
     ifr.remove();
   });

   T('CL2 콘솔 오류 0',(window.__err||[]).length===0,window.__err);
"""

PHONE2 = r"""<script>
(function(){
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const until=async(fn,ms)=>{const t0=Date.now();while(Date.now()-t0<(ms||40000)){try{if(fn())return true}catch(e){}await wait(80)}return false};
 const __nf=window.fetch.bind(window);
 window.fetch=async function(url,opt){
  opt=opt||{};const u=String(url);
  const m=/api\.github\.com\/repos\/([^\/]+\/[^\/]+)\/contents\/([^?]+)/.exec(u);
  if(!m){ if(/^https?:/i.test(u))return {ok:false,status:599,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
          return __nf(url,opt); }
  const path=decodeURIComponent(m[2]);
  if(m[1]==='zzikkaplan/notes')return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  if((opt.method||'GET')==='PUT')return {ok:true,status:200,json:async()=>({content:{sha:'x'}}),text:async()=>''};
  const r=await __nf('/data/'+encodeURI(path),{cache:'no-store'});
  if(!r.ok)return {ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)};
  const acc=(opt.headers||{}).Accept||'';
  if(acc.indexOf('raw')>=0)return r;
  return {ok:true,status:200,json:async()=>({sha:'sha'}),text:async()=>JSON.stringify({sha:'sha'})};
 };
 async function go(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   if(typeof HASBOOK!=='undefined'&&HASBOOK&&typeof loadEarthData==='function'){await loadEarthData()}
   await until(()=>DATA.length>0,45000);
   FL.past='';draw();await wait(300);
   await openView(DATA[0][F.NO]); await wait(1200);
   window.__phready=1;
  }catch(e){window.__pherr=String(e&&e.stack||e)}
 }
 if(document.readyState==='complete')setTimeout(go,900);else window.addEventListener('load',()=>setTimeout(go,900));
})();
</script>"""


def build(mode, src_text, subj):
    stub = E.STUB.replace('__SUBJ__', subj)
    anchor = '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js'
    html = src_text.replace(anchor, stub + anchor, 1)
    body = BODY_CL2.replace('__ROW__', json.dumps(ROW))
    open(os.path.join(OUT, 'app.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', E.HEAD + body + E.TAIL + '</body>', 1))
    open(os.path.join(OUT, 'phone.html'), 'w', encoding='utf-8', newline='').write(
        html.replace('</body>', PHONE2 + '</body>', 1))
    m = os.path.join(OUT, 'motion')
    shutil.rmtree(m, ignore_errors=True)
    os.makedirs(m, exist_ok=True)
    for f in ('phys_72.html', 'index.json'):
        shutil.copyfile(os.path.join(MOTDIR, f), os.path.join(m, f))


def run(mode, subj, src_text, secs=340):
    build(mode, src_text, subj)
    spd = os.path.join(SPDROOT, subj)
    done = threading.Event()
    box = {}

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=OUT, **k)

        def log_message(self, *a, **k):
            pass

        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/data/'):
                rel, pre = p[6:], subj + '/'
                if not rel.startswith(pre):
                    self.send_response(404); self.end_headers(); return
                f = os.path.join(spd, rel[len(pre):].replace('/', os.sep))
                if not os.path.isfile(f):
                    self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                if subj in ('earth', 'bio') and rel == subj + '/기록.json':
                    # ★ A-6(d) 9/30 _task_qa_baseline — claude_e001 적재(studyplandata cbd451ae · 결정로그 9/29 20:35)가 지학 기록에 Claude 풀이 둘(gpt 149·84)을 넣어
                    #   CL2-5(글 넣은 줄 태그 1 · 글 없는 줄 0 · 지우면 0)가 그 둘을 더 센다 → 카드 층 기록 사본에서 gpt 칸과 그 도장만 비운다(claude_e001 하네스 recs() 바탕 꼴 · 다른 칸 그대로)
                    j = json.loads(b.decode('utf-8'))
                    j.setdefault('data', {})['gpt'] = {}
                    for kk in ('u', 'gone'):
                        j[kk] = {x: y for x, y in (j.get(kk) or {}).items() if not str(x).startswith('gpt|')}
                    b = json.dumps(j, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b)))
                self.send_header('X-Sha', hashlib.sha1(b).hexdigest())
                self.end_headers(); self.wfile.write(b); return
            return super().do_GET()

        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n).decode('utf-8', 'replace')
            self.send_response(204); self.end_headers()
            if self.path.startswith('/partial'):
                box['partial'] = body; return
            if self.path.startswith('/snap') or self.path.startswith('/cap'):
                return
            box['txt'] = body; done.set()

    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    prof = os.path.join(OUT, 'prof_' + mode)
    shutil.rmtree(prof, ignore_errors=True)
    t0 = time.time()
    p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
                          '--user-data-dir=' + prof, '--window-size=1500,950',
                          'http://127.0.0.1:%d/app.html' % port],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    got = done.wait(secs)
    p.terminate()
    try:
        p.wait(10)
    except Exception:
        p.kill()
    srv.shutdown()
    print('  [%s] %.0fs' % (mode, time.time() - t0))
    if not got:
        return ['FAIL | %s 묶음이 시간 안에 안 끝났다 | %s'
                % (mode, box.get('partial', '(중간 결과 없음)')[-2500:])]
    return [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]


def _firstdiff(a, b):
    """어긋난 자리를 **글자로** 찍는다 — 통째로 900자 자르면 어디가 다른지 못 본다."""
    sa, sb = json.dumps(a, ensure_ascii=False), json.dumps(b, ensure_ascii=False)
    i = next((k for k in range(min(len(sa), len(sb))) if sa[k] != sb[k]), min(len(sa), len(sb)))
    return json.dumps({'길이': [len(sa), len(sb)], '갈린자리': i,
                       '새판': sa[max(0, i - 70):i + 90],
                       '바탕': sb[max(0, i - 70):i + 90]}, ensure_ascii=False)


def static_checks():
    out = []

    def T(name, cond, info=''):
        out.append(('PASS' if cond else 'FAIL') + ' | ' + name
                   + ('' if cond else ' | ' + json.dumps(info, ensure_ascii=False, default=str)))

    raw = open(SRC, 'rb').read()
    s = raw.replace(b'\r\n', b'\n').decode('utf-8')
    base = base_text()
    # ★ A-6(d) 9/30 _task_qa_baseline — 「사라진 바탕 줄」은 이 판(add1) 인도 검산이다 → 새 쪽을 인도 판 007fde4 로 박는다(두 커밋 사이 f810502 ↔ 007fde4 · 수행 결과 「소스 diff +43 / −9」)
    s_dl = subprocess.run(['git', '-C', GENIE, 'show', '007fde4:jagwa/index.html'], capture_output=True).stdout.replace(b'\r\n', b'\n').decode('utf-8')

    T('CL2-Z 줄끝이 CRLF 그대로다(외톨이 LF 0)',
      raw.count(b'\r\n') > 9000 and raw.replace(b'\r\n', b'').count(b'\n') == 0,
      [raw.count(b'\r\n'), raw.replace(b'\r\n', b'').count(b'\n')])
    T('CL2-Z 바탕보다 줄이 늘기만 했다',
      len(s.split('\n')) > len(base.split('\n')),
      [len(s.split('\n')), len(base.split('\n'))])
    gone = [l for l in set(base.split('\n')) - set(s_dl.split('\n')) if l.strip()]   # ★ A-6(d) — 인도 판 007fde4(위 s_dl)
    T('CL2-Z 사라진 바탕 줄이 열 줄 아래다(손댄 자리뿐)', len(gone) <= 10,
      [g.strip()[:80] for g in gone])
    out.append('NOTE | CL2-Z 사라진 바탕 줄 | '
               + json.dumps([g.strip()[:90] for g in gone], ensure_ascii=False))

    # ── 물리 몫을 곁가지로 안 건드렸나 ──
    for pat, ko, n in [
            (r'const PH=!HASBOOK;', 'PH 정의', 1),
            (r'\(PH&&r\[F\.STAR\]\)', '★ 는 물리 갈래 그대로', 1),
            (r'\(PH&&r\[F\.VLT\]\)', '볼트 태그는 물리 갈래 그대로', 1),
            (r"PH\?\(typeof typeOf==='function'", '유형 태그는 물리 갈래 그대로', 1),
            (r"PH&&r\[F\.SRC\]!=='변리사'", '.nog 는 물리 갈래 그대로', 1),
            (r'function physRowBuild\(\)\{\n  if\(HASBOOK\|\|!SHELL\)return;', 'physRowBuild 머리', 1),
            (r'if\(HASBOOK\)showProblem=async function\(\)\{', '카드 층 showProblem 머리', 1),
            (r'gptSheet', 'gptSheet 이름', 4)]:
        a, b = len(re.findall(pat, s)), len(re.findall(pat, base))
        T('CL2-Z %s : 바탕과 같은 수' % ko, a == b and a >= 1, [a, b])

    # ── 물리 lk2 규칙의 **선언**이 한 글자도 안 바뀌었나 ──
    for decl in ['{width:auto;height:auto;padding:4px 8px;border:0;background:none;',
                 'font-size:11.5px;font-weight:600;color:var(--muted);border-radius:6px}',
                 '{white-space:nowrap}',
                 '{appearance:none;-webkit-appearance:none;']:
        T('CL2-Z 물리 lk2 선언 무변 — %s' % decl[:42],
          s.count(decl) == base.count(decl) and base.count(decl) >= 1,
          [s.count(decl), base.count(decl)])
    T('CL2-Z 물리 #pRow1 선택자가 그대로 남아 있다',
      s.count('body[data-layer="pdf"] #pRow1 .lk2') == base.count('body[data-layer="pdf"] #pRow1 .lk2'),
      [s.count('body[data-layer="pdf"] #pRow1 .lk2'),
       base.count('body[data-layer="pdf"] #pRow1 .lk2')])
    T('CL2-Z 카드 층 lk2 선택자가 다섯 곳 생겼다',
      s.count('body[data-book] .vbot .tools .lk2')
      + s.count('body[data-book] .vbot .tools select.lk2') == 5,
      [s.count('body[data-book] .vbot .tools .lk2'),
       s.count('body[data-book] .vbot .tools select.lk2')])
    T('CL2-Z 카드 층 숨김 목록에서 #tGpt 만 빠졌다',
      'body[data-layer="card"] #tGpt' not in s
      and 'body[data-layer="card"] #tTwin' in s
      and 'body[data-layer="card"] #tType' in s)
    T('CL2-Z cardRowBuild 가 한 번 정의되고 한 번 불린다',
      len(re.findall(r'function cardRowBuild\(\)', s)) == 1
      and len(re.findall(r'^cardRowBuild\(\);', s, re.M)) == 1,
      [len(re.findall(r'function cardRowBuild\(\)', s)),
       len(re.findall(r'^cardRowBuild\(\);', s, re.M))])
    T('CL2-Z cardRowBuild 는 카드 층에서만 돈다',
      'if(!HASBOOK||!SHELL)return;' in s)
    return out


def main():
    src = io.open(SRC, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    cur = md5lf(open(SRC, 'rb').read())
    print('[src ] md5(LF) %s' % cur)
    if cur == BASE_MD5:
        raise SystemExit('NG  아직 고치기 전 판이다 — _patch_jagwa_claude_slot_add1.py 를 먼저 돌려라')
    base = base_text()
    lines, meas = [], {}
    only = [a for a in sys.argv[1:] if not a.startswith('-')]

    def grab(mode, r):
        for x in r:
            if x.startswith('NOTE') and 'CL2 실측' in x:
                k = x.split('|')[1].strip()
                try:
                    meas.setdefault(mode, {})[k] = json.loads(x.split('|', 2)[2].strip())
                except Exception:
                    meas.setdefault(mode, {})[k] = None

    for mode, subj, txt_ in [('earth', 'earth', src), ('bio', 'bio', src), ('phys', 'phys', src),
                             ('earthbase', 'earth', base), ('biobase', 'bio', base),
                             ('physbase', 'phys', base)]:
        if only and mode not in only:
            continue
        r = run(mode, subj, txt_)
        grab(mode, r)
        ko = {'earth': '지학', 'bio': '생물', 'phys': '물리',
              'earthbase': '바탕지학', 'biobase': '바탕생물', 'physbase': '바탕물리'}[mode]
        if mode.endswith('base'):
            continue
        lines += [x.replace('| CL2', '| [%s] CL2' % ko, 1) for x in r]

    def M(mode, key):
        return (meas.get(mode) or {}).get(key)

    # ── CL2-2 꼴 — 카드 층 여섯이 물리 같은 단추와 같은 계산값인가 ──
    ps = M('phys', 'CL2 실측 아랫줄 꼴')
    for sub, ko in (('earth', '지학'), ('bio', '생물')):
        cs = M(sub, 'CL2 실측 아랫줄 꼴')
        if not ps or not cs:
            lines.append('FAIL | CL2-2 [%s] 꼴 실측을 못 받았다 | %s' % (ko, json.dumps([bool(ps), bool(cs)])))
            continue
        # ⚠ width·height 는 **글자 길이**를 따른다 — 물리 `#tHist` 는 회독이 있으면 「3회독」,
        #   카드 층은 「기록」 이라 같은 꼴이어도 폭이 다르다. 지시서가 든 항목만 맞댄다.
        skip = ('width', 'height')
        bad = {}
        for i in ROW:
            a, b = cs.get(i), ps.get(i)
            if not a or not b:
                bad[i] = 'missing'
                continue
            d = {k: [a[k], b[k]] for k in a if k not in skip and a[k] != b[k]}
            if d:
                bad[i] = d
        lines.append(('PASS' if not bad else 'FAIL')
                     + ' | CL2-2 [%s] ★아랫줄 여섯의 계산 꼴이 물리 #pRow1 과 같다' % ko
                     + ('' if not bad else ' | ' + json.dumps(bad, ensure_ascii=False)))

    # ── CL2-5 태그 색이 물리와 같은가 · 곁가지가 안 살아났나 ──
    pc = M('phys', 'CL2 실측 태그 색')
    for sub, ko in (('earth', '지학'), ('bio', '생물')):
        cc = M(sub, 'CL2 실측 태그 색')
        if pc and cc:
            lines.append(('PASS' if cc == pc else 'FAIL')
                         + ' | CL2-5 [%s] 보라 태그 계산 색이 물리와 같다' % ko
                         + ('' if cc == pc else ' | ' + json.dumps([cc, pc])))
        a, b = M(sub, 'CL2 실측 곁가지 표시'), M(sub + 'base', 'CL2 실측 곁가지 표시')
        if a is not None and b is not None:
            lines.append(('PASS' if a == b else 'FAIL')
                         + ' | CL2-5 [%s] ★곁가지 표시(.nog·쌍둥이·연결·유형·★·볼트·난이도) 수가 바탕과 같다' % ko
                         + ('' if a == b else ' | ' + json.dumps([a, b], ensure_ascii=False)))
        a, b = M(sub, 'CL2 실측 서랍'), M(sub + 'base', 'CL2 실측 서랍')
        if a is not None and b is not None:
            lines.append(('PASS' if a == b else 'FAIL')
                         + ' | CL2-5 [%s] 상주 서랍이 바탕과 같다' % ko
                         + ('' if a == b else ' | ' + json.dumps([a, b], ensure_ascii=False)))

    # ── CL2-6 물리 무변 ──
    for key, ko in (('CL2 실측 목록 25줄', '목록 25줄'),
                    ('CL2 실측 아랫줄 글', '아랫줄 글자'),
                    ('CL2 실측 아랫줄 전수 꼴', '#pRow1 전수 계산 꼴'),
                    ('CL2 실측 아랫줄 보이는 차례', '아랫줄 보이는 차례')):
        a, b = M('phys', key), M('physbase', key)
        if a is None or b is None:
            lines.append('FAIL | CL2-6 물리 %s 실측을 못 받았다' % ko)
            continue
        if key == 'CL2 실측 아랫줄 글' and isinstance(a, str):
            # ★ 합치기 10/1(하위 에이전트 C) — physphone A-3(97883ef 본문 「#tTheory 「공식」 → 「이론」」) — 그 단추 글자만 옛 글자로 맞춘다(바탕 판을 돌려도 같게)
            a = a.replace('암기카드이론개념', '암기카드공식개념', 1)
        lines.append(('PASS' if a == b else 'FAIL')
                     + ' | CL2-6 ★물리 %s 가 바탕과 같다' % ko
                     + ('' if a == b else ' | ' + _firstdiff(a, b)))

    # ── CL2-0 헛잣대 ──
    for sub, ko in (('earth', '지학'), ('bio', '생물')):
        b = M(sub + 'base', 'CL2 실측 아랫줄 보이는 차례')
        if b is None:
            lines.append('FAIL | CL2-0 헛잣대 [%s] 바탕 실측을 못 받았다' % ko)
            continue
        lines.append(('PASS' if (b != ROW and 'tGpt' not in b) else 'FAIL')
                     + ' | CL2-0 헛잣대 — 바탕 %s 아랫줄에는 #tGpt 가 없다(다섯뿐)' % ko
                     + ('' if (b != ROW and 'tGpt' not in b) else ' | ' + json.dumps(b)))
        a, bb = M(sub + 'base', 'CL2 실측 아랫줄 꼴'), M('phys', 'CL2 실측 아랫줄 꼴')
        if a and bb:
            skip = ('width', 'height')
            same = all(all(a[i][k] == bb[i][k] for k in a[i] if k not in skip)
                       for i in ROW if a.get(i) and bb.get(i))
            lines.append(('PASS' if not same else 'FAIL')
                         + ' | CL2-0 헛잣대 — 바탕 %s 꼴은 물리와 **달랐다**(상자 꼴)' % ko
                         + ('' if not same else ' | 바탕이 이미 같았다면 이 판이 잰 것이 없다'))

    lines += static_checks()
    npass = sum(1 for x in lines if x.startswith('PASS'))
    nfail = sum(1 for x in lines if x.startswith('FAIL'))
    nnote = sum(1 for x in lines if x.startswith('NOTE'))
    for x in lines:
        print(x)
    print('\n== 묶음 CL2  %d PASS / %d FAIL / %d NOTE / %d항 ==' % (npass, nfail, nnote, len(lines)))
    sys.exit(0 if nfail == 0 else 2)


if __name__ == '__main__':
    main()
