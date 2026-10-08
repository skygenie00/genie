# -*- coding: utf-8 -*-
r"""_task_jagwa_penfinger §D 관문 — 자과앱(지학·생물) 문제 창: 손가락 굴림 · 손바닥 · 펜 필기 · 펜 누르기 · 펜/손가락/마우스 길게 누르기 · 물리 무변

  NEW  = --new <파일>(없으면 genie 작업트리 jagwa/index.html) · BASE = --base <파일>(없으면 genie 72a65b3 = bio ocrfix 인도 판 · md5(LF) b988c9c8)
  입력 = **진짜 포인터**(지시서 ★) — 손가락 = CDP Input.dispatchTouchEvent(radiusX·radiusY 22 = 아이패드 손가락 굵기 · 1 도 잰다)
         펜 = CDP Input.dispatchMouseEvent pointerType 'pen' · 마우스 = page.mouse — el.click()·합성 이벤트로 PASS 하지 않는다
  헛잣대 = 같은 시나리오를 BASE 에 먼저 — 고친 칸은 BASE 에서 FAIL 이어야 잣대다
  데이터 = studyplandata(earth · bio · phys) 로컬 사본을 같은 출처로 — GitHub 요청은 로컬로 돌리고 바깥 網은 막는다
  표본 = 생물 G57-05 · 지학 G48-03(채팅 실측과 같음) · 정답·해설 펼침

쓰기 : python _harness_jagwa_penfinger.py [--new 파일] [--base 파일] [--only earth,bio,phys]   결과 = _harness_jagwa_penfinger_result.txt
"""
import os as _os_r, sys as _sys_r   # env_lanes(9/29) — _roots.py(GENIE_ROOT · SPD_ROOT · MBPDF_ROOT)를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import _qa_common as QC   # noqa: E402 — _task_qa_slim2 A-1(10/8) · --mode gate|regress|smoke · --snap-in · --snap-out 을 뗀다 · gate = 인자 없음 = 이 판 앞과 같다
import _qa_jagwa_common as JG   # noqa: E402 — 자과 띄우기 헬퍼(_task_qa_slim2 A-1-2 · 옛 남 하네스 import 를 갈음)
import hashlib, http.server, io, json, os, socketserver, subprocess, sys, tempfile, threading, time, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright   # noqa: E402


def ARG(k, d=None):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


HERE = os.path.dirname(os.path.abspath(__file__))
GENIE = _roots.genie()
SPDROOT = _roots.spd()
NEWF = ARG('--new', os.path.join(GENIE, 'jagwa', 'index.html'))
BASEF = ARG('--base', '')
BASE_REV, BASE_MD5 = '72a65b3', 'b988c9c81546eaf1bcc3e250f4a2db92'
ONLY = [x for x in (ARG('--only', '') or '').split(',') if x]
WORK = os.path.join(tempfile.gettempdir(), 'h_penfinger'); os.makedirs(WORK, exist_ok=True)
SAMPLE = {'bio': 'B20-57-05', 'earth': 'G11-48-03'}   # ★ jagwa_uid(9/29) — 옛 G57-05 · G48-03(문항 번호 새 꼴)
RES = []


