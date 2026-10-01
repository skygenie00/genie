# -*- coding: utf-8 -*-
"""생물 앱 판 1 헤드리스 검산 (2026-09-05 · saengmul/_task_bio_app_pan1.md §6-1 · _harness_earth.py 복제)

앱 사본에 ① KaTeX 스텁(pdf.js 는 진짜 CDN) ② 가짜 GitHub(fetch 가로채기 → 로컬 studyplandata/bio) ③ 검사를 주입해 헤드리스 크롬으로 돌린다.
    python _harness_bio.py            # 데스크톱 1400×900 · 과목 bio
    python _harness_bio.py phone      # 390×844 iframe(폰 머리 접기 · _harness_earth.TESTS_PHONE 재사용) · PHONE_SUBJ 기본 bio
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import http.server, os, socketserver, subprocess, sys, threading, hashlib, json, csv, shutil, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _harness_earth as E

GENIE = _roots.genie()
SRC = os.path.join(GENIE, 'jagwa', 'index.html')   # 9/5 자과 서재 이사
SPD = os.path.join(_roots.spd(), 'bio')
SAENG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'saengmul')
OUT = os.path.join(os.environ.get('TEMP', '.'), 'bioh'); os.makedirs(OUT, exist_ok=True)
APP = os.path.join(OUT, 'app.html')

TESTS = E.TESTS.split(' async function run(){')[0].replace("if(m[1]==='zzikkaplan/notes'){", "if(m[1]==='zzikkaplan/notes'&&(opt.method||'GET')!=='PUT'){") + r"""
 async function run(){
  try{
   localStorage.setItem('tt.cfg',JSON.stringify({token:'github_pat_TEST',person:'검산'}));
   await loadEarthData(); draw(); await wait(80);
   const cnt={G:0,T:0,E:0,C:0};DATA.forEach(r=>cnt[kindOf(r)]++);
   /* ===== A-1 켜기 ===== */
   T('A-1 SUBJ.bio.ready=true · 과목 bio · IndexedDB bio1 · 제목(판 2 add4: <title> 자과 서재 · 머리 「자과 서재 · 생물」 · SUBJ.bio.TITLE 은 그대로)',SUBJ.bio.ready===true&&SUBJ_ID==='bio'&&db.name==='bio1'&&document.title==='자과 서재'&&$('.brand h1').textContent==='자과 서재 · 생물'&&SUBJ.bio.TITLE==='생물 기출 서재'&&subjResolve('bio')==='bio'&&document.body.dataset.layer==='card',[SUBJ_ID,db.name,document.title,$('.brand h1').textContent]);
   const cells=$$('#subjTabs button');
   T('A-1 탭 셀 셋 다 살아 있음 · 생물 눌림 · off 0',cells.length===3&&cells[1].classList.contains('on')&&!cells.some(b=>b.classList.contains('off'))&&cells.map(b=>b.textContent).join('│')==='물리│생물│지학');
   T('A-1 물리 기본값 무변(subj 없음·모름 → phys)',subjResolve(null)==='phys'&&subjResolve('nope')==='phys'&&subjResolve('earth')==='earth');
   T('A-1 NCH_MAX 8 · CH_LIST 12 · KINDS 셋 · BOOK_PDF_ADD 없음',CUR.NCH_MAX===8&&CUR.CH_LIST.length===12&&CUR.KINDS.join()==='G,T,E'&&CUR.BOOK_PDF_ADD===undefined&&SUBJ.earth.BOOK_PDF_ADD===11);
   /* ===== A-2 적재 ===== */
   T('A-2 746 적재 · G 270 T 342 E 134 · uid 유일 · B006E·B092E 없음(옛 E006·E092)',DATA.length===746&&cnt.G===270&&cnt.T===342&&cnt.E===134&&cnt.C===0&&new Set(DATA.map(r=>r[F.CODE])).size===746&&!DATA.some(r=>r[F.CODE]==='B006E'||r[F.CODE]==='B092E'),cnt);
   T('A-2 열 넷(SOL2·BSENT·BSRC·SYNPG) · 해설2 있는 기출 240 · 대기 12',F.SOL2===26&&F.SYNPG===29&&DATA.filter(r=>r[F.SOL2]).length===240&&DATA.filter(r=>r[F.BSRC]==='절시작·대기').length===12,[DATA.filter(r=>r[F.SOL2]).length,DATA.filter(r=>r[F.BSRC]==='절시작·대기').length]);
   T('A-2 단원 전부 있음(미분류 0) · BIGS 12장',DATA.every(r=>r[F.UNIT])&&BIGS.length===12&&BIGS[0].startsWith('1. 생물의 구성물질'),[BIGS.length,BIGS[0]]);
   T('목차 12장 45절 · TOC.unit 45(항목 = 절)',Object.keys(TOC.ch).length===12&&Object.keys(TOC.sec).length===45&&Object.keys(TOC.unit).length===45);
   buildTree();await wait(30);   /* ★ A-6(a) 9/30 — 셸 add9 §A-6(genie 68216cf): treeOpen 은 빈 함수(옛 목차 서랍 #tree 걷음 · 안 뜨는 것은 earth_shell WD-1 이 세 과목에서 잰다) — #trlist 내용(2단)은 buildTree 가 그대로 그린다(treePick·절 줄 📄 가 쓰는 살아 있는 함수) */
   T('트리 = 장 12 · 절 45 · 항목 줄 0(2단 · 같은 키 한 줄) · 미매칭 줄 0',$$('#trlist .trch').length===12&&$$('#trlist .trsec').length===45&&$$('#trlist .trit').length===0,[$$('#trlist .trch').length,$$('#trlist .trsec').length,$$('#trlist .trit').length]);
   treePick('3.4');await wait(30);
   T('트리 절 클릭 → 그 절 목록(기출만) = CSV',FL.unit==='3.4'&&filtered().length===EXP.u34,[filtered().length,EXP.u34]);
   FL.unit='';treeClose();draw();await wait(30);
   /* ===== A-3 필터 셋 ===== */
   const chipOf=lab=>$$('#fEtc .chip').find(c=>c.textContent.startsWith(lab));
   T('A-3 기본 필터 = 기출 270 · 칩 셋 기출·타기출·예상 · 확인문제 칩 없음',filtered().length===270&&FL.types.size===1&&!!chipOf('기출')&&!!chipOf('타기출')&&!!chipOf('예상')&&!chipOf('확인문제')&&!!$('#fEtc select'),filtered().length);
   chipOf('타기출').click();await wait(40);T('A-3 타기출 토글 → 612',filtered().length===612,filtered().length);
   chipOf('예상').click();await wait(40);T('A-3 예상 토글 → 746',filtered().length===746,filtered().length);
   chipOf('기출').click();await wait(40);T('A-3 기출 끄면 476 · 연도 칩 사라짐',filtered().length===476&&!$('#fEtc select'),filtered().length);
   chipOf('기출').click();chipOf('타기출').click();chipOf('예상').click();await wait(40);T('A-3 되돌리면 270',filtered().length===270&&FL.types.size===1);
   T('A-3 태그 셋 = 목록 첫 줄 tg 기출 · 클래스 tt·te 정의',!!$('#list .item .tag.tg')&&[...document.styleSheets].some(s=>{try{return [...s.cssRules].some(r=>r.selectorText&&r.selectorText.includes('.tag.tt'))}catch(e){return false}}));
   /* ===== A-4 선택지 4·5·7·8 ===== */
   const byUid=u=>DATA.find(r=>r[F.CODE]===u);
   const g5=DATA.find(r=>kindOf(r)==='G'&&(r[F.CH]||[]).filter(x=>x).length===5&&r[F.SOL]&&r[F.SOL2]&&(r[F.BOGI]||[]).some(b=>b.설명));
   await openView(g5[F.NO]);await wait(60);
   T('A-4 기출 5지선다 → 단추 5 · 제목 「YYYY년 자과 N번」',$$('#card .choices button').length===5&&/^\d{4}년 자과 \d+번$/.test(titleOf(g5)),[$$('#card .choices button').length,titleOf(g5)]);
   T('A-7 해설 탭 둘 크리티컬·SYNAPSE · 첫 탭 켜짐 · 둘째 숨김',$$('#card .soltabs button').map(b=>b.textContent).join()==='크리티컬,SYNAPSE'&&$('#card .soltabs button').classList.contains('on')&&$('#card .soltx[data-st="1"]').hidden===true);
   $$('#card .soltabs button')[1].click();await wait(20);
   T('A-7 SYNAPSE 탭 누르면 갈아 끼움',$('#card .soltx[data-st="1"]').hidden===false&&$('#card .soltx[data-st="0"]').hidden===true);
   T('A-7 보기 설명 = 해설 닫힘이면 숨김',$$('#card .bexp').length>0&&$$('#card .bexp').every(x=>x.hidden));
   $('#cDet').open=true;$('#cDet').dispatchEvent(new Event('toggle'));await wait(20);
   T('A-7 해설 열면 보기 밑 설명 보임',$$('#card .bexp').some(x=>!x.hidden&&getComputedStyle(x).display!=='none'));
   T('A-4 부록 쪽 칩 없음(SOLPG 는 크리티컬 쪽 · 교재 아님)',!$('#card summary').textContent.includes('부록')&&!$$('#card .jump .tag').some(x=>x.textContent.startsWith('부록')));
   const t4=byUid('B062T');await openView(t4[F.NO]);await wait(60);
   T('A-4 타기출 4지선다(B062T) → 단추 4 · 제목 「타기출 · 2018년 서울시」',$$('#card .choices button').length===4&&titleOf(t4)==='타기출 · 2018년 서울시',[$$('#card .choices button').length,titleOf(t4)]);
   T('A-7 타기출 해설 = SYNAPSE 하나(탭 없음 · 라벨)',$$('#card .soltabs').length===0&&$('#card .tag.sl')&&$('#card .tag.sl').textContent==='SYNAPSE');
   const t7=byUid('B203T');await openView(t7[F.NO]);await wait(60);$('#cDet').open=true;$('#cDet').dispatchEvent(new Event('toggle'));await wait(20);
   T('A-4 7지선다(B203T · 정답 ⑥) → 단추 7 · 정답 ⑥ 표시 · ⑥ 단추 ans',$$('#card .choices button').length===7&&$('#card .sol b').textContent==='정답 ⑥'&&$('#card .choices button[data-c="6"]').classList.contains('ans'),[$$('#card .choices button').length,$('#card .sol b').textContent]);
   const t8=byUid('B309T');await openView(t8[F.NO]);await wait(60);
   T('A-4 8지선다(B309T · 정답 ⑦) → 단추 8 · 정답 ⑦',$$('#card .choices button').length===8&&$$('#card .choices button')[7].textContent.startsWith('⑧')&&$('#card .sol b').textContent==='정답 ⑦',[$$('#card .choices button').length]);
   const e1=DATA.find(r=>kindOf(r)==='E');T('제목 예상 = 「예상 · SYNAPSE pNNN」',/^예상 · SYNAPSE p\d+$/.test(titleOf(e1)),titleOf(e1));
   const t285=byUid('B285T');await openView(t285[F.NO]);await wait(40);
   T('A-7 해설 없음(B285T) = 칩 「해설 없음」',!!$('#card .tag.nosol'));
   T('A-7 그림 193(문항.json 그림 칸) · IMG_DIR bio/img/',DATA.filter(r=>r[F.FILE]==='IMG').length===193&&CUR.IMG_DIR==='bio/img/',DATA.filter(r=>r[F.FILE]==='IMG').length);
   /* ===== A-5 「이 쪽의 문항」 = 교재쪽만 ===== */
   T('A-5 bookRows(163) = CSV 교재쪽 163 · SYNAPSE 문제쪽으로는 0',bookRows(163).length===EXP.p163&&bookRows(EXP.synpg).length===EXP.synpgN,[bookRows(163).length,EXP.p163,bookRows(EXP.synpg).length,EXP.synpgN]);
   /* ⚠ 2026-09-10 사용자 확정으로 **옆 교재 칸을 걷고 팝업 창 하나**로 갔다.
      옛 판은 `#bpc`·`#bpList`(옆 칸)를 쟀다. 같은 것을 교재 창에서 잰다. */
   await bookOpen(163);await wait(2600);
   {let n=0;while(n++<60&&(!bkCurPage()||bkCurPage().pr!==163))await wait(200);}
   $('#bkQ').click();await wait(400);
   T('A-5 교재 창 163쪽 → 4.1.pdf · 툴바에 PDF 번호 없음 · 목록 = 교재쪽',
     (pieceFor(163)||{}).file==='4.1.pdf'&&!!bkCurPage()&&bkCurPage().pr===163
     &&!/PDF/.test($('#bkInfo').textContent)&&$$('#bkqList [data-no]').length===EXP.p163,
     [(pieceFor(163)||{}).file,bkCurPage()&&bkCurPage().pr,$('#bkInfo').textContent,$$('#bkqList [data-no]').length]);
   $('#bkqX').click();await wait(100);
   const ok4=[];for(const [pg,file,k] of EXP.pages){await bookOpen(pg);await wait(2400);
     {let n=0;while(n++<60&&(!bkCurPage()||bkCurPage().pr!==pg))await wait(200);}
     ok4.push([pg,!!bkCurPage()&&bkCurPage().pr===pg&&(pieceFor(pg)||{}).file===file,(pieceFor(pg)||{}).file])}
   T('A-5 쪽 4곳 → 맞는 조각',ok4.every(x=>x[1]),ok4);
   bkClose();await wait(200);   /* 아래 §5 가 「닫힌 상태에서 열기」를 잰다 */
   /* ===== A-6 대기 배지 · bpg ===== */
   const waits=DATA.filter(bpgWait);
   T('A-6 「대기」 = 12(전부 기출 · 절시작·대기)',waits.length===12&&waits.every(r=>kindOf(r)==='G'),waits.length);
   const w=waits[0],wu=w[F.CODE],p0=w[F.BPAGE];await openView(w[F.NO]);await wait(60);
   T('A-6 카드 칩 📖 p + 「대기」 배지',$('#cBpg')&&$('#cBpg').textContent==='대기'&&$('#card .tag.page').textContent==='📖 p'+p0,[$('#cBpg')&&$('#cBpg').textContent]);
   $('#cBpg').click();await wait(300);
   T('A-6 팝업 = 그 절의 교재 문장 목록(【연도】 p쪽) + 쪽 직접',!!$('#bpgSheet')&&$$('#bpgSheet .bpgl [data-i]').length>0&&/^【\d{4}】 p\d+/.test($('#bpgSheet .bpgl [data-i] b').textContent)&&!!$('#bpgP'),[$$('#bpgSheet .bpgl [data-i]').length]);
   const first=$('#bpgSheet .bpgl [data-i]'),pSel=+first.dataset.p;first.click();await wait(80);
   T('A-6 고르면 kv bpg[uid]={ps,last,s}(판 1: 새 꼴로만 쓴다) · 칩 ✓ · 배지 없어짐 · 팝업 닫힘',BPG[wu]&&JSON.stringify(BPG[wu].ps)===JSON.stringify([pSel])&&BPG[wu].last===pSel&&typeof BPG[wu].s==='number'&&(((await get('kv','bpg'))||{})[wu]||{}).last===pSel&&$('#cBpg').textContent==='✓'&&!bpgWait(rec(w[F.NO]))&&!$('#bpgSheet'),BPG[wu]);
   T('A-6 교재 패널 「이 쪽의 문항」에 반영',bookRows(pSel).some(r=>r[F.CODE]===wu)&&(pSel===p0||!bookRows(p0).some(r=>r[F.CODE]===wu)));
   $('#cBpg').click();await wait(200);$('#bpgP').value='999';$('#bpgAdd').click();await wait(80);
   T('A-6 쪽 번호로 999 ＋고정 → ps 에 더해지고 last=999 · 칩 「📖 p999 +1」(판 1: 갈아치우기가 아니라 더하기 · 빼기는 ✕)',BPG[wu]&&BPG[wu].ps.indexOf(999)>=0&&BPG[wu].ps.indexOf(pSel)>=0&&BPG[wu].last===999&&$('#card .tag.page').textContent==='📖 p999 +1',[BPG[wu],$('#card .tag.page').textContent]);
   $('#cBpg').click();await wait(200);$('#bpgAuto').click();await wait(80);
   T('A-6 「자동값으로 되돌림」 → kv 삭제 · 배지 「대기」 복귀',!BPG[wu]&&!((await get('kv','bpg'))||{})[wu]&&$('#cBpg').textContent==='대기');
   /* ★ A-6(a) 9/30 — 셸 이식(genie c9faff2 · _task_jagwa_shell_bio_phys.md §E-7): 생물 SYNC_KEYS 뒤에 gg·ggref·pick·link 넷(24) — 옛 20키 앞자리 그대로(순서 보존) · 키가 더 늘어도 안 뒤집힌다 */
   T('A-8 SYNC_KEYS 앞 20 그대로(add1 +bref · 셸 +gg·ggref·pick·link 는 뒤에) · 15째 bpg · SYNC_REF.bpg',SYNC_KEYS.slice(0,20).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,snote,crop,txt,tfix,bref'&&SYNC_KEYS[14]==='bpg'&&SYNC_KEYS[13]==='bpit'&&typeof SYNC_REF.bpg.g==='function'&&SYNC_REF.bpg.g()===BPG);
   const snap=JSON.parse(JSON.stringify(BPG));SYNC_REF.bpg.s({[wu]:{p:5}});await wait(10);
   T('A-8 받기(s) → BPG 갈아 끼움 · bpgOf 반영',BPG[wu].p===5&&bpgOf(rec(w[F.NO]))===5);SYNC_REF.bpg.s(snap);await wait(10);T('A-8 되돌림',!BPG[wu]);
   T('A-8 지학 unit 매칭 팝업도 산다(✎ 칩 → matchSheet)',typeof matchSheet==='function'&&!!$('#cMatch'));
   /* ===== §5 교재 모드 ===== */
   $('#btnBook').click();await wait(1800);
   T('§5 📖 교재 모드 열림 · 조각 받음 · 목차 서랍 2단(장 12 · 절 = 항목 45 · 절 머리 0)',BK.open&&BK.pgs.length>0&&$$('#bklist .bkch').length===12&&$$('#bklist .bkit').length===45&&$$('#bklist .bksec').length===0,[BK.pgs.length,$$('#bklist .bkch').length,$$('#bklist .bkit').length,$$('#bklist .bksec').length,$('#bkmsg').textContent]);
   await bkGoto(163);await wait(600);const cp=bkCurPage();
   T('§5 163쪽 → 4.1.pdf · 툴바 「4.1 · 163쪽」(PDF 번호 없음) · 문항 수 = 교재쪽 163',cp&&cp.pr===163&&cp.pc.file==='4.1.pdf'&&$('#bkInfo').textContent==='4.1 · 163쪽'&&+$('#bkQn').textContent===EXP.p163&&!!$('#bklist .bkit.cur'),[cp&&cp.pr,cp&&cp.pc.file,$('#bkInfo').textContent,$('#bkQn').textContent]);
   T('§5 PIECES 45 · localStorage bio_book · IndexedDB pdf 캐시',Object.keys(PIECES).length===45&&!!localStorage.getItem('bio_book')&&!!(await get('pdf','4.1.pdf')));
   $('#bkQ').click();await wait(200);T('§5 「문항 N」 팝업 = bookRows',$$('#bkqList [data-no]').length===EXP.p163);$('#bkqX').click();
   bkClose();await wait(50);T('§5 닫힘',!BK.open&&$('#book').classList.contains('hide'));
   T('§5 서브노트 = notes 저장소 bio/ (빈 판 · 정리판은 판 2)',CUR.NOTE_PATH==='bio/'&&(await notePath(1)).path==='bio/서브노트_1.pdf',await notePath(1));
   /* ===== 판 2 · 정리판 · 줄에 붙이는 층 snote · 수정 큐 · 앱 이름 (_task_bio_app_pan2.md §B + add2~add4 · §C-3~C-5) ===== */
   T('P2-0 add4 앱 이름 = <title> 자과 서재 · 머리 「자과 서재 · 생물」 · SUBJ.bio.TITLE/LOG/NAME 무변',document.title==='자과 서재'&&$('.brand h1').textContent==='자과 서재 · 생물'&&SUBJ.bio.TITLE==='생물 기출 서재'&&SUBJ.bio.LOG==='생물'&&CUR.NAME==='생물');
   /* ★ A-6(a) 9/30 — A-8 과 같은 까닭(c9faff2 §E-7 · 생물 +gg·ggref·pick·link = 24) — 옛 20키 앞자리 그대로 */
   T('P2-1 SYNC_KEYS 앞 20 그대로(add1 +bref · 셸 +gg·ggref·pick·link 는 뒤에) · 16째 snote · SYNC_REF.snote · SN 전역 · NOTE_JSON · 층 켜짐',SYNC_KEYS.slice(0,20).join()==='status,note,qtype,conc,gpt,twin,ansfix,frm,maskpos,omrpos,mcard,bogi,unit,bpit,bpg,snote,crop,txt,tfix,bref'&&SYNC_KEYS[15]==='snote'&&SYNC_KEYS[16]==='crop'&&SYNC_KEYS[17]==='txt'&&SYNC_KEYS[18]==='tfix'&&SYNC_KEYS[19]==='bref'&&SYNC_REF.snote.g()===SN&&CUR.NOTE_JSON==='bio/정리판/'&&SN_ON===true&&typeof ghRawRepo==='function');
   T('P2-2 지학 19(add1 +bref) · 물리 12 무변(9/5 필터 손질 +link) · 정리판 층은 NOTE_JSON 있는 과목만',SUBJ.earth.SYNC_KEYS.length===19&&SUBJ.earth.SYNC_KEYS[14]==='bpg'&&SUBJ.earth.SYNC_KEYS[15]==='crop'&&SUBJ.earth.SYNC_KEYS[16]==='txt'&&SUBJ.earth.SYNC_KEYS[17]==='tfix'&&SUBJ.earth.SYNC_KEYS[18]==='bref'&&SUBJ.earth.NOTE_JSON===undefined&&SUBJ.phys.NOTE_JSON===undefined&&SUBJ.phys.SYNC_KEYS.length===12);
   await snIndex(true);T('P2-3 index.json 받음 · 1.1 있음 · snHas 1.1=true · 9.9=false',!!SNOTE.idx&&!!SNOTE.idx['1.1']&&snHas('1.1')===true&&snHas('9.9')===false,SNOTE.idx);
   const q11=DATA.find(r=>kindOf(r)==='G'&&secOf(unitOf(r[F.NO]))==='1.1');await openView(q11[F.NO]);await wait(60);
   T('P2-4 카드 절 칩 「📄 정리판」(1.1)',!!$('#cSn')&&$('#cSn').textContent==='📄 정리판'&&$('#cSn').dataset.sec==='1.1',[$('#cSn')&&$('#cSn').textContent]);
   $('#cSn').click();await wait(1500);
   const ws=$('#snworld'),svp=$('#snvp');
   T('P2-5 창 열림(떠 있는 창 · makeFloat) · 1.1 · 80줄 · 폭 1180 · 줄마다 data-lid',SNOTE.open&&!$('#snw').classList.contains('hide')&&$('#snw').classList.contains('sheet')&&SNOTE.sec==='1.1'&&SNOTE.doc.줄.length===80&&ws.offsetWidth===1180&&$$('#snworld [data-lid]').length===80&&!!$('#snw .twgrip'),[SNOTE.doc&&SNOTE.doc.줄.length,ws.offsetWidth,$$('#snworld [data-lid]').length]);
   T('P2-5 처음 열면 폭 맞춤 · 팬/줌 = Z 엔진(zWire · 타일 없음 ready:false)',Math.abs(SNZ.S-(svp.clientWidth-16)/1180)<0.001&&SNZ.ready===false&&typeof SNZ.toPage==='function'&&typeof SNZ.stop==='function',[SNZ.S,svp.clientWidth]);
   const s0z=SNZ.S,vr=svp.getBoundingClientRect();svp.dispatchEvent(new WheelEvent('wheel',{deltaY:-300,ctrlKey:true,clientX:vr.left+200,clientY:vr.top+200,bubbles:true,cancelable:true}));await wait(60);
   T('P2-5 Ctrl+휠 → 확대 · 맨 휠 = 이동',SNZ.S>s0z&&(()=>{const y0=SNZ.Y;svp.dispatchEvent(new WheelEvent('wheel',{deltaY:120,clientX:vr.left+200,clientY:vr.top+200,bubbles:true,cancelable:true}));return SNZ.Y<y0})(),[s0z,SNZ.S]);snFit();
   T('P2-5 줄바꿈 0(scrollWidth ≤ 1180 · white-space:pre) · 1단',ws.scrollWidth<=1181&&$$('#snworld .snl').every(el=>el.scrollWidth<=1181)&&getComputedStyle(ws).whiteSpace==='pre'&&$$('#snworld .snl').every(el=>getComputedStyle(el).display==='block'),[ws.scrollWidth]);
   const col=sel=>{const el=$('#snworld '+sel);return el?getComputedStyle(el).color:''};
   T('P2-5 색 셋 = 파랑 #2F6FD0 · 빨강 #D93B3B · 진분홍 #C2557C · 회색 #7C8794 · 초록 #3B9C6B · 청록 #2E7D6F · 뒤판 분홍/노랑 · 연도칩 7',col('.cb')==='rgb(47, 111, 208)'&&col('.cr')==='rgb(217, 59, 59)'&&col('.cp')==='rgb(194, 85, 124)'&&col('.cm')==='rgb(124, 135, 148)'&&col('.cg')==='rgb(59, 156, 107)'&&col('.ct')==='rgb(46, 125, 111)'&&getComputedStyle($('#snworld .hlp')).backgroundColor==='rgb(251, 213, 228)'&&getComputedStyle($('#snworld .hly')).backgroundColor==='rgb(255, 243, 163)'&&$$('#snworld .snchip').length===7,[col('.cb'),col('.cr'),col('.cp'),$$('#snworld .snchip').length]);
   T('P2-5 표 3(4색 머리 1 · 흰 글자 셀 1 · 행 36 · 레인 왼/오른) · 상자 9 · 구분선 2 · 꼬리 접힘 · 라벨 줄 8 · 경고 2',$$('#snworld .sntb').length===3&&$$('#snworld .sntb.h4').length===1&&$$('#snworld .sntr').length===36&&$$('#snworld .sntd.hd.cw').length===1&&$$('#snworld .snlane.l').length===8&&$$('#snworld .snlane.r').length===5&&$$('#snworld .snbox').length===9&&$$('#snworld .snl.sep').length===2&&!!$('#snworld details.snfold')&&!$('#snworld details.snfold').open&&$$('#snworld .snl.k-라벨').length===8&&$$('#snworld .snl.k-경고').length===2,[$$('#snworld .sntb').length,$$('#snworld .sntr').length,$$('#snworld .snlane.l').length,$$('#snworld .snlane.r').length,$$('#snworld .snbox').length]);
   T('P2-5 열폭 = @열폭(큰 표 188/134/134/138/104 · x 196) · 작은 표 x 100(±1 = 표 테두리)',(()=>{const r=$$('#snworld .sntb.h4 .sntr')[1];const c=[...r.children].filter(x=>x.classList.contains('sntd')).map(x=>Math.round(x.getBoundingClientRect().width/SNZ.S));const x0=(r.closest('.sntb').getBoundingClientRect().left-ws.getBoundingClientRect().left)/SNZ.S;const t1=$('#snworld .sntb');const x1=(t1.getBoundingClientRect().left-ws.getBoundingClientRect().left)/SNZ.S;return c.join()==='188,134,134,138,104'&&Math.abs(x0-196)<=1&&Math.abs(x1-100)<=1})(),[[...$$('#snworld .sntb.h4 .sntr')[1].children].map(x=>Math.round(x.getBoundingClientRect().width/SNZ.S)),$('#snworld .sntb.h4').getBoundingClientRect().left-ws.getBoundingClientRect().left,$('#snworld .sntb').getBoundingClientRect().left-ws.getBoundingClientRect().left]);
   T('P2-5 다크 = CSS 변수(--sn-*) 로만 색을 잡는다(변수만 갈아 끼우면 된다)',getComputedStyle(document.documentElement).getPropertyValue('--sn-blue').trim()==='#2F6FD0'&&getComputedStyle(document.documentElement).getPropertyValue('--sn-paper').trim()==='#FFFFFF');
   /* 줄 길게 누르기 → 시트 → 메모 */
   const PE2=(t,el,x,y)=>el.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:9,pointerType:'touch',bubbles:true,cancelable:true,isPrimary:true}));
   const L5=$('#snworld [data-lid="1.1-0005"]');const r5=L5.getBoundingClientRect();
   PE2('pointerdown',L5,r5.left+40,r5.top+r5.height/2);await wait(650);PE2('pointerup',L5,r5.left+40,r5.top+r5.height/2);
   T('P2-6 줄 길게 누르기(500ms) → 시트 #snsheet(줄 id · 메모/수정/링크/그림) · 창 위(z 90)',!!$('#snsheet')&&/1\.1-0005/.test($('#snsheet h2').textContent)&&!!$('#snMemo')&&!!$('#snFixB')&&!!$('#snLink')&&!!$('#snImg')&&+getComputedStyle($('#snsheet')).zIndex>+getComputedStyle($('#snw')).zIndex,$('#snsheet')&&$('#snsheet h2').textContent);
   $('#snT').value='검산 메모';$('#snMemo').click();await wait(150);
   T('P2-6 메모 저장 → SN[lid]=[{k:memo}] · kv snote · 줄 밑 접힌 띠 · 오른쪽 표시 ✎',!!SN['1.1-0005']&&SN['1.1-0005'].length===1&&SN['1.1-0005'][0].k==='memo'&&SN['1.1-0005'][0].v==='검산 메모'&&!!((await get('kv','snote'))||{})['1.1-0005']&&!!$('#snworld [data-lid="1.1-0005"] + .snband')&&!$('#snworld [data-lid="1.1-0005"] + .snband').classList.contains('open')&&$('#snworld [data-lid="1.1-0005"] .snmk').textContent.includes('✎')&&!$('#snsheet'),SN['1.1-0005']);
   $('#snworld .snband').click();await wait(30);T('P2-6 띠 탭 → 펼침(메모 글)',$('#snworld .snband').classList.contains('open')&&$('#snworld .snband .sni.memo').textContent.includes('검산 메모'));
   const L5b=$('#snworld [data-lid="1.1-0005"]'),r5b=L5b.getBoundingClientRect();   /* 저장 뒤 창이 다시 그려졌으니 줄 요소를 다시 잡는다 */
   PE2('pointerdown',L5b,r5b.left+40,r5b.top+r5b.height/2);PE2('pointermove',L5b,r5b.left+70,r5b.top+r5b.height/2);await wait(650);PE2('pointerup',L5b,r5b.left+70,r5b.top+r5b.height/2);
   T('P2-6 8px 넘게 움직이면 시트 안 뜸',!$('#snsheet'));
   L5b.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true,clientX:r5b.left+40,clientY:r5b.top+5}));await wait(30);
   T('P2-6 PC 우클릭 → 같은 시트(붙어 있는 것 1)',!!$('#snsheet')&&$$('#snsheet .snlist div').length===1);$('#snSX').click();
   /* 강제 받기 왕복 = SYNC_REF.snote.s · fix 배지 · 절 머리 「수정 N」 · 채팅이 done:true */
   const snap6=JSON.parse(JSON.stringify(SN));SYNC_REF.snote.s({'1.1-0009':[{k:'fix',v:'표 첫 행 오타',t:1}],'1.1-0005':[{k:'memo',v:'원격 메모',t:2}]});await wait(80);
   T('P2-7 받기(s) → SN 갈아 끼움 · 창 다시 그림 · fix 줄 노란 배지 · 머리 「수정 1」',SN['1.1-0009'][0].k==='fix'&&$('#snworld [data-lid="1.1-0009"]').classList.contains('fix')&&$('#snFix').textContent==='수정 1'&&$('#snworld [data-lid="1.1-0009"] .snmk b').textContent==='수정'&&$('#snworld .snband .sni.memo').textContent.includes('원격 메모'),[$('#snFix').textContent]);
   SYNC_REF.snote.s({'1.1-0009':[{k:'fix',v:'표 첫 행 오타',t:1,done:true}]});await wait(80);
   T('P2-7 채팅이 done:true 로 닫으면 「반영됨」 · 수정 0 · 지우기 단추',!$('#snworld [data-lid="1.1-0009"]').classList.contains('fix')&&$('#snFix').textContent===''&&$$('#snworld .sni.fix.done').length===1&&!!$('#snworld .sni.fix.done button[data-act="del"]'));
   $('#snworld .sni.fix.done button[data-act="del"]').click();await wait(100);
   T('P2-7 지우기 → SN 비움 · kv',!SN['1.1-0009']&&!((await get('kv','snote'))||{})['1.1-0009']);
   SYNC_REF.snote.s(snap6);await wait(40);
   /* 그림 PUT(모의) · 링크 → 문항 카드 · 다른 절 · 교재쪽 */
   const cvI=document.createElement('canvas');cvI.width=1600;cvI.height=400;cvI.getContext('2d').fillRect(0,0,1600,400);const blobI=await new Promise(r=>cvI.toBlob(r,'image/png'));
   await snImgAdd('1.1-0005',new File([blobI],'x.png',{type:'image/png'}));await wait(150);
   const im=SN['1.1-0005'].find(x=>x.k==='img');
   T('P2-8 그림 → 폭 1180 이하 JPEG · notes bio/att/<sha8>.jpg PUT(모의 · 서브노트 올리기 통로) · 항목 · 캐시 · <img>',!!im&&/^att\/[0-9a-f]{8}\.jpg$/.test(im.v)&&window.__puts.includes('bio/'+im.v)&&!!(await get('pdf','snatt:'+im.v))&&!!$('#snworld .sni.img img'),[im,window.__puts]);
   const bmpChk=await createImageBitmap(new Blob([await get('pdf','snatt:'+im.v)],{type:'image/jpeg'}));T('P2-8 저장 그림 폭 = 1180',bmpChk.width===1180,bmpChk.width);
   const tgt=DATA.find(r=>r[F.NO]!==VNO&&kindOf(r)==='G');await snAdd('1.1-0005',{k:'link',v:{q:tgt[F.CODE],p:163,s:'9.9'}});await wait(60);
   $('#snworld .snband').classList.add('open');$('#snworld .snlk[data-act="q"]').click();await wait(200);
   T('P2-9 링크 문항 칩 → 그 문항 카드(openView) · 정리판 창은 떠 있는 채',VNO===tgt[F.NO]&&!$('#view').classList.contains('hide')&&SNOTE.open,[VNO,tgt[F.NO]]);
   $('#snworld .snlk[data-act="s"]').click();await wait(800);
   T('P2-10 없는 절(9.9) → 「아직 없음」 · SNOTE.has 9.9=false · 캐시 없음',SNOTE.sec==='9.9'&&SNOTE.doc===null&&/아직 없음/.test($('#snworld').textContent)&&SNOTE.has['9.9']===false&&!(await get('kv','snote:9.9')),[SNOTE.sec,$('#snworld').textContent.slice(0,40)]);
   await snOpen('1.1');await wait(300);T('P2-10 다시 1.1 (캐시 kv snote:1.1 · doc.sha)',SNOTE.doc&&SNOTE.doc.절==='1.1'&&!!(await get('kv','snote:1.1'))&&typeof SNOTE.doc.sha==='string');
   $('#snworld .snband').classList.add('open');$('#snworld .snlk[data-act="p"]').click();await wait(1500);
   T('P2-9 링크 교재쪽 칩 → 교재 모드 163쪽',BK.open&&bkCurPage()&&bkCurPage().pr===163,bkCurPage()&&bkCurPage().pr);
   $('#bkSn').click();await wait(700);
   T('P2-11 교재 모드 툴바 「📄 정리판」 → 이 쪽 절(4.1) = 아직 없음',!!$('#bkSn')&&SNOTE.sec==='4.1'&&SNOTE.doc===null,[SNOTE.sec]);bkClose();await wait(50);
   treeOpen();await wait(30);T('P2-12 목차 서랍 절 줄 📄 45 · 1.1 만 살아 있음(index) · 1.2 흐림',$$('#trlist .snt').length===45&&!$('#trlist .snt[data-sn="1.1"]').classList.contains('none')&&$('#trlist .snt[data-sn="1.2"]').classList.contains('none'),$$('#trlist .snt').length);
   $('#trlist .snt[data-sn="1.1"]').click();await wait(400);T('P2-12 📄 → 정리판 1.1 · 서랍은 그대로',SNOTE.sec==='1.1'&&!!SNOTE.doc&&!$('#navdr').classList.contains('hide'));   /* ★ A-6(a) 9/30 — 셸 add9 §A(68216cf): 서랍 = 첫 화면 왼쪽 상주 서랍 #navdr(옛 #tree 는 걷어 늘 숨음) */
   /* 필터 add1(9/5): 생물 서랍에도 공통 손잡이 #trGrip — 탭 접기 · 끌기 · 여백
      ★ A-6(a) 9/30 — 셸 add9 §A(68216cf): 옛 #tree(#trGrip · SET.tro/trw · body.tropen)는 걷었고 그 구실은 상주 서랍 #navdr 이 맡는다 —
      #ndGrip 탭 = 접기(13px) · 끌기 = 너비(160~420 · 기본 236) · 기기별 localStorage jagwa.nd.fold/w.<과목> · 놓으면 SET.ndw · 여백 body.ndon = --ndw → 같은 세 동작을 그 손잡이로 잰다 */
   {const gB=$('#ndGrip'),dB=$('#navdr');const PEB=(t,x,y)=>gB.dispatchEvent(new PointerEvent(t,{clientX:x,clientY:y,pointerId:6,pointerType:'mouse',bubbles:true,cancelable:true,isPrimary:true}));
    T('A1 생물 상주 서랍 #ndGrip 손잡이 · body.ndon 여백 236',!!gB&&document.body.classList.contains('ndon')&&getComputedStyle(document.body).paddingLeft==='236px',[!!gB,getComputedStyle(document.body).paddingLeft]);
    PEB('pointerdown',265,200);await wait(10);PEB('pointerup',266,201);await wait(60);T('A1 생물 탭 → 접힘 13 · jagwa.nd.fold.bio',dB.classList.contains('fold')&&Math.round(dB.getBoundingClientRect().width)===13&&localStorage.getItem('jagwa.nd.fold.bio')==='1',[dB.getBoundingClientRect().width,localStorage.getItem('jagwa.nd.fold.bio')]);
    PEB('pointerdown',5,200);await wait(10);PEB('pointerup',6,201);await wait(60);PEB('pointerdown',265,200);await wait(10);PEB('pointermove',365,200);await wait(10);PEB('pointerup',365,200);await wait(60);
    T('A1 생물 끌기 +100 → 336 · SET.ndw · 서랍 줄(절 45 · 📄) 무변',!dB.classList.contains('fold')&&Math.round(dB.getBoundingClientRect().width)===336&&SET.ndw===336&&$$('#trlist .trsec').length===45&&$$('#trlist .snt').length===45,[dB.getBoundingClientRect().width,SET.ndw]);
    ndSetW(236);delete SET.ndw;await put('kv','set',SET);}
   treeClose();
   await openView(q11[F.NO]);await wait(60);T('P2-4 없는 절 카드 칩 = 「📄 아직 없음」',(()=>{const r=DATA.find(x=>secOf(unitOf(x[F.NO]))==='1.2');return !!r&&snChip(r).includes('아직 없음')})());
   /* 백업/복원에 snote(+카드 층 키) */
   const ex2=await (async()=>{let got=null;const a0=HTMLAnchorElement.prototype.click;HTMLAnchorElement.prototype.click=function(){got=this.href};try{await exportData(false)}finally{HTMLAnchorElement.prototype.click=a0}return got?JSON.parse(await (await __nativeFetch(got)).text()):null})();
   T('P2-13 백업에 card.snote(+bogi·unit·bpit·bpg·mcard) 실림 · 이름 생물_',!!ex2&&!!ex2.card&&JSON.stringify(ex2.card.snote)===JSON.stringify(SN)&&'bpg' in ex2.card&&'bogi' in ex2.card,ex2&&Object.keys(ex2.card||{}));
   const snKeep=JSON.parse(JSON.stringify(SN));SN={};await put('kv','snote',SN);await importData(new Blob([JSON.stringify(ex2)],{type:'application/json'}));await wait(150);
   T('P2-13 복원 → snote 되살아남 · kv',JSON.stringify(SN)===JSON.stringify(snKeep)&&JSON.stringify((await get('kv','snote'))||{})===JSON.stringify(snKeep));
   delete SN['1.1-0005'];await saveSN();snClose();await wait(30);
   T('P2-14 창 닫힘 · .sheet 벗음(물리 키 1~4 차단 해제)',!SNOTE.open&&$('#snw').classList.contains('hide')&&!$('#snw').classList.contains('sheet'));
   T('E-9 JS 오류 0',(window.__err||[]).length===0,window.__err);
   T('기록 PUT 없음(검산 중 원격 무접촉 · 정리판 그림 모의 PUT bio/att/ 1 뿐)',window.__puts.length===1&&window.__puts.every(p=>p.startsWith('bio/att/')),window.__puts);
  }catch(e){R.push('FAIL | 예외 | '+(e&&e.stack||e))}
  await __nativeFetch('/result',{method:'POST',body:R.join(String.fromCharCode(10))});
 }
 (function boot(n){
  if(typeof loadEarthData==='function'&&typeof db!=='undefined'&&db&&typeof recPaint==='function'&&document.getElementById('recChip').textContent)return setTimeout(run,300);
  if(n>600)return;
  setTimeout(()=>boot(n+1),25);
 })(0);
})();
</script>
"""

def main():
    phone = 'phone' in sys.argv[1:]; subj = os.environ.get('PHONE_SUBJ', 'bio')
    html = open(SRC, encoding='utf-8', newline='').read()
    html = html.replace('<script defer src="https://cdnjs', '<script defer data-off="https://cdnjs')
    html = html.replace('<link rel="stylesheet" href="https://cdnjs', '<link rel="off" href="https://cdnjs')
    html = html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', E.STUB.replace("localStorage.setItem('subj','earth')", "localStorage.setItem('subj','%s')" % (subj if phone else 'bio')) + '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js', 1)
    rows = list(csv.DictReader(open(os.path.join(SAENG, '_생물_문항.csv'), encoding='utf-8-sig')))
    idx = json.load(open(os.path.join(SPD, 'pdf', 'index.json'), encoding='utf-8'))
    def loc(p):
        for k, v in idx.items():
            if v['인쇄시작'] <= p <= v['인쇄끝']: return [p, v['file'], p - v['pdf_offset']]
    synpg = int(next(r['문제쪽'] for r in rows if r['uid'] == 'T001'))
    exp = {'u34': sum(1 for r in rows if r['유형'] == '기출' and r['단원'] == '3.4'),
           'p163': sum(1 for r in rows if r['교재쪽'] == '163'),
           'synpg': synpg, 'synpgN': sum(1 for r in rows if r['교재쪽'] == str(synpg)),
           'pages': [loc(p) for p in (2, 163, 205, 462)]}
    # 폰 꼴(판 2 §B-5-1): 생물이면 정리판 창이 전체 화면 · 폭 맞춤 배율 < 1 · 닫힘 — 지학 폰 검사(E.TESTS_PHONE) 뒤에 한 항 얹는다
    PHONE_EXTRA = r"""if(SUBJ_ID==='bio'&&typeof snOpen==='function'){await snOpen('1.1');await wait(1500);const pr=$('#snw .panel').getBoundingClientRect();
   const de=document.documentElement;   /* 헤드리스 iframe 은 고전 스크롤바 15px 이 있어 layout 뷰포트(clientWidth) 로 잰다 · 실기기는 겹침 스크롤바 0 */
   T('P2 폰 정리판 창 = 전체 화면(layout 뷰포트 · 390×844 − 스크롤바) · 폭 맞춤 배율 <1 · 80줄',Math.abs(pr.width-de.clientWidth)<2&&Math.abs(pr.height-de.clientHeight)<2&&pr.left===0&&pr.top===0&&SNZ.S<1&&SNZ.S>0.2&&$$('#snworld [data-lid]').length===80,[pr.width,pr.height,de.clientWidth,de.clientHeight,innerWidth,innerHeight,SNZ.S,pr.left,pr.top,$$('#snworld [data-lid]').length,SNOTE.sec,!!SNOTE.doc,$('#snInfo').textContent]);
   T('P2 폰 제목 「자과 서재 · 생물」 한 줄(줄바꿈 없음)',$('.brand h1').textContent==='자과 서재 · 생물'&&$('.brand h1').getBoundingClientRect().height<26,[$('.brand h1').getBoundingClientRect().height]);snClose()}
   """
    # 지학 폰 검사의 가짜 GitHub 는 notes 요청도 /data/ 로 보낸다 → 정리판 JSON(notes) 은 /notes/ 로(데스크톱 TESTS 와 같은 규칙)
    PHONE_TESTS = E.TESTS_PHONE.replace("  const path=decodeURIComponent(m[2]);\n  if((opt.method||'GET')==='PUT')",
        "  const path=decodeURIComponent(m[2]);\n  if(m[1]==='zzikkaplan/notes'&&(opt.method||'GET')!=='PUT'){const r=await __nativeFetch('/notes/'+encodeURI(path),{cache:'no-store'});return r.ok?r:{ok:false,status:404,json:async()=>({}),text:async()=>'',arrayBuffer:async()=>new ArrayBuffer(0)}}\n  if((opt.method||'GET')==='PUT')")
    assert PHONE_TESTS != E.TESTS_PHONE, '폰 검사 가짜 GitHub 앵커를 못 찾음'
    html = html.replace('</body>', (PHONE_TESTS.replace("T('JS 오류 0'", PHONE_EXTRA + "T('JS 오류 0'") if phone else TESTS).replace('__EXP__', json.dumps(exp, ensure_ascii=False)) + '</body>', 1)
    open(APP, 'w', encoding='utf-8', newline='').write(html)
    open(os.path.join(OUT, 'phone.html'), 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><body style="margin:0;background:#888"><iframe src="app.html" style="width:390px;height:844px;border:0"></iframe></body>')

    done = threading.Event(); box = {}
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=OUT, **k)
        def log_message(self, *a, **k): pass
        def do_GET(self):
            p = urllib.parse.unquote(self.path.split('?')[0])
            if p.startswith('/notes/'):
                f = os.path.join(os.path.expanduser('~'), 'Documents', 'notes', p[7:].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read(); self.send_response(200); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b); return
            if p.startswith('/data/'):
                rel = p[6:]
                base = SPD if rel.startswith('bio/') else (E.SPD if rel.startswith('earth/') else None)
                if not base: self.send_response(404); self.end_headers(); return
                f = os.path.join(base, rel.split('/', 1)[1].replace('/', os.sep))
                if not os.path.isfile(f): self.send_response(404); self.end_headers(); return
                b = open(f, 'rb').read()
                self.send_response(200); self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', str(len(b))); self.send_header('X-Sha', hashlib.sha1(b).hexdigest()); self.end_headers()
                self.wfile.write(b); return
            return super().do_GET()
        def do_POST(self):
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n).decode('utf-8', 'replace'); self.send_response(204); self.end_headers()
            if self.path.startswith('/partial'): box['partial'] = body; return
            box['txt'] = body; done.set()
    srv = socketserver.ThreadingTCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    prof = os.path.join(OUT, 'prof'); shutil.rmtree(prof, ignore_errors=True)
    p = subprocess.Popen([chrome, '--headless=new', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof, '--window-size=1400,900',
                          'http://127.0.0.1:%d/%s' % (port, 'phone.html' if phone else 'app.html')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import time as _t; _t0 = _t.time(); got = done.wait(int(os.environ.get('HARNESS_WAIT', '600'))); p.terminate(); print('elapsed %.0fs' % (_t.time() - _t0))
    try: p.wait(10)
    except Exception: p.kill()
    srv.shutdown()
    if not got: print('결과 없음 — 시간 안에 검사가 끝나지 않았다 · 마지막 중간 결과:'); print(box.get('partial', '(없음)')); sys.exit(1)
    lines = [ln for ln in box['txt'].replace('\r', '').split('\n') if ln.strip()]
    if phone:
        npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
        for x in lines: print(x)
        print('\n== 폰(%s) %d PASS / %d FAIL / %d항 ==' % (subj, npass, nfail, len(lines))); sys.exit(0 if nfail == 0 else 2)
    def T2(name, cond, info=''): lines.append(('PASS' if cond else 'FAIL') + ' | ' + name + ('' if cond else ' | ' + str(info)))
    s = open(SRC, encoding='utf-8').read()
    samples = [r['문항'][:18] for r in rows if len(r['문항']) > 30][:5] + [r['해설'][:18] for r in rows if len(r['해설']) > 30][:3]
    T2('D11 앱에 생물 본문 문자열 0(표본 8)', not any(x in s for x in samples), [x for x in samples if x in s])
    T2('배달 pdf 45 · 25MB 초과 0 · img 196', len(idx) == 45 and all(os.path.getsize(os.path.join(SPD, 'pdf', v['file'])) < 25 * 1048576 for v in idx.values()) and len([f for f in os.listdir(os.path.join(SPD, 'img')) if f.endswith('.jpg') and not f.startswith('ref')]) == 196)   # ★ A-6(d) 9/30 — 참고 그림 ref*.jpg 39 는 bio_ocrfix(studyplandata 550ee2e5 · 9/25)가 같은 폴더에 더한 것 · 문항 그림은 196 그대로
    T2('백틱 짝', s.count('`') % 2 == 0)
    lay = s[s.index('/*EARTH:js*/'):s.index('/*/EARTH:js*/')]
    T2('층 안 EARTH.·earthdata·bio/ 하드코딩 0 · 층 머리 가드 = if(SHELL)(셸 세 과목 · 카드 몫은 if(HASBOOK))', 'EARTH.' not in lay and "'earthdata'" not in lay and "'bio/" not in lay and lay.split('\n')[2] == 'if(SHELL){')   # ★ A-6(a) 9/30 — 셸 이식(c9faff2): 층 머리 if(CARD_LAYER){ → if(SHELL){
    T2('A-9 물리 F 16 무변 · CIRC5 자리 값 무변 · SUBJ.phys 무변(9/5 필터 손질: SYNC_KEYS 12째 link 반영)', 'const F={NO:0,PG:1,FILE:2,FPG:3,BIG:4,SUB:5,LNO:6,STAR:7,TYPE:8,CODE:9,YEAR:10,SRC:11,LV:12,ANS:13,BODY:14,VLT:15};' in s and s.count("const CIRC5='①②③④⑤';") == 1 and "phys:{DB:'phys535', PDF_DIR:'phys/pdf/', REC_PATH:'phys/기록.json', SYNC_PREFIX:'phys_sync_',\n        SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','link'],   /* 2026-09-05 필터 손질 B-4: link = 「연결」(한 방향 · 12째) */\n        TITLE:'물리 535 서재', LOG:'물리535', DATA:'인라인 DATA', NAME:'물리', ready:true}," in s.replace('\r\n', '\n'))
    T2('A-9 SUBJ.earth = 19 키(add1: +bref) · BOOK_PDF_ADD 11 · ready', "SYNC_KEYS:['status','note','qtype','conc','gpt','twin','ansfix','frm','maskpos','omrpos','mcard','bogi','unit','bpit','bpg','crop','txt','tfix','bref']," in s and "BOOK_PDF_ADD:11," in s and "TITLE:'지학 기출 서재', LOG:'지학', NAME:'지학', LAYER:true, ready:true}" in s)
    T2('A-10 제어문자 0 · U+FFFD 0', not any(ord(c) < 32 and c not in '\t\r\n' for c in s) and '\ufffd' not in s)
    npass = sum(1 for x in lines if x.startswith('PASS')); nfail = len(lines) - npass
    for x in lines: print(x)
    print('\n== %d PASS / %d FAIL / %d항 ==' % (npass, nfail, len(lines))); sys.exit(0 if nfail == 0 else 2)

if __name__ == '__main__':
    main()
