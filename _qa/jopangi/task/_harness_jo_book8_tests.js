/* _harness_jo_book8_tests.js — _task_jo_book8 관문 도구(__B8).
   mbsame 도구(__HM) · uidmbs2 도구(__UZ) 뒤에 붙는다 · BASE(genie HEAD = jo_p8up 인도판)·NEW 같은 것을 넣는다 — 없는 함수·칸은 빈 값(헛잣대).
   ⚠ 누름은 여기서 안 한다 — 자리만 돌려주고 파이썬이 page.mouse · CDP 터치 r22 · WebKit touchscreen.tap 으로 누른다. */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
function hitOn(t){ if (!t) return null; try{ t.scrollIntoView({ block: 'center', inline: 'nearest' }); }catch(e){}
  const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen, vis: vis(t), t: txt(t).slice(0, 60), tag: at ? at.tagName + '.' + at.className : null }); }
const pops = () => (typeof POPS !== 'undefined' ? POPS : []);
const popOf = pre => pops().filter(x => (x._pk || '').indexOf(pre) === 0).pop();
const boxPop = () => popOf('cell|📚 교재 자리');
const bookPop = () => popOf('cv|book|patent_hr8');
window.__B8 = {
  idAt(k){ const c = [...document.querySelectorAll('.qb.id')].filter(vis).find(b => txt(b) === k) || [...document.querySelectorAll('.qb.id')].find(b => txt(b) === k); return c ? hitOn(c) : null; },
  box(){ const w = boxPop(); if (!w) return null; const h = w.querySelector('.mbb8');
    return { next: /다음 판에서/.test(txt(w)), p8u: h ? h.dataset.p8u : null, vis: vis(w),
      rows: h ? [...h.querySelectorAll('.mbbrow')].map(r => ({ k: txt(r.querySelector('.hd .k')), p: txt(r.querySelector('.hd .p')), m: [...r.querySelectorAll('.hd .m')].map(txt), sn: txt(r.querySelector('.sn')), vis: vis(r), pdf: +r.dataset.p })) : [],
      btns: h ? [...h.querySelectorAll('.ncb-more')].map(b => ({ t: txt(b), vis: vis(b) })) : [], none: h ? [...h.querySelectorAll('.mbbnone')].map(txt) : [],
      pic: h ? !!h.querySelector('.ncb-pic canvas') : false, loading: h ? /받는 중/.test(txt(h)) : false,
      omrRows: [...w.querySelectorAll('.mbbrow')].filter(r => !r.closest('.mbb8')).map(r => txt(r.querySelector('.hd .k'))) }; },
  async boxReady(){ for (let i = 0; i < 300; i++){ const b = __B8.box(); if (b && !b.loading && (b.rows.length || b.none.length || !b.p8u)){ await wait(400); return __B8.box(); } await wait(50); } return __B8.box(); },
  async snipReady(){ for (let i = 0; i < 200; i++){ const b = __B8.box(); if (b && b.rows.length && b.rows[0].sn) return b; await wait(50); } return __B8.box(); },
  async picReady(){ for (let i = 0; i < 400; i++){ const b = __B8.box(); if (b && b.pic) return b; await wait(50); } return __B8.box(); },
  rowAt(i){ const w = boxPop(); const r = w && w.querySelectorAll('.mbb8 .mbbrow')[i || 0]; return r ? hitOn(r) : null; },
  btnAt(re){ const w = boxPop(); const rx = new RegExp(re); const b = w && [...w.querySelectorAll('.mbb8 .ncb-more')].find(x => rx.test(txt(x))); return b ? hitOn(b) : null; },
  book(){ const w = bookPop(); if (!w) return { n: 0 };
    const pg = w.querySelector('.cv-bookpg'), hl = w.querySelector('.cv-bookhl'), box = w.querySelector('.cv-pickbox'), cvs = w.querySelector('.cv-bookpg canvas'), nav = w.querySelector('.cv-booknav');
    return { n: pops().filter(x => (x._pk || '').indexOf('cv|book|') === 0).length, page: nav && nav.querySelector('#cvBookP') ? +nav.querySelector('#cvBookP').value : null, nav: txt(nav), title: txt(w.querySelector('.pt')),
      hl: hl ? { l: parseFloat(hl.style.left), t: parseFloat(hl.style.top), w: parseFloat(hl.style.width), h: parseFloat(hl.style.height), vis: vis(hl) } : null,
      pg: R(pg), box: box ? { l: parseFloat(box.style.left), t: parseFloat(box.style.top), w: parseFloat(box.style.width), h: parseFloat(box.style.height) } : null,
      ov: !!w.querySelector('.cv-pickov'), pkOn: !!w.querySelector('.cv-booknav [data-pk].on'), sv: txt(w.querySelector('.cv-booknav [data-sv]')),
      cvsW: cvs ? cvs.width : 0, loading: /받는 중/.test(txt(w)), err: /받지 못했다/.test(txt(w)) ? txt(w).slice(0, 200) : null, rect: R(w) }; },
  async bookReady(){ for (let i = 0; i < 900; i++){ const b = __B8.book(); if (b.n && (b.cvsW > 0 || b.err) && !b.loading){ await wait(200); return __B8.book(); } await wait(50); } return __B8.book(); },
  bookAt(what){ const w = bookPop(); if (!w) return null;
    const t = w.querySelector(what === 'pk' ? '.cv-booknav [data-pk]' : what === 'sv' ? '.cv-booknav [data-sv]' : what === 'x' ? '.ph button' : '.cv-bookpg');
    if (!t) return null; if (what === 'pg'){ try{ t.scrollIntoView({ block: 'nearest' }); }catch(e){} return R(t); } return hitOn(t); },
  pin(u){ try{ return (JSON.parse(localStorage.getItem('jopangi.canvasjari') || '{}'))['p8|' + u] || null; }catch(e){ return null; } },
  orphBadge(){ const w = document.getElementById('cvJariOrph'); return w ? { t: txt(w), vis: vis(w) } : null; },
  api(){ try{ return { k8: !!(viewCanvas.jari && viewCanvas.jari.k8), book8: !!(viewCanvas.jari && viewCanvas.jari.book8), name: viewCanvas.hsBook ? viewCanvas.hsBook.name('patent_hr8') : null }; }catch(e){ return { err: String(e) }; } },
  async idb(k){ return await new Promise(res => { let rq; try{ rq = indexedDB.open('ox_master_db', 1); }catch(e){ return res({ err: String(e) }); }
    rq.onupgradeneeded = () => { const db = rq.result; if (!db.objectStoreNames.contains('rows')) db.createObjectStore('rows'); };
    rq.onsuccess = () => { const db = rq.result; let g; try{ g = db.transaction('rows', 'readonly').objectStore('rows').get(k); }catch(e){ return res({ err: String(e) }); }
      g.onsuccess = () => { const v = g.result; res(v ? { has: true, md5: v.pdfMd5 || null, n: (v.buf && v.buf.byteLength) || 0, keys: Object.keys(v).slice(0, 6) } : { has: false }); }; g.onerror = () => res({ has: false }); };
    rq.onerror = () => res({ err: 'open' }); }); },
  async idbDel(k){ return await new Promise(res => { const rq = indexedDB.open('ox_master_db', 1);
    rq.onupgradeneeded = () => { const db = rq.result; if (!db.objectStoreNames.contains('rows')) db.createObjectStore('rows'); };
    rq.onsuccess = () => { const db = rq.result; try{ const tx = db.transaction('rows', 'readwrite'); tx.objectStore('rows').delete(k); tx.oncomplete = () => res(true); tx.onerror = () => res(false); }catch(e){ res(false); } };
    rq.onerror = () => res(false); }); },
  stat(){ try{ return JSON.parse(JSON.stringify((window.__jocvb && window.__jocvb.C.stat['patent_hr8']) || null)); }catch(e){ return null; } },
  closeAll(){ try{ closeAllPops(); }catch(e){} return true; },
  closeBox(){ pops().filter(x => /^(cell\|📚|cv\|book\|)/.test(x._pk || '')).forEach(x => { try{ closeOne(x); }catch(e){} }); return true; }   /* 교재 자리 창 · 교재 창만(검색 지문 팝업은 둔다) */
};
})();
