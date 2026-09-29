/* _harness_jo_hdrfold_tests.js — jo_hdrfold(9/27) 하네스 도구(__HF). __HM · __UZ · __JS 뒤에 붙는다.
   NEW·BASE 같은 것을 넣는다 — 바탕에는 #hdrFold 가 없다(헛잣대). 누름은 여기서 안 한다(자리만 · 파이썬이 page.mouse · CDP 터치 r22 · WebKit touchscreen). */
(function(){
const wait = ms => new Promise(r => setTimeout(r, ms));
const txt = e => e ? (e.textContent || '').replace(/\s+/g, ' ').trim() : '';
const vis = e => !!e && e.isConnected && getComputedStyle(e).display !== 'none' && getComputedStyle(e).visibility !== 'hidden' && e.getBoundingClientRect().height > 0;
const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return { x: +r.left.toFixed(2), y: +r.top.toFixed(2), w: +r.width.toFixed(2), h: +r.height.toFixed(2), r: +r.right.toFixed(2), b: +r.bottom.toFixed(2), cx: +(r.left + r.width / 2).toFixed(2), cy: +(r.top + r.height / 2).toFixed(2) }; };
function hitOn(t){ if (!t) return null; const r = R(t), at = document.elementFromPoint(r.cx, r.cy);
  const onScreen = r.cy > 0 && r.cy < innerHeight && r.cx > 0 && r.cx < innerWidth && r.w > 0 && r.h > 0;
  return Object.assign(r, { on: !!at && (at === t || t.contains(at)) && onScreen, onScreen, vis: vis(t), t: txt(t).slice(0, 40), tag: at ? at.tagName + '#' + at.id + '.' + String(at.className).slice(0, 30) : null }); }
async function idle(){ for (let i = 0; i < 400 && (typeof busy !== 'undefined' && busy); i++) await wait(25); }
async function until(f, ms){ const t0 = Date.now(); while (Date.now() - t0 < (ms || 8000)){ try{ const v = f(); if (v) return v; }catch(e){} await wait(40); } try{ return f(); }catch(e){ return null; } }
const FIVE = ['#hrail', '#hbadges', '#hsrow', '#slot .mbhd', '#slot .mbsr'];
window.__HF = {
  errs(){ return (window.__ERR || []).filter(e => !/^ResizeObserver loop/.test(e)).slice(0, 20); },
  btn(){ const b = document.getElementById('hdrFold'), l = document.getElementById('laws'); if (!b) return { has: false, laws: R(l) };
    const cs = getComputedStyle(b), lr = R(l), br = R(b);
    return Object.assign(hitOn(b), { has: true, text: b.textContent, title: b.title, laws: lr, prevId: b.previousElementSibling ? b.previousElementSibling.id : null,
      gapL: +(br.x - lr.r).toFixed(2), dy: +(br.cy - lr.cy).toFixed(2), sameRow: Math.abs(br.cy - lr.cy) <= 4,
      cs: { fontSize: cs.fontSize, color: cs.color, backgroundColor: cs.backgroundColor, borderTopWidth: cs.borderTopWidth, paddingLeft: cs.paddingLeft, paddingRight: cs.paddingRight } }); },
  state(){ const o = {}; FIVE.forEach(s => { const e = document.querySelector(s); o[s] = e ? (vis(e) ? 'vis' : getComputedStyle(e).display) : 'none-dom'; });
    const slot = document.getElementById('slot'), d = document.documentElement;
    return { five: o, slotTop: slot ? +slot.getBoundingClientRect().top.toFixed(1) : null, over: d.scrollWidth - d.clientWidth, hfold: document.getElementById('app').classList.contains('hfold'),
      S: typeof S !== 'undefined' ? { hdrFold: S.hdrFold, law: S.law, tab: S.tab } : null, logo: !!document.querySelector('header.topbar .logo') && vis(document.querySelector('header.topbar .logo')),
      laws: [...document.querySelectorAll('#laws .pill')].map(txt), lawsVis: vis(document.getElementById('laws')), btnVis: vis(document.getElementById('hdrFold')) }; },
  ui(){ try{ return JSON.parse(localStorage.getItem('jopangi_ui') || 'null'); }catch(e){ return 'bad'; } },
  lawAt(t){ const b = [...document.querySelectorAll('#laws .pill')].find(x => txt(x) === t); return b ? hitOn(b) : null; },
  railAt(re){ const rx = new RegExp(re); const b = [...document.querySelectorAll('#hrail .rb')].find(x => rx.test(txt(x))); return b ? hitOn(b) : null; },
  sk(){ const s = document.getElementById('sk'); return { vis: vis(s), disp: s ? getComputedStyle(s).display : null, focus: document.activeElement ? document.activeElement.id : null }; },
  skClose(){ try{ if (typeof skClose === 'function') skClose(); else { const s = document.getElementById('sk'); if (s) s.style.display = 'none'; } }catch(e){} return 1; },
  bars(){ const q = s => [...document.querySelectorAll(s)].filter(vis).length; return { modebar: q('#slot .modebar'), jtbar: q('#slot .jtbar'), ctrlbar: q('#slot .ctrlbar'), omrbar: q('#slot .omrbar'), hm: q('#slot .mbhm') }; },
  head(){ const top = document.querySelector('header.topbar'); if (!top) return null;
    const kids = [...top.children].filter(vis).map(e => ({ id: e.id || e.className, r: R(e) }));
    return { h: R(top).h, kids: kids, hs: document.getElementById('hsrow') ? R(document.getElementById('hsrow')).h : null }; },
  async gaek(law){ try{ closeAllPops(true); }catch(e){} S.law = law || '특허법'; S.tab = 'jimun'; S.jimunTab = 'ox'; S.mok = ''; S.oxQueue = ''; S.year = '';
    await idle(); await render(); await idle(); await until(() => document.querySelector('#slot .mbhd'), 30000); await wait(300); return !!document.querySelector('#slot .mbhd'); },
  async jo(law, k){ try{ closeAllPops(true); }catch(e){} S.tab = 'jo'; S.law = law || '특허법'; S.jo = k || '제1조'; await idle(); await render(); await idle(); await until(() => document.querySelector('#slot .jotitle'), 20000); await wait(300); return S.tab; }
};
})();
