# -*- coding: utf-8 -*-
r"""_harness_jagwa_dbready — 자과앱 저장 층 「db 열리기 전에 온 부름」 관문(2026-10-10 · 사용자 08:4x 「고쳐」 · 판 jg_dbfix)

  python _harness_jagwa_dbready.py [--new <앱>] [--base <커밋 | 앱 파일>] [--eng chromium,webkit] [--dev pc,phone,pad]
                                   [--subj phys,bio,earth] [--only D1,D2a,...] [--hold 2000] [--res <결과>] [--mode gate|regress|smoke]

  결함: 앱의 get·put·del(·keys·all)이 db 가 열리기 전에 불리면 tx 가 db.transaction 에서 던져
        웹킷 「undefined is not an object (evaluating 'db.transaction')」 페이지 오류 · 그 읽기 · 쓰기가 사라졌다
        (생물 정리판 snIndex 1.5 초 타이머가 웹킷 db 열림(헤드리스 실측 2 초 안팎)을 앞지름 · search g4 · g9 웹킷 흔들림).
  늦춤: init 스크립트가 indexedDB.open 의 onsuccess(· onerror)를 쥐고 있다가 하네스가 푼다(DOMContentLoaded 뒤 --hold ms · 기본 2000 · 상한 15 초).
        그동안 앱 db = 없음 — 이른 동작마다 그때 db 가 없었는지 잰다(있었으면 늦춤 헛것 = FAIL).
  이른 동작(db 없을 때): 부팅(생물 snIndex 타이머가 여기서 돈다) · 검색 칸 입력(#q input) · 보기 상태 저장(설정 시트 「문제별 타이머」 →
        put('kv','set',SET) · 저장된 SET 에 없는 표지 칸 __dbmark 를 같이 실음) · 저장 층 직접 put·get·del·keys(kv dbready_probe · dbready_gone) ·
        기록 동기화 syncRecords(true).
  관문(엔진·기기 = chromium PC · webkit 폰 390 · webkit iPad 820 / 과목 = 물리 · 생물 · 지학 · 한 문맥 = 한 IndexedDB 프로필):
    D1  「transaction」 페이지 오류 0(pageerror + window.__err)                                   헛잣대(바탕 FAIL 이어야)
    D2a 직접 put·get·del·keys — put 1 · get = 그 값(put 뒤 차례) · del 1 · keys 에 probe · 열린 뒤 다시 읽어 같음 · 새로고침 뒤 같음   헛잣대
    D2b 보기 상태 저장 — 열린 뒤 저장 SET 에 표지 · 저장 SET = 메모리 SET · 시동 칸(autoNextReset · p3reset · 물리 renum 2) 그대로 · 새로고침 뒤 표지   헛잣대
    D2c 기록 동기화 — 이른 syncRecords 가 오류 없이 끝남(recErr '') · 저장 status = 메모리 ST · 새로고침 뒤 ST 같음   헛잣대
    D2d 덮어쓰기 없음 — 씨앗(보통 부팅) 프로필에서 늦춘 부팅 뒤 ST = 씨앗 ST · SET 시동 칸 그대로(이른 쓰기가 시동 읽기를 앞질러 덮으면 FAIL)   기준(바탕도 PASS)
    D3  검색 — 늦춘 부팅 뒤 같은 말 → ES_NOS = 늦추지 않은 부팅 값                                기준
    D4  보통 부팅(늦춤 없음) 값 무변 — DATA 수 · #cnt · 목록 줄(uid · 번호) · ST · SET · kv 열쇠(ink* 뺌) · 검색 = 바탕(gate) / 기준 스냅샷(regress)
    D5  열기 실패(같은 이름 DB 를 판 2 로 먼저 열어 앱 open(이름,1) = VersionError · onerror 도 쥐었다 푼다) — 기다리던 부름이 15 초 안에 다 끝남(멈춤 없음) ·
        쓰기(put·del) 0 · 읽기(get·keys) = 열기 오류로 거절(빈 값으로 「읽었다」 안 됨) · 이른 동기화 = 오류로 끝남 · 「transaction」 0   헛잣대
        (새 문맥 = 빈 프로필에서 — 씨앗 문맥이면 판 2 올림이 막혀(blocked) open 이 끝나지 않는다 · Run.fail 주석)
  헛잣대 = 바탕 d48e4a8(이 판 앞 main) — 늦추면 페이지 오류 · 이른 쓰기 사라짐 · 이른 동기화 오류 · 열기 실패 때 쓰기도 TypeError.
  ⚠ 자과앱 픽셀 게이트 없음(CLAUDE.md) — DOM 글자 · 개수 · 저장 값.
  모드: gate(바탕 띄움 · 헛잣대) · regress(NEW 만 · D4 = 기준 스냅샷) · smoke(chromium PC · 생물 · D1 · D2a).
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기(Srv · Dev · INIT_HU · JS_HU · git_HU · PAD)
import hashlib, io, json, os, re, sys, time   # noqa: E402
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


GENIE = _roots.genie(); SPD = _roots.spd()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEF = ARG('--base', 'd48e4a8')   # 헛잣대 바탕 = 이 판 앞 main(dbready 없음) · 앱 파일 자리를 주면 그 파일
ENGS = [x for x in (ARG('--eng', 'chromium,webkit') or '').split(',') if x]
DEVS = [x for x in (ARG('--dev', 'pc,phone,pad') or '').split(',') if x]
SUBJS = [x for x in (ARG('--subj', 'phys,bio,earth') or '').split(',') if x]
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
HOLD = int(ARG('--hold', '2000'))
OUTF = ARG('--res', os.path.join(HERE, '_harness_jagwa_dbready_result.txt'))
from playwright.sync_api import sync_playwright   # noqa: E402

COMBOS = [('chromium', 'pc'), ('webkit', 'phone'), ('webkit', 'pad')]   # 사용자 기기 = 아이폰 · 아이패드(웹킷) + PC
QUERY = {'phys': '속력', 'bio': '플라스미드', 'earth': '광물'}   # 과목마다 걸리는 말(늦추지 않은 부팅에서 결과 > 0 을 같이 잰다)
ROWS = []   # (관문, 기기, 과목, 이름, NEW ok, BASE ok, 잰 값, 종류)
KIND = {'D1': '헛잣대', 'D2a': '헛잣대', 'D2b': '헛잣대', 'D2c': '헛잣대', 'D2d': '기준', 'D3': '기준', 'D4': '무변', 'D5': '헛잣대'}
NAME = {'D1': '늦춘 부팅 + 이른 동작 → 「transaction」 페이지 오류 0',
        'D2a': '직접 put·get·del·keys(db 없을 때) → 열린 뒤 · 새로고침 뒤 남음',
        'D2b': '보기 상태 저장(설정 시트 타이머 · SET 표지) → 열린 뒤 · 새로고침 뒤 남음 · 시동 칸 그대로',
        'D2c': '기록 동기화(db 없을 때 syncRecords) → 오류 없음 · 저장 status = 메모리 ST · 새로고침 뒤 같음',
        'D2d': '덮어쓰기 없음 — 늦춘 부팅 뒤 ST = 씨앗 ST · SET 시동 칸 그대로',
        'D3': '검색 — 늦춘 부팅 뒤 같은 말 = 늦추지 않은 부팅 결과',
        'D4': '보통 부팅 값 무변(DATA · #cnt · 목록 줄 · ST · SET · kv 열쇠 · 검색)',
        'D5': '열기 실패(VersionError) — 기다리던 부름이 끝남(멈춤 없음) · 쓰기 0 · 읽기 = 열기 오류 · 이른 동기화 오류로 끝남'}
SMOKE_IDS = ('D1', 'D2a')
TX = re.compile(r'transaction')

# ── db 열림 쥐기 — 앱의 indexedDB.open 요청에서 onsuccess · onerror 를 가로채 쥐고 있다가 __dbRelease() 로 푼다(상한 CAP ms 뒤엔 저절로) ──
HOLD_JS = r"""(()=>{const CAP=15000;const Q=window.__dbq={req:0,succ:null,err:null,app:null,cap:0};
 const o=IDBFactory.prototype.open;
 IDBFactory.prototype.open=function(){const req=o.apply(this,arguments);Q.req++;
  const H={success:null,error:null};let ev=null,kind=null,done=false;
  try{['success','error'].forEach(k=>Object.defineProperty(req,'on'+k,{configurable:true,get(){return H[k]},set(f){H[k]=f}}))}catch(e){Q.defErr=String(e);return req}
  const go=()=>{if(done||!ev)return;done=true;Q.app=Math.round(performance.now());const h=H[kind];try{if(h)h.call(req,ev)}catch(e){setTimeout(()=>{throw e})}};
  const got=k=>e=>{ev=e;kind=k;Q[k==='success'?'succ':'err']=Math.round(performance.now());if(window.__dbRel)go();else setTimeout(()=>{if(!done)Q.cap=1;go()},CAP)};
  req.addEventListener('success',got('success'));req.addEventListener('error',got('error'));
  window.__dbRelease=()=>{window.__dbRel=true;go()};
  return req}})();"""
# D5 — 열기 실패 만들기: 앱보다 먼저(쥐기 앞 init) 같은 이름 DB 를 판 2 로 연다 → 앱의 open(이름, 1) = VersionError → onerror(쥐었다 푼다)
V2_JS = r"""(()=>{try{indexedDB.open('__DBN__',2)}catch(e){}})();"""

DBNOW = "typeof db!=='undefined'&&!!db"

# ── 이른 동작 넷(db 없을 때 · 각자 그때 db 상태를 돌려준다) ──
EARLY_SEARCH = r"""q=>{const R={db0:%s};const e=document.getElementById('q');if(!e)return Object.assign(R,{err:'#q 없음'});
  e.value=q;e.dispatchEvent(new Event('input',{bubbles:true}));R.n=(typeof ES_NOS!=='undefined'&&ES_NOS)?ES_NOS.length:null;return R}""" % DBNOW
EARLY_PROBE = r"""()=>{const R={db0:%s};const P=window.__dbpr={};
  const cap=(k,f)=>{try{Promise.resolve(f()).then(v=>{P[k]={v:v===undefined?null:v}},e=>{P[k]={err:String(e&&e.message||e)}})}catch(e){P[k]={err:'즉시 '+String(e&&e.message||e)}}};
  cap('put',()=>put('kv','dbready_probe',{v:'early',n:7}));
  cap('get',()=>get('kv','dbready_probe'));
  cap('del',()=>del('kv','dbready_gone'));
  cap('keys',()=>keys('kv').then(a=>({n:a.length,probe:a.indexOf('dbready_probe')>=0,gone:a.indexOf('dbready_gone')>=0})));
  R.db1=%s;return R}""" % (DBNOW, DBNOW)
EARLY_SET = r"""()=>{const R={db0:%s};
  SET.__dbmark='early';   /* 표지 칸 — 저장된 SET 에 없는 칸(시동의 Object.assign 이 안 덮음) → 열린 뒤 저장 SET 에 있으면 이른 쓰기가 닿은 것 */
  const b=document.getElementById('btnSet');if(!b)return Object.assign(R,{err:'#btnSet 없음'});b.click();
  const t=document.querySelector('.sheet #bTimer');R.sheet=!!t;R.timer0=SET.timer;if(t)t.click();R.timer1=SET.timer;
  try{if(typeof setSheet!=='undefined'&&setSheet){setSheet.remove();setSheet=null}}catch(e){R.closeErr=String(e)}
  R.db1=%s;return R}""" % (DBNOW, DBNOW)
EARLY_SYNC = r"""()=>{const R={db0:%s};window.__esr=null;
  try{syncRecords(true).then(()=>{window.__esr={err:(typeof recErr!=='undefined'?recErr:'')||''}},e=>{window.__esr={throw:String(e&&e.message||e)}})}
  catch(e){window.__esr={throw:'즉시 '+String(e&&e.message||e)}}
  R.db1=%s;return R}""" % (DBNOW, DBNOW)

# ── 값 모으기 ──
SNAP_JS = r"""async q=>{const t=s=>String(s||'').replace(/\s+/g,' ').trim(),c=document.getElementById('cnt');
  const e=document.getElementById('q');let es=null;
  if(e&&q){e.value=q;e.dispatchEvent(new Event('input',{bubbles:true}));es=(typeof ES_NOS!=='undefined'&&ES_NOS)?ES_NOS.slice():null}
  let kv=null;try{kv=(await keys('kv')).map(String).sort()}catch(x){kv='ERR '+x}
  return {data:(typeof DATA!=='undefined')?DATA.length:null,cnt:t(c&&c.textContent),list:(window.__J&&__J.list)?__J.list():null,
    st:JSON.parse(JSON.stringify(ST)),set:JSON.parse(JSON.stringify(SET)),kv:kv,es:es,
    stS:await get('kv','status'),setS:await get('kv','set'),probe:await get('kv','dbready_probe'),gone:await get('kv','dbready_gone'),
    lastSync:((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}')||{}).lastSync||0)}}"""
ERRS_JS = "()=>(window.__err||[]).slice(0,20)"
LAST_JS = "()=>((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}')||{}).lastSync||0)"


def md5(o):
    return hashlib.md5(json.dumps(o, ensure_ascii=False, sort_keys=True, default=str).encode('utf-8')).hexdigest()[:12]


def want(g):
    if ONLY and g not in ONLY:
        return False
    return QC.want(g, smoke=g in SMOKE_IDS)


def R(g, dev, subj, okn, okb, val):
    ROWS.append((g, dev, subj, NAME[g], okn, okb, val, KIND[g]))
    print('%s | 바탕 %s | %s · %s · %s · %s | %s' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dev, subj, NAME[g],
          (val if isinstance(val, str) else json.dumps(val, ensure_ascii=False, default=str))[:600]), flush=True)


class Run:
    """한 기기 · 한 과목 · 한 앱(NEW | BASE) = 한 문맥(한 IndexedDB 프로필) — 씨앗(보통 부팅) → 늦춘 부팅 → 새로고침"""

    def __init__(self, br, eng, dev, subj, who, app):
        self.br, self.eng, self.dev, self.subj, self.who, self.app = br, eng, dev, subj, who, app
        self.dv = JG.Dev(br, eng, phone=(dev == 'phone'))
        self.vp = {'width': JG.PAD[0], 'height': JG.PAD[1]} if dev == 'pad' else None
        self.errs = {}

    def load(self, tag, hold=False, pre=None):
        QC.launch('base' if self.who == 'BASE' else 'new')
        dv = self.dv
        dv.S.app = self.app; dv.S.spd = SPD; dv.S.rec = {}; dv.S.static = {}
        if dv.pg:
            dv.pg.close()
        dv.ctx.clear_cookies()
        dv.pg = dv.ctx.new_page(); dv.pg.set_default_timeout(150000)
        if self.vp:
            dv.pg.set_viewport_size(self.vp)
        dv.pg.add_init_script(JG.INIT_HU.replace('__SUBJ__', self.subj))
        if pre:
            dv.pg.add_init_script(pre)   # 쥐기보다 먼저(쥐기에 안 걸리게)
        if hold:
            dv.pg.add_init_script(HOLD_JS)
        el = self.errs.setdefault(tag, [])
        dv.pg.on('pageerror', lambda e: el.append('page: ' + str(e)[:240]))
        dv.pg.goto('http://127.0.0.1:%d/app.html' % dv.S.port, wait_until='domcontentloaded' if hold else 'load')
        dv.pg.evaluate(JG.JS_HU)
        return dv.pg

    def ev(self, js, arg=None):
        return self.dv.ev(js, arg)

    def boot_done(self, last0, what, early_sync=False):
        """시동 끝 표지 — DATA · GG_READY(__J.ready) · db · 목록 줄 · 기록 동기화 끝(lastSync 가 이 부팅 앞 값보다 큼 · recBusy 거짓) · (이른 동기화 끝)"""
        js = ("()=>__J.ready()&&%s&&document.querySelectorAll('#list .item').length>0&&typeof recBusy!=='undefined'&&!recBusy"
              "&&((JSON.parse(localStorage.getItem(SMETA_KEY)||'{}')||{}).lastSync||0)>%d%s") % (DBNOW, int(last0), "&&!!window.__esr" if early_sync else '')
        return QC.until(self.dv.pg, js, 60000, what)

    def seed(self):
        """씨앗 = 보통 부팅(늦춤 없음) — D4 값 · D3 기준 검색 · D2a del 표본(dbready_gone)"""
        pg = self.load('seed')
        ok = self.boot_done(0, '씨앗 부팅 끝(%s · %s)' % (self.dev, self.subj))
        QC.sleep(600, '첫 동기화 뒤 ink 고리(inkKick) 쓰기가 끝나게 — 끝 표지 없음', pg)
        v = self.ev(SNAP_JS, QUERY[self.subj])
        self.ev("async()=>{await put('kv','dbready_gone',{v:'seed'});return 1}")   # D2a — 이른 del 의 표본(보통 부팅에서 심음)
        v['booted'] = ok; v['err'] = self.errs['seed'] + (self.ev(ERRS_JS) or [])
        self.seedv = v
        return v

    def held(self):
        """늦춘 부팅 — db 를 쥔 채 이른 동작 넷 → --hold 까지 기다림 → 풂 → 시동 · 이른 동기화 끝 → 값"""
        last0 = self.seedv.get('lastSync') or 0
        pg = self.load('held', hold=True)
        t0 = time.time()
        early = {'search': self.ev(EARLY_SEARCH, QUERY[self.subj]), 'probe': self.ev(EARLY_PROBE), 'set': self.ev(EARLY_SET), 'sync': self.ev(EARLY_SYNC)}
        rest = HOLD / 1000.0 - (time.time() - t0)
        if rest > 0:
            QC.sleep(int(rest * 1000), 'db 를 쥔 채 --hold 까지 — 생물 snIndex 1.5 초 타이머가 쥔 동안 돈다(실제 결함 자리)', pg)
        early['dbBeforeRelease'] = self.ev("()=>(%s)" % DBNOW)
        early['dbq'] = self.ev("()=>window.__dbq")
        self.ev("()=>{window.__dbRelease&&window.__dbRelease();return 1}")
        ok = self.boot_done(last0, '늦춘 부팅 끝 · 이른 동기화 끝(%s · %s)' % (self.dev, self.subj), early_sync=True)
        QC.until(pg, "()=>{const P=window.__dbpr||{};return ['put','get','del','keys'].every(k=>P[k])}", 15000, '이른 put·get·del·keys 답')
        QC.sleep(600, '풀린 이른 쓰기(설정 put) · ink 고리 쓰기가 끝나게 — 끝 표지 없음', pg)
        v = self.ev(SNAP_JS, QUERY[self.subj])
        v['early'] = early; v['booted'] = ok; v['esr'] = self.ev("()=>window.__esr"); v['dbpr'] = self.ev("()=>window.__dbpr")
        v['err'] = self.errs['held'] + (self.ev(ERRS_JS) or [])
        self.heldv = v
        return v

    def reload(self):
        """새로고침(늦춤 없음) — 이른 쓰기가 저장에 남았나"""
        pg = self.load('reload')
        ok = self.boot_done(self.heldv.get('lastSync') or 0, '새로고침 부팅 끝(%s · %s)' % (self.dev, self.subj))
        QC.sleep(600, '첫 동기화 뒤 ink 고리 쓰기가 끝나게 — 끝 표지 없음', pg)
        v = self.ev(SNAP_JS, '')
        v['booted'] = ok; v['err'] = self.errs['reload'] + (self.ev(ERRS_JS) or [])
        self.relv = v
        return v

    def fail(self):
        """열기 실패 — 새 문맥(빈 프로필)에서 같은 이름 DB 를 판 2 로 먼저 만들어 앱의 open(이름, 1) 을 VersionError 로 · onerror 를 쥔 채 이른 부름 → 풂 → 다 끝나나
        ⚠ 새 문맥이어야 한다 — 씨앗 문맥(판 1 DB 가 있음)에서는 판 2 올림이 앞 쪽의 남은 연결 · 큰 쓰기에 막혀(blocked) 앱 open 이 성공도 오류도 안 낸다
          (10/10 최종 1 차 chromium 지학 실측 = dbq succ · err 둘 다 null · 그동안 새 판 이른 부름은 기다림 · 바탕은 곧장 TypeError — 보고 「남은 위험」)"""
        m = re.search(r"\b%s:\{DB:'([^']+)'" % re.escape(self.subj), self.app.decode('utf-8', 'replace'))
        dbn = m.group(1) if m else None
        if not dbn:
            self.failv = {'err': ['DB 이름 못 찾음(SUBJ 표)'], 'settled': False}
            return self.failv
        try:
            self.dv.close()
        except Exception:
            pass
        self.dv = JG.Dev(self.br, self.eng, phone=(self.dev == 'phone'))   # 새 문맥 = 빈 IndexedDB 프로필
        pg = self.load('fail', hold=True, pre=V2_JS.replace('__DBN__', dbn))
        t0 = time.time()
        early = {'probe': self.ev(EARLY_PROBE), 'sync': self.ev(EARLY_SYNC)}
        rest = HOLD / 1000.0 - (time.time() - t0)
        if rest > 0:
            QC.sleep(int(rest * 1000), 'onerror 를 쥔 채 --hold 까지(이른 부름이 기다리는 사이)', pg)
        early['dbq0'] = self.ev("()=>window.__dbq")
        self.ev("()=>{window.__dbRelease&&window.__dbRelease();return 1}")
        settled = QC.until(pg, "()=>{const P=window.__dbpr||{};return ['put','get','del','keys'].every(k=>P[k])&&!!window.__esr}", 15000,
                           '열기 실패 뒤 기다리던 put·get·del·keys · 이른 동기화 끝')
        v = {'db': dbn, 'early': early, 'settled': settled, 'dbq': self.ev("()=>window.__dbq"), 'dbpr': self.ev("()=>window.__dbpr"), 'esr': self.ev("()=>window.__esr"),
             'err': self.errs['fail'] + (self.ev(ERRS_JS) or [])}
        self.failv = v
        return v

    def close(self):
        self.dv.close()


def d4vals(v):
    """D4 무변 값(보통 부팅) — 시각 · 기기마다 갈리는 것(lastSync · ink* 열쇠)은 뺌"""
    kv = v.get('kv') if isinstance(v.get('kv'), list) else ['ERR']
    return {'data': v.get('data'), 'cnt': v.get('cnt'), 'list_n': len(v.get('list') or []), 'list': md5(v.get('list')),
            'st_n': len(v.get('st') or {}), 'st': md5(v.get('st')), 'set': md5(v.get('set')),
            'kv': [k for k in kv if not k.startswith('ink') and not k.startswith('dbready')], 'es_n': len(v.get('es') or []), 'es': md5(v.get('es'))}


def judge5(run):
    """D5 — 열기 실패 걸음 값 → (ok, 값)"""
    f = run.failv
    P = f.get('dbpr') or {}
    esr = f.get('esr') or {}
    tx = [x for x in f.get('err', []) if TX.search(x)]
    early = f.get('early') or {}
    gerr = (P.get('get') or {}).get('err', '')
    ok = (bool(f.get('settled')) and not any((early.get(k) or {}).get('db0') for k in ('probe', 'sync'))
          and (P.get('put') or {}).get('v') == 0 and (P.get('del') or {}).get('v') == 0
          and bool(gerr) and not TX.search(gerr) and 'err' in (P.get('keys') or {})
          and bool(esr.get('err')) and not TX.search(esr.get('err', '')) and not tx)
    return ok, {'DB': f.get('db'), '다 끝남(15 초 안)': f.get('settled'), '이른 답': P, '이른 동기화': esr, 'transaction 오류': tx[:3],
                '다른 오류': [x for x in f.get('err', []) if not TX.search(x)][:3], 'dbq': f.get('dbq')}


def judge(run):
    """한 Run 의 관문 값 → {관문: (ok, 값)}"""
    out = {}
    if getattr(run, 'failv', None) is not None:
        out['D5'] = judge5(run)
    if getattr(run, 'relv', None) is None:
        return out
    s, h, r = run.seedv, run.heldv, run.relv
    e = h['early']
    early_db = {k: [e[k].get('db0'), e[k].get('db1')] for k in ('search', 'probe', 'set', 'sync') if isinstance(e.get(k), dict)}
    held_ok = not any(any(x) for x in early_db.values()) and e.get('dbBeforeRelease') is False and not (e.get('dbq') or {}).get('cap')
    tx = [x for x in h['err'] if TX.search(x)]
    out['D1'] = (held_ok and not tx and h['booted'], {'transaction 오류': tx[:3], '다른 오류': [x for x in h['err'] if not TX.search(x)][:3],
                                                     '이른 동작 때 db(앞·뒤)': early_db, '풀기 직전 db': e.get('dbBeforeRelease'), 'dbq': e.get('dbq'), '시동 끝': h['booted']})
    P = h.get('dbpr') or {}
    a_ok = (held_ok and (P.get('put') or {}).get('v') == 1 and (P.get('get') or {}).get('v') == {'v': 'early', 'n': 7}
            and (P.get('del') or {}).get('v') == 1 and ((P.get('keys') or {}).get('v') or {}).get('probe') is True
            and h.get('probe') == {'v': 'early', 'n': 7} and h.get('gone') is None
            and r.get('probe') == {'v': 'early', 'n': 7} and r.get('gone') is None)
    out['D2a'] = (a_ok, {'이른 답': P, '열린 뒤 probe · gone': [h.get('probe'), h.get('gone')], '새로고침 뒤': [r.get('probe'), r.get('gone')]})
    ss, sm, rs = h.get('setS') or {}, h.get('set') or {}, r.get('setS') or {}
    keep = ['autoNextReset', 'p3reset'] + (['renum'] if run.subj == 'phys' else [])
    seed_set = s.get('setS') or {}
    b_ok = (held_ok and (e.get('set') or {}).get('sheet') is True and ss.get('__dbmark') == 'early' and md5(ss) == md5(sm)
            and all(ss.get(k) == seed_set.get(k) and seed_set.get(k) is not None for k in keep) and rs.get('__dbmark') == 'early'
            and (r.get('set') or {}).get('__dbmark') == 'early')
    out['D2b'] = (b_ok, {'이른 동작': e.get('set'), '열린 뒤 저장 표지': ss.get('__dbmark'), '저장 = 메모리': md5(ss) == md5(sm),
                        '시동 칸(씨앗 → 열린 뒤)': {k: [seed_set.get(k), ss.get(k)] for k in keep}, '타이머(저장 · 시동이 저장값으로 덮음)': ss.get('timer'),
                        '새로고침 뒤 표지(저장 · 메모리)': [rs.get('__dbmark'), (r.get('set') or {}).get('__dbmark')]})
    esr = h.get('esr') or {}
    c_ok = (held_ok and esr.get('err') == '' and 'throw' not in esr and md5(h.get('stS') or {}) == md5(h.get('st') or {})
            and md5(r.get('st') or {}) == md5(h.get('st') or {}))
    out['D2c'] = (c_ok, {'이른 동기화': esr, '저장 status = 메모리 ST': md5(h.get('stS') or {}) == md5(h.get('st') or {}),
                        'ST 수(씨앗 · 늦춤 · 새로고침)': [len(s.get('st') or {}), len(h.get('st') or {}), len(r.get('st') or {})],
                        '새로고침 뒤 ST = 늦춘 뒤 ST': md5(r.get('st') or {}) == md5(h.get('st') or {})})
    d_ok = md5(h.get('st') or {}) == md5(s.get('st') or {}) and all(ss.get(k) == seed_set.get(k) for k in keep)
    s_st, h_st = s.get('st') or {}, h.get('st') or {}
    moved = sorted((k for k in set(s_st) | set(h_st) if md5(s_st.get(k)) != md5(h_st.get(k))), key=lambda x: (len(str(x)), str(x)))
    out['D2d'] = (d_ok, {'ST md5(씨앗 · 늦춤)': [md5(s_st), md5(h_st)], 'ST 수': [len(s_st), len(h_st)], '값이 바뀐 ST 칸': [len(moved), moved[:12]],
                        '시동 칸(씨앗 · 늦춤)': {k: [seed_set.get(k), ss.get(k)] for k in keep}})
    out['D3'] = ((s.get('es') is not None and len(s.get('es') or []) > 0 and h.get('es') == s.get('es')),
                 {'말': QUERY[run.subj], '이른 입력 때 결과 수': (e.get('search') or {}).get('n'), '늦춤 뒤': len(h.get('es') or []), '보통 부팅': len(s.get('es') or [])})
    out['D4v'] = d4vals(s)
    return out


def main():
    apps = {'NEW': open(NEWF, 'rb').read().replace(b'\r\n', b'\n')}
    if QC.GATE:
        if os.path.isfile(BASEF):
            apps['BASE'] = open(BASEF, 'rb').read().replace(b'\r\n', b'\n')
        else:
            QC.sub('git:show-app')
            apps['BASE'] = JG.git_HU(GENIE, 'show', BASEF + ':jagwa/index.html')
            assert apps['BASE'], '바탕 %s 블롭을 못 꺼냄' % BASEF
    whos = ('NEW', 'BASE') if QC.GATE else ('NEW',)
    combos = [(e, d) for e, d in COMBOS if e in ENGS and d in DEVS]
    subjs = SUBJS
    if QC.SMOKE:
        combos = [c for c in combos if c[0] == 'chromium'][:1] or combos[:1]
        subjs = ['bio'] if 'bio' in SUBJS else SUBJS[:1]
    need_main = any(want(g) for g in ('D1', 'D2a', 'D2b', 'D2c', 'D2d', 'D3', 'D4'))
    need_fail = want('D5')
    t0 = time.time()
    with sync_playwright() as pw:
        brs = {}
        try:
            for eng, dev in combos:
                if eng not in brs:
                    brs[eng] = getattr(pw, eng).launch()
                for subj in subjs:
                    res = {}
                    for who in whos:
                        with QC.stage('%s %s %s %s' % (eng, dev, subj, who)):
                            run = Run(brs[eng], eng, dev, subj, who, apps[who])
                            try:
                                if need_main:
                                    run.seed(); run.held(); run.reload()
                                if need_fail:
                                    run.fail()   # 이 문맥 마지막(DB 판이 2 가 된다)
                                res[who] = judge(run)
                            except Exception as ex:
                                res[who] = {'ERR': repr(ex)[:400]}
                            finally:
                                run.close()
                    devn = '%s·%s' % (eng, dev)
                    for g in ('D1', 'D2a', 'D2b', 'D2c', 'D2d', 'D3', 'D5'):
                        if not want(g):
                            continue
                        n = (res['NEW'].get(g) or (False, '값 없음')) if 'ERR' not in res['NEW'] else (False, res['NEW']['ERR'])
                        b = ((res['BASE'].get(g) or (None, '값 없음')) if 'ERR' not in res['BASE'] else (None, res['BASE']['ERR'])) if 'BASE' in res else (None, None)
                        R(g, devn, subj, bool(n[0]), b[0], {'NEW': n[1], 'BASE': b[1]})
                    if want('D4') and need_main:
                        cid = 'D4@%s/%s' % (devn, subj)
                        nv = res['NEW'].get('D4v') if 'ERR' not in res['NEW'] else None
                        if 'BASE' in res:
                            bv = res['BASE'].get('D4v') if 'ERR' not in res['BASE'] else None
                            QC.base(cid, nv)
                            R('D4', devn, subj, nv is not None and nv == bv and (nv or {}).get('es_n', 0) > 0, None,
                              {'NEW': nv, 'BASE': bv, '다른 칸': sorted(k for k in (nv or {}) if (nv or {}).get(k) != (bv or {}).get(k))})
                        else:
                            bv = QC.base(cid, nv)
                            R('D4', devn, subj, nv is not None and QC.norm(nv) == bv, None, {'NEW': nv, '기준': QC.base_note(cid)})
        finally:
            for b in brs.values():
                try:
                    b.close()
                except Exception:
                    pass
    npass = sum(1 for r in ROWS if r[4]); nfail = sum(1 for r in ROWS if not r[4])
    vac = [r for r in ROWS if r[7] == '헛잣대' and r[5] is True]
    print('\n== PASS %d · FAIL %d · 헛잣대(바탕도 PASS) %d · %.0f초' % (npass, nfail, len(vac), time.time() - t0))
    with io.open(OUTF, 'a', encoding='utf-8') as f:
        f.write('\n==== %s · jagwa_dbready · %s · NEW %s(LF md5 %s) · 바탕 %s · 쥠 %d ms · 엔진·기기 %s · 과목 %s ====\n' % (
            time.strftime('%Y-%m-%d %H:%M'), QC.MODE, NEWF, hashlib.md5(apps['NEW']).hexdigest(), BASEF if QC.GATE else '(regress · 바탕 안 띄움)',
            HOLD, ','.join('%s·%s' % c for c in combos), ','.join(subjs)))
        for g, dev, subj, n, okn, okb, v, k in ROWS:
            f.write('%s | 바탕 %s | %s · %s · %s · %s [%s] | %s\n' % ('PASS' if okn else 'FAIL', {True: 'PASS', False: 'FAIL', None: '—'}[okb], g, dev, subj, n, k,
                    (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str))[:2000]))
        f.write('== PASS %d · FAIL %d · 헛잣대(바탕도 PASS) %d · %.0f초\n' % (npass, nfail, len(vac), time.time() - t0))
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