def T(grp, name, ok, detail=''):
    RES.append((grp, name, bool(ok), detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('%s | %s · %s | %s' % ('PASS' if ok else 'FAIL', grp, name, d[:300]), flush=True)


def N(grp, name, detail=''):
    RES.append((grp, name, None, detail))
    d = detail if isinstance(detail, str) else json.dumps(detail, ensure_ascii=False)
    print('NOTE | %s · %s | %s' % (grp, name, d[:300]), flush=True)


P = JG.P   # JG 로 옮김(_task_qa_slim2 A-1-2) — 남은 제 코드가 이 이름을 부른다 · 같은 객체(두 벌 아님)


# ── qa_slim2(2026-10-08) regress 도우미 — 이름이 `_rg` 로 시작 = gate 에서 안 쓰는 갈래(gate 에서 도는 줄은 원래 글 그대로)
def _rg_keep_base(keep):
    """regress — 기준 칸 4b · 6m · 7 의 바탕 값 = 앞 인도판 NEW 값 스냅샷(BASE scen 을 안 돌린다) — keep 의 BASE 자리를 스냅샷으로 채워 아래 비교(eff · == · move)를 그대로 탄다"""
    for subj in ('bio', 'earth'):
        for k in ('press', 'mouse'):
            d = keep.get(k) or {}
            if 'NEW' + subj in d:
                d['BASE' + subj] = QC.base('%s.%s' % (k, subj), d['NEW' + subj])
    ph = keep.get('phys') or {}
    if 'NEW' in ph:
        ph['BASE'] = QC.base('phys.7', ph['NEW'])


def scen(br, app, tag, subj, keep):
    g = '%s %s' % (tag, subj)
    u = SAMPLE[subj]
    QC.launch('base' if tag.startswith('BASE') else 'new')   # 셈(§B-4)
    p = P(br, app, subj, tag + subj)

    def fresh(tool='view'):
        p.ev("()=>__P.closeSheet()")
        ok = p.ev("u=>__P.open(u)", u); p.ev("()=>__P.ans()"); p.ev("m=>__P.tool(m)", tool); p.wait(250)
        # ★ 9/28 penfinger_add2 — 앞 관문의 마우스가 카드 글자 위에 남아 있으면, 도구를 펜으로 바꾼 뒤(덮개가 덮음) 크롬이 늦게 보내는
        #   마우스 hover 갱신(pointerleave)이 다음 손가락 길게 누르기 도중에 떨어져 tfixLong 시계를 끈다(tfixLong 은 어느 포인터의 leave 에도 끈다) —
        #   손가락 관문 앞에 마우스를 카드 밖 구석으로 치워 hover 를 매듭짓는다(마우스 관문은 제가 다시 옮긴다)
        p.pg.mouse.move(1, 1); p.wait(120)
        return ok

    try:
        ok = fresh()
        s0 = p.ev("()=>__P.st()")
        if QC.want('0'):
            T(g, '0 %s 문제 창 · 정답·해설 펼침 · 창보다 150px 넘게 길다(굴림 잣대가 설 만큼)' % u, ok and s0['det'] and s0['sh'] > s0['ch'] + 150, s0)
        # ── 1 손가락 굴림 · 반지름 22 · 1 · 보기 도구 · 펜 도구 ──
        got = {}
        for tool in ('view', 'pen'):
            fresh(tool)
            for r in (22, 1):
                p.ev("v=>__P.top(v)", 0); m = p.ev("()=>__P.wrapMid()")
                p.fdrag(m['x'], m['y'], 0, -225, r)
                t = p.ev("()=>__P.st()"); got['%s r%d' % (tool, r)] = t['top']
                if t['sheet']:
                    got['창 %s r%d' % (tool, r)] = t['sheet']; p.ev("()=>__P.closeSheet()")
        T(g, '1 손가락 위로 225px(반지름 22 · 아이패드 손가락) → 굴림 ≥ 150 — 보기·펜 도구 둘 다(헛잣대: 바탕 0)', got['view r22'] >= 150 and got['pen r22'] >= 150, got)
        if QC.want('1b'):
            T(g, '1b 반지름 1 도 같다(≥ 150)', got['view r1'] >= 150 and got['pen r1'] >= 150, got)
        if QC.want('1c'):
            T(g, '1c 손가락으로 끄는 동안 글자 고치기 창이 안 뜬다(길게 누르기 시계는 움직이면 꺼진다)', not any(k.startswith('창') for k in got), got)
        if QC.SMOKE:   # smoke — 1(손가락 굴림) + Z(페이지 오류 0)만
            er = p.errs + (p.ev("()=>__P.errs()") or [])
            T(g, 'Z 페이지 오류 0', not er, er[:5])
            return
        # ── 2 손바닥(ⓑ 그대로) ──
        fresh('pen')
        q = p.ev("()=>__P.at('.q',.3,.5)")
        n0 = p.ev("()=>__P.st()")['strokes']
        p.pdrag(q['x'], q['y'], q['x'] + 60, q['y'] + 2)
        p.ev("v=>__P.top(v)", 40); m = p.ev("()=>__P.wrapMid()")
        p.fdrag(m['x'], m['y'], 0, -120, 22)
        a = p.ev("()=>__P.st()")['top']
        p.wait(1500); p.ev("v=>__P.top(v)", 40)
        p.fdrag(m['x'], m['y'], 0, -120, 22)
        b = p.ev("()=>__P.st()")['top']
        T(g, '2 펜 뗀 뒤 0.5초 안 손가락(반지름 22) → 굴림 0 · 1.5초 뒤 → 굴림(헛잣대: 바탕은 뒤도 0)', a == 40 and b > 40 + 60, {'0.5초 안': a, '1.5초 뒤': b, '획': n0})
        # ── 3 펜 필기 — 문제 글 · 〈보기〉 줄 글 · 〈보기〉 설명 ──
        fresh('pen')
        tg = [('문제 글', '.q', .25, .5), ('〈보기〉 ㄱ 줄 글', '.bogi .row .t', .15, .3)]
        if subj == 'bio':
            tg.append(('〈보기〉 ㄱ 설명', '.bogi .row .bexp', .2, .5))
        res3 = {}
        for nm, sel, fx, fy in tg:
            a = p.ev("([s,x,y])=>__P.at(s,x,y)", [sel, fx, fy])
            if not a:
                res3[nm] = '표적 없음'; continue
            s1 = p.ev("()=>__P.st()")
            p.pdrag(a['x'], a['y'], a['x'] + 60, a['y'] + 1)
            s2 = p.ev("()=>__P.st()")
            res3[nm] = {'획': [s1['strokes'], s2['strokes']], '굴림': [s1['top'], s2['top']], '밑': a['under'], '안': a['inEl']}
        ok3 = all(isinstance(v, dict) and v['안'] and v['획'][1] == v['획'][0] + 1 and v['굴림'][0] == v['굴림'][1] for v in res3.values())
        T(g, '3 펜 60px 긋기 → 획 +1씩 · 그동안 굴림 무변 — %s(헛잣대: 바탕 획 0)' % ' · '.join(res3), ok3, res3)
        keep.setdefault('stroke_on_q', {})[tag + subj] = res3.get('문제 글')
        # ── 4 펜 누르기 무변 — 선택지 · 〈보기〉 O/X(덮개 밑) · O/△/X 표시(근거 층) · 「정답·해설 ▸」 · 근거 ＋ ──
        fresh('pen')
        r4 = {}
        s = p.ev("()=>__P.st()")
        a = p.ev("()=>__P.at('.choices button[data-c=\"2\"]',.5,.5)")
        if a:
            p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['선택지 ②'] = {'pick': t['pick'], '획': t['strokes'] - s['strokes'], '밑': a['under']}
        a = p.ev("()=>__P.at('.bogi .row .ox button[data-v=\"O\"]',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['〈보기〉 O'] = {'ox': t['ox'], 'ox0': s['ox'], '획': t['strokes'] - s['strokes']}   # ★ A-6(a) 9/30 — 누르기 전 O/X(4b 가 누름이 바꾼 칸을 맞댄다)
        a = p.ev("()=>__P.at('.vox[data-vmark=\"Q\"]',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['표시 △'] = {'vox': t['vox'], '획': t['strokes'] - s['strokes'], '위': a['top']}
        a = p.ev("()=>__P.at('#cDetBtn',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); t = p.ev("()=>__P.st()"); r4['정답·해설 ▸'] = {'det': [s['det'], t['det']], '획': t['strokes'] - s['strokes']}
        a = p.ev("()=>__P.at('.ggwrap button[title=\"병렬 근거 줄 더하기\"]',.5,.5)")
        if a:
            s = p.ev("()=>__P.st()"); p.ptap(a['x'], a['y']); p.wait(300); t = p.ev("()=>__P.st()"); r4['근거 ＋'] = {'gg': [s['gg'], t['gg']], '획': t['strokes'] - s['strokes']}
        keep.setdefault('press', {})[tag + subj] = r4
        ok4 = all(v.get('획') == 0 for v in r4.values()) and r4.get('선택지 ②', {}).get('pick') == [2] and r4.get('정답·해설 ▸', {}).get('det') == [True, False] \
            and bool(r4.get('〈보기〉 O', {}).get('ox')) and 'Q' in (r4.get('표시 △', {}).get('vox') or [])
        T(g, '4 펜 톡 → 선택지 고름 · 〈보기〉 O 표시 · △ 표시 · 「정답·해설 ▸」 접힘 · 근거 ＋(바탕과 맞대기는 끝에) · 넷 다 획 0', ok4, r4)
        # ── 5 펜 길게 누르기 → 글자 고치기 · 획 무증가 · 이미 그은 획 위에서도 ──
        fresh('pen')
        r5 = {}
        for nm, sel, fx, want in (('문제 글', '.q', .25, '✎ 글자 고치기 — 문제'), ('〈보기〉 ㄱ', '.bogi .row .t', .12, '✎ 글자 고치기 — 〈보기〉 ㄱ')):
            a = p.ev("([s,x])=>__P.at(s,x,.4)", [sel, fx])
            if not a:
                r5[nm] = '표적 없음'; continue
            s = p.ev("()=>__P.st()"); p.phold(a['x'], a['y'], 750); t = p.ev("()=>__P.st()")
            r5[nm] = {'sheet': t['sheet'], 'want': want, '획': t['strokes'] - s['strokes']}
            p.ev("()=>__P.closeSheet()"); p.wait(150)
        # 이미 그은 획 위
        a = p.ev("()=>__P.at('.q',.55,.5)")
        s = p.ev("()=>__P.st()"); p.pdrag(a['x'], a['y'], a['x'] + 70, a['y']); t = p.ev("()=>__P.st()")
        sp = p.ev("()=>__P.strokeAt()")
        if t['strokes'] == s['strokes'] + 1 and sp:
            s2 = p.ev("()=>__P.st()"); p.phold(sp['x'], sp['y'], 750); t2 = p.ev("()=>__P.st()")
            r5['획 위'] = {'sheet': t2['sheet'], 'want': '✎ 글자 고치기 — 문제', '획': t2['strokes'] - s2['strokes']}
            p.ev("()=>__P.closeSheet()")
        else:
            # 바탕은 글자 위에 획이 안 그어져(3번) 그을 수 있는 빈 곳에 긋고 그 위에서 잰다 — 글자 위 획이 없으니 「획 위」 는 못 잰다
            r5['획 위'] = {'sheet': None, 'want': '✎ 글자 고치기 — 문제', '획': None, '까닭': '글자 위에 획을 못 그었다(바탕의 3번 증상)'}
        ok5 = all(isinstance(v, dict) and v.get('sheet') == v.get('want') and v.get('획') == 0 for v in r5.values())
        T(g, '5 펜 750ms(2px 안) → 「✎ 글자 고치기 — 문제 / 〈보기〉 ㄱ」 · 획 무증가 · 이미 그은 획 위에서도(헛잣대: 바탕은 획 위에서 안 열림)', ok5, r5)
        # ── 5b 펜 길게 누르기(창) 뒤에도 손가락 굴림 — 펜을 창 위에서 떼 penDown 이 안 풀리던 것 ──
        fresh('pen')   # 그 앞 펜 동작이 상자 안에서 떼며 penDown 을 풀어 두지 않게 — 펜 길게 누르기 하나만 하고 곧바로 잰다
        a = p.ev("()=>__P.at('.q',.25,.4)")
        p.phold(a['x'], a['y'], 750); sh5 = p.ev("()=>__P.st()")['sheet']
        p.ev("()=>__P.closeSheet()"); p.wait(1500)
        p.ev("v=>__P.top(v)", 0); m = p.ev("()=>__P.wrapMid()"); p.fdrag(m['x'] - 150, m['y'], 0, -225, 1)
        t5 = p.ev("()=>__P.st()")
        T(g, '5b 펜 길게 누르기로 창을 연 뒤 1.5초 — 손가락(반지름 1) 굴림 ≥ 150(헛잣대: 바탕 0 — 펜을 창 위에서 떼 penDown 이 참으로 남았다)', sh5 == '✎ 글자 고치기 — 문제' and t5['top'] >= 150, {'펜 길게 창': sh5, 'top': t5['top'], 'sheet': t5['sheet']})
        p.ev("()=>__P.closeSheet()")
        # ── 6 손가락·마우스 길게 누르기 → 글자 고치기 ──
        r6 = {}
        for tool in ('view', 'pen'):
            fresh(tool)
            a = p.ev("()=>__P.at('.q',.3,.5)")
            p.fhold(a['x'], a['y'], 800, 22); r6['손가락 ' + tool] = p.ev("()=>__P.st()")['sheet']; p.ev("()=>__P.closeSheet()")
        fresh('view')
        a = p.ev("()=>__P.at('.q',.3,.5)")
        p.pg.mouse.move(a['x'], a['y']); p.pg.mouse.down(); p.wait(800); p.pg.mouse.up(); p.wait(300)
        r6['마우스'] = p.ev("()=>__P.st()")['sheet']; p.ev("()=>__P.closeSheet()")
        keep.setdefault('mouse', {})[tag + subj] = r6['마우스']
        W6 = '✎ 글자 고치기 — 문제'
        T(g, '6 손가락(반지름 22 · 800ms) 문제 글 길게 → 「%s」 — 보기·펜 도구 둘 다 · 마우스도(헛잣대: 바탕은 손가락으로 안 열림 — 가드가 capture 에서 막았다)' % W6,
          r6.get('손가락 view') == W6 and r6.get('손가락 pen') == W6 and r6.get('마우스') == W6, r6)
        # 6b 선택지 단추(눌리는 것) 길게 — 창은 하나(가드 시계와 단추 제 tfixLong 이 겹치지 않는다) · 고르지 않는다
        fresh('view')
        a = p.ev("()=>__P.at('.choices button[data-c=\"4\"]',.5,.5)")
        s6 = p.ev("()=>__P.st()")
        p.fhold(a['x'], a['y'], 800, 22)
        n6, t6 = p.ev("()=>__P.sheets()"), p.ev("()=>__P.st()")
        p.ev("()=>__P.closeSheet()")
        T(g, '6b 선택지 ④ 손가락 길게 → 글자 고치기 창 1(겹침 없음) · ④ 는 안 골라진다', n6 == 1 and 4 not in (t6['pick'] or []) and t6['sheet'] == '✎ 글자 고치기 — 보기 ④',
          {'창': n6, 'sheet': t6['sheet'], 'pick': [s6['pick'], t6['pick']]})
        # 6c 손바닥 — 펜을 뗀 뒤 0.5초 안에 글자 위에 얹은 손가락(= 손바닥)은 길게 눌러도 안 연다
        fresh('pen')
        a = p.ev("()=>__P.at('.q',.3,.5)")
        b = p.ev("()=>__P.wrapMid()")
        p.pdrag(b['x'] - 200, b['y'] + 60, b['x'] - 140, b['y'] + 62)
        p.fhold(a['x'], a['y'], 800, 22)
        t6 = p.ev("()=>__P.st()"); p.ev("()=>__P.closeSheet()")
        T(g, '6c 펜 뗀 뒤 0.5초 안 글자 위 손가락(손바닥) 800ms → 창 안 뜸', not t6['sheet'], t6['sheet'])
        er = p.errs + (p.ev("()=>__P.errs()") or [])
        T(g, 'Z 페이지 오류 0', not er, er[:5])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def scen_phys(br, app, tag, keep):
    g = '%s phys' % tag
    QC.launch('base' if tag.startswith('BASE') else 'new')   # 셈(§B-4)
    p = P(br, app, 'phys', tag + 'phys')
    try:
        no = p.ev("()=>DATA.find(r=>r[F.FILE]&&r[F.FILE]!=='IMG'||true)[F.NO]")
        p.ev("n=>openView(n)", no); p.wait(1500)
        dom = p.ev("()=>__P.physDom()")
        st = p.ev("()=>{const s=document.getElementById('stage');if(!s)return null;const r=s.getBoundingClientRect();return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height*.6),top:s.scrollTop,sh:s.scrollHeight,ch:s.clientHeight}}")
        mv = None
        if st:
            p.fdrag(st['x'], st['y'], 0, -200, 22)
            mv = p.ev("()=>{const s=document.getElementById('stage');return s?[s.scrollTop,s.scrollLeft]:null}")
        keep.setdefault('phys', {})[tag] = {'dom': hashlib.md5(dom.encode('utf-8')).hexdigest() + ':%d' % len(dom), 'stage': st, 'move': mv}
        N(g, '7 물리 문제 창 DOM · #stage 손가락(반지름 22) 끌기(바탕과 맞대기는 끝에)', keep['phys'][tag])
        er = p.errs + (p.ev("()=>__P.errs()") or [])
        T(g, 'Z 페이지 오류 0', not er, er[:5])
    except Exception as ex:
        T(g, '묶음 예외', False, repr(ex)[:400])
    finally:
        p.close()


def report(t0, newmd5, bmd5):
    lines = ['# _harness_jagwa_penfinger — %s' % time.strftime('%Y-%m-%d %H:%M'),
             'NEW = %s (md5(LF) %s) · BASE = %s (md5(LF) %s) · 데이터 = studyplandata 로컬' % (NEWF, newmd5, BASEF or BASE_REV, bmd5),
             '입력 = CDP 터치(반지름 22·1) · CDP 펜(pointerType pen) · page.mouse — 합성 이벤트·el.click 없음', '']
    for grp, name, ok, d in RES:
        dd = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
        lines.append('%s | %s · %s | %s' % ('NOTE' if ok is None else 'PASS' if ok else 'FAIL', grp, name, dd[:700]))
    new = [x for x in RES if x[2] is not None and not x[0].startswith('BASE')]
    base = [x for x in RES if x[2] is not None and x[0].startswith('BASE')]
    np_, nf = sum(1 for x in new if x[2]), sum(1 for x in new if not x[2])
    bp, bf = sum(1 for x in base if x[2]), sum(1 for x in base if not x[2])
    lines += ['', '헛잣대(BASE) — PASS %d · FAIL %d (고친 칸 잣대는 FAIL 이어야 잣대 — 반지름 1 굴림·페이지 오류 같은 무변 잣대는 PASS)' % (bp, bf),
              '합계(NEW)  PASS %d · FAIL %d  (%.0f초)' % (np_, nf, time.time() - t0)]
    txt = '\n'.join(lines) + '\n'
    f = os.path.join(HERE, '_harness_jagwa_penfinger_result.txt')
    for _ in range(3):
        io.open(f, 'w', encoding='utf-8', newline='\n').write(txt); time.sleep(0.5)
        if io.open(f, encoding='utf-8').read() == txt:
            break
    print('\n'.join(lines[-3:]))
    return nf


def main():
    t0 = time.time()
    new = io.open(NEWF, encoding='utf-8', newline='').read()
    newmd5 = hashlib.md5(new.replace('\r\n', '\n').encode('utf-8')).hexdigest()
    if QC.GATE:
        QC.sub('git:show-app')
        base = io.open(BASEF, encoding='utf-8', newline='').read() if BASEF else subprocess.run(['git', '-C', GENIE, 'show', BASE_REV + ':jagwa/index.html'], capture_output=True).stdout.decode('utf-8')
        bmd5 = hashlib.md5(base.replace('\r\n', '\n').encode('utf-8')).hexdigest()
        T('땅값', 'BASE = bio ocrfix 인도 판(72a65b3 · b988c9c8)', bmd5 == BASE_MD5, bmd5)
    else:   # regress · smoke — 바탕(72a65b3) 앱 풀기 0 · 땅값(바탕 md5) 칸 = 관문만
        base, bmd5 = None, '(regress — 바탕 안 띄움)'
    run = lambda x: not ONLY or x in ONLY
    keep = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for subj in ('bio', 'earth'):
            if run(subj):
                if QC.GATE:   # BASE scen = 헛잣대 줄(관문만)
                    scen(br, base, 'BASE', subj, keep)
                scen(br, new, 'NEW', subj, keep)
        if run('phys') and not QC.SMOKE:   # smoke — 물리 안 돎(smoke 칸 = 지학 · 생물 손가락 굴림)
            if QC.GATE:
                scen_phys(br, base, 'BASE', keep)
            scen_phys(br, new, 'NEW', keep)
        br.close()
    if QC.REGRESS:   # regress — 4b · 6m · 7 바탕 값 = 앞 인도판 NEW 값 스냅샷
        _rg_keep_base(keep)
    for subj in ('bio', 'earth'):
        a, b = (keep.get('press') or {}).get('BASE' + subj), (keep.get('press') or {}).get('NEW' + subj)
        if a is not None and b is not None:
            # ★ A-6(a) 9/30 _task_qa_baseline — jagwa_uid(genie 5e18424 + studyplandata 4a011475 · 결정로그 9/29 15:09 · _task_jagwa_uid.md 수행 결과 「남은 차이 … penfinger 4b 지학
            #   = 바탕 쪽(옛 앱 + 새 데이터)이 기록을 못 봄」): 옛 앱(BASE 72a65b3)은 새 번호 데이터에서 옛 열쇠 기록(〈보기〉 O/X · 근거)을 못 봐 누르기 전 상태가 갈린다
            #   → 〈보기〉 O 는 누름이 바꾼 칸(앞뒤 대칭차) · 근거 ＋ 는 늘어난 글자 수로 맞댄다 · 선택지·△·정답·해설·획 수는 그대로 같아야
            def eff(r):
                o = {}
                for k, v in r.items():
                    if k == '〈보기〉 O':
                        o[k] = {'바뀐 칸': sorted(set(v.get('ox0') or []) ^ set(v.get('ox') or [])), '획': v.get('획')}
                    elif k == '근거 ＋':
                        g = v.get('gg') or [0, 0]
                        o[k] = {'늘어난 글자': g[1] - g[0], '획': v.get('획')}
                    else:
                        o[k] = {kk: vv for kk, vv in v.items() if kk not in ('밑', '위')}
                return o
            T('NEW ' + subj, '4b 펜 근거 ＋ = 바탕과 같은 결과 · 선택지·O/X·△·정답·해설 누름도 바탕과 같음',
              eff(a) == eff(b),
              {'BASE': a, 'NEW': b})
        la, lb = (keep.get('mouse') or {}).get('BASE' + subj), (keep.get('mouse') or {}).get('NEW' + subj)
        if la is not None and lb is not None:
            T('NEW ' + subj, '6m 마우스 길게 누르기 = 바탕 그대로(무변)', la == lb, {'BASE': la, 'NEW': lb})
    ph = keep.get('phys') or {}
    if 'BASE' in ph and 'NEW' in ph:
        # ★ 합치기 10/1(하위 에이전트 C) — physphone A-3 · A-5(97883ef)가 물리 문제 창 머리·근거 칸을 바꿨다(DOM 해시 · #stage 자리·높이) — 손가락 끌기 결과(move)만 바탕과 맞댄다
        T('NEW phys', '7 물리 문제 창 DOM · #stage 손가락 끌기 = 바탕', ph['BASE'] == ph['NEW']
          or ((ph['NEW'] or {}).get('move') is not None and (ph['NEW'] or {}).get('move') == (ph['BASE'] or {}).get('move')), ph)
    return report(t0, newmd5, bmd5)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
