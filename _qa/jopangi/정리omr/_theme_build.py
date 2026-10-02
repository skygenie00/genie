# -*- coding: utf-8 -*-
"""⚙ 정리omr 테마 재료 — theme/patent_hr8/테마.json.gz + 표 초안(_테마\\테마.csv · 두문자.csv · 주체.txt)
   (jopangi/task/_task_jo_theme_data.md A-1 · 2026-10-01 · 파일 꼴 정본 = _task_jo_theme.md §A-0
    · 2026-10-02 _task_jo_theme_fix2 §A — 거리 묶음 걷음 · 구역 그림 · 테마 점 새 규칙)

  python _theme_build.py                 만든다(표가 없으면 초안을 먼저 쓴다 · 있으면 안 덮는다 · 테마.json.gz · img\\<k>.webp 는 바뀌었을 때만 쓴다 · 멱등)
  python _theme_build.py --check         만들지 않고 값만(§B) — 표·gz 를 쓰지 않는다(표가 없으면 메모리 초안으로 잰다)
  python _theme_build.py --tables <폴더> --out <파일>    다른 표 폴더 · 다른 출력(하네스가 쓴다 · 기본 = N: _테마 · MBPDF_ROOT)

  재료(읽기만 · 한 바이트도 안 고친다)
    정리omr  = <N:>\\jopangi\\정리omr\\26특허해례정리omr주석1.pdf — 도장(Stamp) 191 = 텍스트박스 · 펜 Ink 1,256
    대조     = 같은 폴더 26특허해례정리omr프1.pdf 1~5쪽(도장 글이 쪽 글자로 찍힌 판) — 박스 글자 = 프1 같은 자리 같은 글자 100% 가 아니면 멈춘다
    조문     = <GENIE_ROOT>\\jo\\data\\ jo_특허법_목록.json(조 열쇠·제목) · jo_특허법_본문.json(법조문 줄 H·항·호·본문 = 사전 · 주체)
               · blank_특허.json(bk = 앱 서랍 점 셋의 출처 — 빈칸 kind 내용·주체·기간 · 주체 켜진 조 175/268) · prec_특허_전문.json(흔한 법률어)
  박스 뽑기 — 도장 /AP /N(Form XObject · 서브셋 CID 글꼴 · ToUnicode 없음 → pypdf 는 못 읽고 pdfminer 는 읽는다)을
    쪽 크기 빈 쪽에 Rect 맞춰 한 장씩 그린 PDF(메모리 · 파일 안 남김)를 pdfplumber 로 읽는다. 도장 작성자(/T) 칸은 읽지 않는다.
    Adobe-Korea1 밖 CID 두 글리프는 CID_FIX 판독표(모양을 보고 정함)로 · 표에 없는 「(cid:N)」 이 나오면 멈춘다.
    k = 주석 차례 번호(1쪽 첫 도장 0 … 5쪽 끝 190 · 글 없는 도장 포함) · p = 쪽 · r = Rect / 쪽 크기(위 기준 · [x0,y0,x1,y1])
    줄 = 기준선 y 가 줄 첫 글자에서 ±0.6pt · x 차례 · 공백 = 도장 속 실제 공백 글리프 그대로(폭 0.57pt — 지시서의 「틈 > 폭 중앙값×1.45」
         만으로는 이 공백을 못 잡아 낱말이 붙는다 · 2026-10-01 실측) + 글리프 없이 뛴 자리(틈 > 박스 글자 폭 중앙값×1.45)에 공백 하나
    ind = round((줄 첫 글자 x − 박스 왼쪽) / 2.7) · run = 글자색이 바뀔 때 끊음(#rrggbb · 공백은 앞 run 에 붙음) · 줄 앞뒤 공백은 뺀다
  초안 규칙(표가 없을 때 처음 한 번만 — 박스 묶음은 표가 정본이다)
    테마  = 큰 박스(공백 뺀 글자 200 이상) 한 줄씩 · 이름 = 첫 줄 머리 {…} 안 글(없으면 「N.」·「3.3.」 번호 떼고 첫 줄 24자)
            · 작은 조각·그림 도장은 초안에 안 붙인다 — 어느 테마에 갈지는 표(사람 · 채팅 그림 검수)가 정한다
              (옛 「같은 쪽 사각 거리 가장 가까운 큰 박스에 +k」 규칙은 걷었다 — 근거 없이 들어간 규칙 · _task_jo_theme_fix2 §A-1 · 2026-10-02)
            · 조 = 그 줄 박스 글의 조 인용 중 특허법(목록에 있는 조)만 — 「…법」 이름(민법·상표법·민집법·민소법 …) · 시규 · 민소 · 시행령 · PCT 머리는
              다른 법으로 빼고 · 한 글자 머리(상·디)는 앞이 한글이 아니면 다른 법 · 앞이 한글이면 못 가름(_task_jo_theme_fix1 A-32 와 같은 규칙)
            · bk = 빈칸(굽을 때 아래 「테마 점」 규칙으로 센다)
  테마 점 bk = [내용, 주체, 기간](표 bk 칸이 비었을 때 · 적으면 그 값 — _task_jo_theme_fix2 §A-4 · 사용자 10/1 00:38 「그 테마 글에 그 갈래가 있으면 켜짐」)
    내용 = 테마 조 가운데 blank_특허.json 내용 빈칸이 있는 조가 있음(옛 규칙 그대로)
    주체 = 테마 글(박스 글 · 구역 SVG 글 · 이름 말고)에 주체 목록(주체.txt) 낱말이 하나라도 있음
    기간 = ① 테마 박스(구역 포함) 위에 초록 형광펜 획 — Ink /C (0,1,0) 진한 초록 · (0.694,1,0) 연두 · 굵기 ≥ 2.5pt
             (획 점 사각의 가운데가 든 박스 · 두 박스에 들면 획에 가장 가까운 글자의 박스 · 구역 사각에 들면 그 구역 테마 ·
              1.3pt 초록(✓·낙서) · 0.78pt 초록 펜 그림 · 노랑 형광펜은 뺀다) — 사용자 10/2 09:27 · 09:37
           ② 또는 테마 글(이름 말고)에 「기간」 낱말이 그대로 있음 · 테마에서만(조문 줄 점 무변)
    두문자 = 한글 2~8 + 숫자 0~3 낱말 · (같은 박스 두 번 이상) 또는 (글자가 모두 검정 아닌 한 색) · 사전(법조문 낱말·조 제목·흔한 법률어) 밖
            → 사전 낱말(2자 이상)·한 글자 접사·조사로만 나뉘는 합성어 · 조 인용 꼴 · 「…때/것/판례」 꼴을 뺀다
            → 다른 후보 + 사전 낱말로 된 구(「존기연출원」)를 뺀다 · 조 = 그 말이 든 줄의 특허법 조 인용
    주체  = 법조문 줄의 「…장·…관·…인·…자(·…원)」 명사 · 빈도 5 이상 · 조사가 붙어 나온 적 있음(서술격 「-인」 거름) · 「…출원」·행위말 뺌
  표(사용자 정본 · N:) — 처음 한 번 초안을 쓰고, 있으면 안 덮는다. 손질 뒤 이 ⚙ 를 다시 돌리면 그대로 다시 굽는다.
    테마.csv  id,이름,박스,구역,조,bk
      박스 = 「k k k」(빈칸 가름 · 옛 표의 앞 + 표시는 읽을 때 무시한다 — 뜻은 같다)
      구역 = 「쪽 x0 y0 x1 y1」(pt · 위 기준 · 쪽 841.8×595.32) — 적으면 그 사각을 SVG 하나로 그린다(앱 = 박스 글 대신 SVG):
             구역 박스 = 그 테마 박스 칸의 박스 중 가운데가 사각 안인 것(줄 글에서 빠지고 SVG 로만 보인다)
             · 글 = 구역 박스의 글자 중 사각 안(남의 박스 글자는 안 그린다 — 테마 밖 박스 조각·같은 테마 큰 박스 글이 SVG 에 겹쳐 나오지 않게 · fix2)
             · 그림 도장 = 그림이면 <image>(원본 해상도 webp) · 벡터면 <path> · 펜 획 = 점이 모두 사각 안인 Ink
      조   = 「3 4 7-2 133」(특허법 조 · 「16②」 → 「16」 · 「42-2」 · 「36의2」 = 그 조) · bk = 「110」(내용·주체·기간 · 비우면 위 「테마 점」 규칙으로 셈)
    두문자.csv 말,뜻,조   주체.txt 한 줄 하나(빈 줄 · # 줄 무시) — 엑셀이 CP949 로 저장해도 읽는다(utf-8 → cp949 차례)
  출력 = <MBPDF_ROOT>\\theme\\patent_hr8\\테마.json.gz (+ 구역 그림 = 같은 폴더 img\\<k>.webp)
    { pdfMd5(주석1 PDF), boxes:{k:{p,r,lines:[{ind,runs:[{t,c}]}],svg:null}}, themes:[{id,n,boxes,region,jo,bk}], acr:{말:{m,jo}}, subj:[…] }
    구역 테마 = 구역 박스 「<id>r」 하나({p, r(구역/쪽), lines:[], svg}) + 구역 밖 박스 — 앱 tmSvgs 가 svg 있는 박스를, tmLines 가 없는 박스를 그린다.
    구역 그림(_task_jo_theme_fix2 §A-3) — 그림 도장을 한 장씩 제자리 PDF 로 떼어 pymupdf 로 원본 그림 해상도(그림 XObject 의 가로·세로 화소) ·
      투명 바탕으로 그려 webp(q90 · 투명 있으면 RGBA)로. 모두 data URI 로 넣은 gz 가 1 MB 를 넘으면 그림은 img\\<k>.webp 따로 두고
      <image href="theme/patent_hr8/img/<k>.webp">(minbeoppdf 저장소 안 자리 · 앱이 창 열 때 받는다) · 넘지 않으면 href="data:image/webp;base64,…".
      모양이 없는 도장(BBox 0 · 내용 「q Q」)은 그릴 것이 없어 건너뛴다.
    압축형 JSON · gzip mtime 0 · 집합·사전 순회는 모두 정렬 → 같은 재료·같은 표면 바이트까지 같다(그림 webp 도 같은 바이트 — 2026-10-02 실측).
  D11 — 쓰기 전에 출력 JSON 을 _d11_scan(메일·휴대전화·토큰 꼴 · 워터마크 해시)으로 본다 · 걸림 0 일 때만 쓴다(값은 안 찍는다).
"""
import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
_d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
    _d_r = _os_r.path.dirname(_d_r)
_sys_r.path.append(_d_r); import _roots   # noqa: E402
import argparse, base64, collections, csv, gzip, hashlib, io, json, math, os, re, statistics, sys, time
from xml.sax.saxutils import escape as _xesc

PDF_NAME = '26특허해례정리omr주석1.pdf'
PDF1_NAME = '26특허해례정리omr프1.pdf'
LAW = '특허법'
WANT_CHARS = 159787          # 지시서 §0-1(채팅 실측) — 박스 글자 합(공백 뺌)
BIG = 200                    # 큰 박스 = 공백 뺀 글자 200 이상
LINE_TOL = 0.6               # 줄 묶음 — 기준선 ±0.6pt
GAP_K = 1.45                 # 글리프 없이 뛴 자리 = 틈 > 박스 글자 폭 중앙값 × 1.45
IND_UNIT = 2.7               # 들여쓰기 = (줄 첫 x − 박스 왼쪽) / 2.7
XREV_TOL = 0.25              # 줄 안 x 역전 = 다음 글자 x0 < 앞 글자 x1 − 0.25pt
NAME_LEN = 24                # 머리 없는 이름 = 첫 줄 24자
SUBJ_MIN = 5                 # 주체 = 본문 빈도 5 이상
F_THEME, F_ACR, F_SUBJ = '테마.csv', '두문자.csv', '주체.txt'
H_THEME = ['id', '이름', '박스', '구역', '조', 'bk']
H_ACR = ['말', '뜻', '조']
# 테마 점 — 기간(_task_jo_theme_fix2 §A-4 · 사용자 10/2 09:27 · 09:37)
GREEN_C = ('#00ff00', '#b1ff00')   # Ink /C (0,1,0) 진한 초록 · (0.694,1,0) 연두(hexcol 로 바꾼 꼴)
GREEN_W = 2.5                      # 굵기 ≥ 2.5pt — 1.3pt 초록(✓ 표·낙서) · 0.78pt 초록 펜 그림은 빠진다(2026-10-02 실측 2.598 = 46 획)
KIGAN = '기간'
# 구역 그림(_task_jo_theme_fix2 §A-3)
IMG_DIR = 'img'                            # 출력 gz 옆 img\<k>.webp
IMG_HREF = 'theme/patent_hr8/img/'         # SVG <image href> — minbeoppdf 저장소 안 자리(앱이 창 열 때 받는다)
IMG_Q, IMG_METHOD = 90, 4                  # webp 손실 q90 · method 4(같은 그림 = 같은 바이트 · 2026-10-02 실측)
EMBED_MAX = 1 << 20                        # 그림을 data URI 로 넣은 테마.json.gz 가 이보다 크면 그림은 따로 파일
BLEND = {'/Multiply': 'multiply', '/Screen': 'screen', '/Overlay': 'overlay', '/Darken': 'darken', '/Lighten': 'lighten',
         '/ColorDodge': 'color-dodge', '/ColorBurn': 'color-burn', '/HardLight': 'hard-light', '/SoftLight': 'soft-light',
         '/Difference': 'difference', '/Exclusion': 'exclusion', '/Hue': 'hue', '/Saturation': 'saturation', '/Color': 'color', '/Luminosity': 'luminosity'}


def P(*a):
    print(*a, flush=True)


def default_paths():
    nr = _roots.need_n('정리omr 주석1 PDF · 표')
    d = os.path.join(nr, 'jopangi', '정리omr')
    return dict(pdf=os.path.join(d, PDF_NAME), pdf1=os.path.join(d, PDF1_NAME), tables=os.path.join(d, '_테마'),
                out=_roots.mbpdf('theme', 'patent_hr8', '테마.json.gz'), jodata=_roots.genie('jo', 'data'))


def md5_file(p):
    m = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            m.update(c)
    return m.hexdigest()


def hexcol(c):
    """pdfplumber non_stroking_color → #rrggbb (회색 1 · RGB 3 · CMYK 4 · None = PDF 기본 검정) · 그 밖 꼴은 멈춘다"""
    if c is None:
        return '#000000'
    if isinstance(c, (int, float)):
        c = (c,)
    if isinstance(c, (list, tuple)) and all(isinstance(v, (int, float)) for v in c):
        if len(c) == 1:
            v = max(0, min(255, round(c[0] * 255)))
            return '#%02x%02x%02x' % (v, v, v)
        if len(c) == 3:
            return '#%02x%02x%02x' % tuple(max(0, min(255, round(v * 255))) for v in c)
        if len(c) == 4:
            C, M, Y, K = c
            return '#%02x%02x%02x' % tuple(max(0, min(255, round(255 * (1 - v) * (1 - K)))) for v in (C, M, Y))
    raise SystemExit('★읽지 못한 글자색 꼴 %r — 판독기를 고쳐야 한다. 멈춘다.' % (c,))


# Adobe-Korea1 순서 밖에 덧붙은 CID — 내장 CFF 에 cmap 이 없고 ToUnicode 도 없어 pdfminer 가 「(cid:N)」 으로 낸다(2026-10-01 실측 4 글리프).
# 글리프를 크게 그려 모양을 보고 정했다: 18353(야놀자 · 맨 끝 글리프 · 폭 0.82pt · 마침표 「.」 0.55pt 와 다른 글리프) = 점 —
#   그 줄은 특허법 제127조 「생산ㆍ양도ㆍ대여」(본문 데이터 U+318D)를 옮긴 줄이라 「ㆍ」 · 18548(애플SD고딕 · 맨 끝 글리프) = 굵은 오른쪽 화살표 「➔」(노트의 화살표는 모두 U+2794).
# 이 표에 없는 「(cid:N)」 이 나오면 멈춘다(짐작으로 채우지 않는다).
CID_FIX = {('YanoljaYacheOTFR', 18353): 'ㆍ', ('AppleSDGothicNeo-Regular', 18548): '➔'}
RX_CIDTXT = re.compile(r'^\(cid:(\d+)\)$')


def fix_cid(text, fontname):
    m = RX_CIDTXT.match(text or '')
    if not m:
        return text
    return CID_FIX.get((str(fontname).split('+', 1)[-1], int(m.group(1))), text)


def fnum(v):
    s = '%.2f' % v
    s = s.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


# ───────────────────────── 1. 박스 뽑기 ─────────────────────────
def extract(pdf_path):
    """돌려줌 dict(boxes=[{k,p,rect(top 기준 pt),W,H,chars:[{t,x0,x1,b,size,c,i}]}], inks=[{p,a,pts,c,w,op}], order={p:[('S',k)|('I',j)]})"""
    import pikepdf, pdfplumber
    src = pikepdf.open(pdf_path)
    dst = pikepdf.new()
    boxes, inks, order = [], [], {}
    for pi, pg in enumerate(src.pages):
        mb = [float(v) for v in pg.MediaBox]
        if mb[0] != 0 or mb[1] != 0 or int(pg.get('/Rotate', 0)) % 360:
            raise SystemExit('★%d쪽 MediaBox 원점·회전이 0 이 아니다 %r — 판독기를 고쳐야 한다. 멈춘다.' % (pi + 1, mb))
        W, H = mb[2], mb[3]
        p = pi + 1
        order[p] = []
        for ai, a in enumerate(pg.get('/Annots', [])):
            st = str(a.get('/Subtype'))
            if st == '/Stamp':
                rc = [float(v) for v in a.Rect]
                x0, y0, x1, y1 = min(rc[0], rc[2]), min(rc[1], rc[3]), max(rc[0], rc[2]), max(rc[1], rc[3])
                n = a.AP.N
                bb = [float(v) for v in n.BBox]
                mt = n.get('/Matrix')
                if mt is not None and [float(v) for v in mt] != [1, 0, 0, 1, 0, 0]:
                    raise SystemExit('★도장 %d쪽 #%d /Matrix 가 단위 행렬이 아니다 — 판독기를 고쳐야 한다. 멈춘다.' % (p, ai))
                bx0, by0, bx1, by1 = min(bb[0], bb[2]), min(bb[1], bb[3]), max(bb[0], bb[2]), max(bb[1], bb[3])
                sx = (x1 - x0) / (bx1 - bx0) if bx1 > bx0 else 1.0
                sy = (y1 - y0) / (by1 - by0) if by1 > by0 else 1.0
                fx = dst.copy_foreign(n)
                page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=[0, 0, W, H],
                                          Resources=pikepdf.Dictionary(XObject=pikepdf.Dictionary(X0=fx)))
                page.Contents = dst.make_stream(('q %.6f 0 0 %.6f %.6f %.6f cm /X0 Do Q' % (sx, sy, x0 - bx0 * sx, y0 - by0 * sy)).encode())
                dst.pages.append(pikepdf.Page(page))
                k = len(boxes)
                boxes.append(dict(k=k, p=p, rect=[x0, H - y1, x1, H - y0], W=W, H=H, chars=[]))
                order[p].append(('S', k))
            elif st == '/Ink':
                strokes = []
                for s in a.get('/InkList', []):
                    v = [float(q) for q in s]
                    strokes.append([(v[i], H - v[i + 1]) for i in range(0, len(v) - 1, 2)])
                c = a.get('/C')
                col = hexcol(tuple(float(q) for q in c)) if c is not None and len(c) else '#000000'
                w = None
                bs = a.get('/BS')
                if bs is not None and bs.get('/W') is not None:
                    w = float(bs.get('/W'))
                elif a.get('/Border') is not None and len(a.get('/Border')) >= 3:
                    w = float(a.get('/Border')[2])
                op = float(a.get('/CA')) if a.get('/CA') is not None else 1.0
                bm = None
                # 형광펜 획 — 모양(/AP /N) ExtGState 의 /CA 0.5 · /BM /Multiply(235 획 · 2026-10-02 실측) — 주석 /CA 가 없으면 모양 값을 쓴다
                #   (안 읽으면 SVG 에서 형광펜이 불투명하게 글자·그림을 덮는다 · fix2 그림 확인에서 찾음)
                ap = a.get('/AP')
                if ap is not None and ap.get('/N') is not None:
                    eg = (ap.N.get('/Resources') or {}).get('/ExtGState') or {}
                    for _nm in sorted(eg.keys(), key=str):
                        g = eg[_nm]
                        if g.get('/BM') is not None and str(g.get('/BM')) not in ('/Normal', '/Compatible'):
                            bm = BLEND.get(str(g.get('/BM')))
                            if bm is None:
                                raise SystemExit('★Ink %d쪽 #%d 섞기 %s 를 모른다 — 판독기를 고쳐야 한다. 멈춘다.' % (p, ai, g.get('/BM')))
                        if a.get('/CA') is None and g.get('/CA') is not None:
                            op = float(g.get('/CA'))
                j = len(inks)
                inks.append(dict(j=j, p=p, pts=strokes, c=col, w=1.0 if w is None else w, op=op, bm=bm))
                order[p].append(('I', j))
    buf = io.BytesIO()
    dst.save(buf)
    buf.seek(0)
    with pdfplumber.open(buf) as pdf:
        if len(pdf.pages) != len(boxes):
            raise SystemExit('★제자리 PDF 쪽 수 %d ≠ 도장 %d — 멈춘다.' % (len(pdf.pages), len(boxes)))
        for b, pg in zip(boxes, pdf.pages):
            for i, c in enumerate(pg.chars):
                m = c.get('matrix')
                if not m or len(m) < 6:
                    raise SystemExit('★글자 matrix 를 못 읽었다(k%d) — 판독기를 고쳐야 한다. 멈춘다.' % b['k'])
                t = fix_cid(c['text'], c.get('fontname'))
                if RX_CIDTXT.match(t) or len(t) != 1:
                    raise SystemExit('★k%d 글리프 %r(글꼴 %s) 를 유니코드로 못 읽었다 — CID_FIX 판독표에 없다. 판독기를 고쳐야 한다. 멈춘다.'
                                     % (b['k'], t, str(c.get('fontname')).split('+', 1)[-1]))
                b['chars'].append(dict(t=t, x0=float(c['x0']), x1=float(c['x1']), b=b['H'] - float(m[5]),
                                       size=float(c['size']), c=hexcol(c.get('non_stroking_color')), i=i))
    return dict(boxes=boxes, inks=inks, order=order, pdf=pdf_path)


def load_pdf1(pdf1_path, pages=(1, 2, 3, 4, 5)):
    """프1 쪽 글자(공백 뺌) — {쪽: [(글, x0, 기준선, 색)]}"""
    import pdfplumber
    out = {}
    with pdfplumber.open(pdf1_path) as pdf:
        for p in pages:
            pg = pdf.pages[p - 1]
            H = float(pg.height)
            out[p] = [(fix_cid(c['text'], c.get('fontname')), float(c['x0']), H - float(c['matrix'][5]), hexcol(c.get('non_stroking_color')))
                      for c in pg.chars if c['text'] != ' ']
    return out


def char_check(boxes, f1, dx_shift=0.0):
    """박스 글자(공백 뺌) 하나하나 → 프1 같은 쪽 같은 글자 · x0·기준선 차 < 0.05pt(한 번만 짝) · 돌려줌 (짝, 못 찾음, 색 같음)
       dx_shift = 헛잣대(박스 글자를 옆으로 민 채 맞대면 짝이 거의 0 이어야 잣대가 산다)"""
    hit = miss = colsame = 0
    for p in sorted({b['p'] for b in boxes}):
        ch = f1.get(p, [])
        idx = collections.defaultdict(list)
        for j, c in enumerate(ch):
            idx[(c[0], round(c[1], 1))].append(j)
        used = set()
        for b in boxes:
            if b['p'] != p:
                continue
            for c in b['chars']:
                if c['t'] == ' ':
                    continue
                x0 = c['x0'] + dx_shift
                found = None
                for dx in (0.0, -0.1, 0.1):
                    for j in idx.get((c['t'], round(round(x0, 1) + dx, 1)), []):
                        if j not in used and abs(ch[j][1] - x0) < 0.05 and abs(ch[j][2] - c['b']) < 0.05:
                            found = j
                            break
                    if found is not None:
                        break
                if found is None:
                    miss += 1
                else:
                    used.add(found)
                    hit += 1
                    if ch[found][3] == c['c']:
                        colsame += 1
    return hit, miss, colsame


def box_layout(b):
    """박스 → lines [{ind, runs:[{t,c}]}] · 부속 = 줄마다 글리프 목록(SVG·검산용) · 글자 폭 중앙값"""
    ns = [c for c in b['chars'] if c['t'] != ' ']
    if not ns:
        return [], [], 0.0
    wmed = statistics.median(sorted(c['x1'] - c['x0'] for c in ns))
    thr = wmed * GAP_K
    rows = []
    for c in sorted(b['chars'], key=lambda c: (c['b'], c['x0'], c['i'])):
        if rows and c['b'] - rows[-1]['b'] <= LINE_TOL:
            rows[-1]['c'].append(c)
        else:
            rows.append(dict(b=c['b'], c=[c]))
    left = b['rect'][0]
    lines, glines = [], []
    for r in rows:
        cs = sorted(r['c'], key=lambda c: (c['x0'], c['i']))
        seq = []      # (글, 색|None, 글리프|None)
        prev = None
        for c in cs:
            if prev is not None and c['t'] != ' ' and prev['t'] != ' ' and c['x0'] - prev['x1'] > thr:
                seq.append((' ', None, None))
            seq.append((c['t'], c['c'] if c['t'] != ' ' else None, c))
            prev = c
        a = 0
        while a < len(seq) and seq[a][0] == ' ':
            a += 1
        z = len(seq)
        while z > a and seq[z - 1][0] == ' ':
            z -= 1
        seq = seq[a:z]
        if not seq:
            continue
        first = seq[0][2]
        ind = max(0, int(math.floor((first['x0'] - left) / IND_UNIT + 0.5)))
        runs = []
        for t, col, _g in seq:
            if t == ' ' or (runs and runs[-1]['c'] == col):
                runs[-1]['t'] += t
            else:
                runs.append({'t': t, 'c': col})
        lines.append({'ind': ind, 'runs': runs})
        glines.append(dict(b=r['b'], g=[c for c in cs], thr=thr))
    return lines, glines, wmed


def xrev_count(glines):
    n = 0
    for gl in glines:
        g = gl['g']
        for i in range(1, len(g)):
            if g[i]['x0'] < g[i - 1]['x1'] - XREV_TOL:
                n += 1
    return n


# ───────────────────────── 2. 조 인용 ─────────────────────────
CIRC = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
RX_CITE = re.compile(r'(?<![0-9.])(?:(제)\s*)?(\d{1,3})(?:(조)(?:의(\d{1,2}))?|-(\d{1,2})(?![0-9.])(?:조)?|의(\d{1,2})|(?=[' + CIRC + ']))')
OTHER_LAW_HEAD2 = ('시규', '민소')                      # 두 글자 머리 — 앞 글자와 상관없이 다른 법(fix1 A-32-1)
OTHER_LAW_HEAD1 = ('상', '디')                          # 한 글자 머리 — 앞이 한글이면 못 가름(fix1 A-32-2)
OTHER_LAW_BEFORE_법 = ('민', '민소', '민집', '민사소송', '민사집행', '상표', '상', '디', '디자인보호', '디보', '실', '실용신안', '실용',
                      '형', '형소', '행소', '행정소송', '헌', '국가배상', '저작권', '부정경쟁', '변리사', '발명진흥')


def cite_law(text, s):
    """인용 시작 자리 s 앞 글자로 법 가르기 → '특허법' | '다른 법' | '못 가름'"""
    j = s
    while j > 0 and re.match(r'[가-힣A-Za-z]', text[j - 1]):
        j -= 1
    run = text[j:s]
    if not run:
        return LAW
    low = run.lower()
    if low.endswith('pct'):
        return '다른 법'
    if run.endswith('령') or run.endswith('규칙'):
        return '다른 법'   # 시행령 · 시행규칙
    for h in OTHER_LAW_HEAD2:
        if run.endswith(h):
            return '다른 법'
    if run.endswith('법'):
        pre = run[:-1]
        for h in OTHER_LAW_BEFORE_법:
            if pre.endswith(h):
                return '다른 법'
        return LAW          # 「법82②」 · 「특허법96조」 · 「본법」
    for h in OTHER_LAW_HEAD1:
        if run.endswith(h):
            return '다른 법' if len(run) == len(h) else '못 가름'
    return LAW              # 「특226조」 · 「무133조」 · 「X55②」 꼴 — 머리 없는 수 = 특허법


def cites(text, jo_keys):
    """→ [(조 짧은꼴 'N'|'N-M', 법 갈래)] — 특허법은 목록에 있는 조만(없는 번호 = '목록 밖')"""
    out = []
    for m in RX_CITE.finditer(text):
        n = int(m.group(2))
        sub = m.group(4) or m.group(5) or m.group(6)
        s = m.start(1) if m.group(1) else m.start(2)
        law = cite_law(text, s)
        short = '%d-%d' % (n, int(sub)) if sub else '%d' % n
        if law == LAW:
            key = '제%d조' % n + ('의%d' % int(sub) if sub else '')
            if key not in jo_keys:
                law = '목록 밖'
        out.append((short, law))
    return out


def jo_sort_key(s):
    m = re.match(r'^(\d+)(?:-(\d+))?$', s)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else (10 ** 6, 0)


def jo_canon(tok):
    """표 조 칸 낱말 → 'N' | 'N-M' (「16②」 → 「16」 · 「36의2」 → 「36-2」 · 「제7조의2」 → 「7-2」) · 못 읽으면 None"""
    m = re.match(r'^\s*(?:제\s*)?(\d{1,3})\s*(?:조)?\s*(?:(?:-|의)\s*(\d{1,2}))?\s*(?:조)?\s*[' + CIRC + r']*\s*$', tok)
    if not m:
        return None
    return m.group(1) + ('-' + m.group(2) if m.group(2) else '')


# ───────────────────────── 3. 조문 재료 ─────────────────────────
def load_jodata(jodir):
    def rd(n):
        return json.load(io.open(os.path.join(jodir, n), encoding='utf-8'))
    mok = rd('jo_특허법_목록.json')
    bon = rd('jo_특허법_본문.json')
    blank = rd('blank_특허.json')
    jo_keys = {j['k'] for j in mok['조']}
    titles = {j['k']: j.get('t', '') for j in mok['조']}
    bk = {}
    for k, e in blank.get('조', {}).items():
        f = [0, 0, 0]
        for r in e.get('행', []):
            for b in (r.get('b') or []):
                kind = b.get('kind')
                if kind in ('내용', '주체', '기간'):
                    f[('내용', '주체', '기간').index(kind)] = 1
        bk[k] = f
    texts = []
    for k in sorted(bon['조'].keys(), key=lambda s: jo_sort_key(re.sub(r'^제(\d+)조(?:의(\d+))?.*$', lambda m: m.group(1) + ('-' + m.group(2) if m.group(2) else ''), s))):
        for r in bon['조'][k].get('행', []):
            if (r.get('k') or [''])[0] in LAW_ROWS:
                texts.append(r.get('t', ''))
    prec = rd(PREC_FILE)
    return dict(jo_keys=jo_keys, titles=titles, bk=bk, texts=texts, prec=prec)


# 본문 JSON 의 법조문 줄 종류 — 꼬리·각주·기타·두문자·FM·R 은 사용자 볼트 메모·태그·개정 이력이라 사전·주체에서 뺀다(2026-10-01 실측)
LAW_ROWS = ('H', '항', '호', '본문')


def key_of_short(s):
    m = re.match(r'^(\d+)(?:-(\d+))?$', s)
    return '제%s조' % m.group(1) + ('의%s' % m.group(2) if m.group(2) else '') if m else None


def bk_of(jos, bkmap):
    f = [0, 0, 0]
    for s in jos:
        v = bkmap.get(key_of_short(s) or '', [0, 0, 0])
        f = [a | b for a, b in zip(f, v)]
    return f


# ───────────────────────── 4. 두문자 · 주체 ─────────────────────────
PARTICLES = sorted(['으로부터', '로부터', '에게서', '에서는', '에서의', '에서도', '에서', '에게는', '에게도', '에게', '으로서', '으로써', '으로는', '으로',
                    '로서', '로써', '로는', '이라는', '이라', '라는', '이나', '이란', '이며', '이고', '이면', '이어야', '이다', '이므로', '이지만',
                    '한다', '하는', '하고', '하여', '하며', '하면', '하지', '할', '한', '함', '해야', '했', '된', '되는', '되어', '되고', '되면', '됨',
                    '와', '과', '은', '는', '이', '가', '을', '를', '의', '에', '로', '도', '만', '등', '들', '께', '나', '란', '며', '고', '면', '까지', '부터', '마다', '보다',
                    '처럼', '만큼', '뿐', '조차', '마저', '밖에', '대로', '라도', '이라도', '으로도', '로도'], key=lambda s: (-len(s), s))
COMMON = {   # 흔한 법률어·풀이말(사전에 없더라도 두문자가 아님) — 초안 거름
    '원칙', '예외', '가능', '불가', '불요', '필요', '인정', '부정', '취지', '요건', '효과', '판례', '학설', '통설', '다수설', '소수설', '견해', '경우', '이유',
    '의미', '대상', '범위', '기준', '시점', '판단', '해석', '적용', '준용', '유추', '근거', '규정', '조문', '법리', '사안', '사례', '문제', '해결', '결론', '비교',
    '구별', '차이', '관계', '정리', '주의', '참고', '개념', '의의', '성질', '종류', '내용', '방법', '절차', '시기', '기간', '효력', '소급', '장래', '당연', '원래',
    '다만', '단서', '본문', '전단', '후단', '각호', '제외', '포함', '해당', '이상', '이하', '초과', '미만', '이내', '전부', '일부', '동일', '유사', '같음', '없음',
    '있음', '불가능', '가능함', '필요함', '아님', '맞음', '틀림', '정답', '오답', '선지', '지문', '기출', '출제', '암기', '중요', '비고', '예시', '보기', '구분',
    '구분하기', '판시사항', '도면', '취소', '무효', '각하', '기각', '인용', '심결', '판결', '결정', '처분', '명령', '통지', '청구', '신청', '제출', '보정', '정정',
    '출원', '등록', '특허', '발명', '실시', '권리', '의무', '침해', '손해', '배상', '보상', '대가', '과실', '고의', '선의', '악의', '민법', '특허법', '상표법',
    '디자인', '실용신안', '민소', '민소법', '상표', '조약', '국내', '국외', '외국', '국제', '원심', '대법원', '하급심', '파기', '환송', '확정', '미확정', '소멸', '발생',
    '자연인', '법인격', '반의사불벌죄', '친고죄', '개방형', '폐쇄형', '물적요건', '인적요건', '주관적요건', '객관적요건',
}


def tok_iter(text):
    """한글로 시작하는 한글·숫자 낱말(공백·기호에서 끊음) · (낱말, 시작, 끝)"""
    for m in re.finditer(r'[가-힣][가-힣0-9]*', text):
        yield m.group(0), m.start(), m.end()


_STEMS = {}


def stems(w):
    """낱말 + 끝 조사·어미를 한두 겹 뗀 꼴(남는 글자 2 이상)"""
    r = _STEMS.get(w)
    if r is not None:
        return r
    out = {w}
    for p in PARTICLES:
        if w.endswith(p) and len(w) - len(p) >= 2:
            s = w[:-len(p)]
            out.add(s)
            for p2 in PARTICLES:
                if s.endswith(p2) and len(s) - len(p2) >= 2:
                    out.add(s[:-len(p2)])
    r = frozenset(out)
    _STEMS[w] = r
    return r


PREC_FILE = 'prec_특허_전문.json'   # 흔한 법률어 = 특허 판례 전문(판시사항·판결요지·전문)에 PREC_MIN 번 이상 나온 낱말(조사 뗀 꼴)
PREC_MIN = 3
SINGLE = set('시후전중상등및각별적성권자인법일월년내외간선신구재타본당동미불무비부제총반초고저대소장단복다그항호')   # 합성어 쪼개기의 한 글자 접사(혼자서는 합성어로 안 본다)
VERB_END = ('다', '요', '하여', '하고', '해야', '하는', '하지', '되는', '되어', '할', '함', '됨', '있는', '없는', '라도', '지만', '므로', '니까', '려면',
            '어야', '아야', '여야', '으면', '면서', '하면', '되면', '때', '때는', '때에', '때까지', '것', '것은', '것이', '뒤', '판례', '사건')
RX_CITE_TOK = re.compile(r'[0-9]+(?:조|항|호)')   # 「시행령5조」 · 「특127조」 꼴 = 조 인용(두문자 아님)


def build_dict(jd):
    """사전 = 조문 법조문 줄·조 제목 낱말(조사 뗀 꼴 포함) ∪ 흔한 법률어(COMMON ∪ 판례 어휘) · 부분 문자열 검사용 낱말 이음(|)"""
    words = set()
    toks = []
    for t in jd['texts'] + [jd['titles'][k] for k in sorted(jd['titles'])]:
        for w, _a, _b in tok_iter(t):
            words |= stems(w)
            toks.append(w)
    flat = '|' + '|'.join(toks) + '|'
    common = set(COMMON)
    pc = collections.Counter()
    for k in sorted(jd.get('prec', {})):
        v = jd['prec'][k]
        for f in ('판시사항', '판결요지', '전문'):
            for w, _a, _b in tok_iter(v.get(f, '') or ''):
                for s in stems(w):
                    pc[s] += 1
    common |= {w for w, n in pc.items() if len(w) >= 2 and n >= PREC_MIN}
    return words, flat, common


def in_dict(w, words, flat, common):
    for s in sorted(stems(w)):
        if s in words or s in common or (len(re.sub(r'[0-9]', '', s)) >= 2 and s in flat):
            return True
    return False


def seg_ordinary(core, D):
    """core 가 사전 낱말(2자 이상)·한 글자 접사·앞뒤 조사로만 나뉘고 그중 2자 이상 낱말이 하나라도 있으면 True(= 흔한 말의 합성)"""
    n = len(core)
    memo = {}

    def f(i, big):
        if i == n:
            return big
        key = (i, big)
        if key in memo:
            return memo[key]
        r = False
        for j in range(n, i, -1):
            piece = core[i:j]
            if len(piece) >= 2 and piece in D:
                r = f(j, True)
            elif len(piece) == 1 and piece in SINGLE:
                r = f(j, big)
            elif piece in TAILS and (j == n and i > 0 or i == 0):
                r = f(j, big) if i == 0 else big
            if r:
                break
        memo[key] = r
        return r
    return f(0, False)


def seg_with(core, D, v):
    """core = 후보 v 한 번 + 2자 이상 사전 낱말들(하나 이상)로만 나뉘면 True — 「존기연출원」 = 「존기연」 + 「출원」"""
    i = core.find(v)
    while i >= 0:
        a, z = core[:i], core[i + len(v):]
        if (a or z) and all(not s or _seg_big_only(s, D) for s in (a, z)):
            return True
        i = core.find(v, i + 1)
    return False


def _seg_big_only(s, D):
    n = len(s)
    ok = [False] * (n + 1)
    ok[0] = True
    for i in range(n):
        if not ok[i]:
            continue
        for j in range(i + 2, n + 1):
            if s[i:j] in D:
                ok[j] = True
    return ok[n]


TAILS = frozenset(PARTICLES)


def acr_candidates(boxes_lay, jd, stat=None):
    """두문자 후보 — 한글 2~8 + 숫자 0~3 · 사전(조문·제목·흔한 법률어 · 그 낱말로만 된 합성어) 밖 ·
       (같은 박스 두 번 이상) 또는 (그 낱말 글자가 모두 검정 아닌 한 색) · 다른 후보 + 사전 낱말로 나뉘는 꼴은 겹침이라 뺀다"""
    words, flat, common = build_dict(jd)
    D = {w for w in words if len(w) >= 2} | common
    occ = collections.defaultdict(list)    # 말 → [(k, 줄 i, 색들, 줄 글)]
    for k in sorted(boxes_lay):
        for li, ln in enumerate(boxes_lay[k]['lines']):
            text = ''.join(r['t'] for r in ln['runs'])
            cols = []
            for r in ln['runs']:
                cols.extend([r['c']] * len(r['t']))
            for w, a, z in tok_iter(text):
                hg = len(re.findall(r'[가-힣]', w))
                dg = len(re.findall(r'[0-9]', w))
                if not (2 <= hg <= 8 and dg <= 3):
                    continue
                occ[w].append((k, li, tuple(cols[a:z]), text))
    rule, out = [], []
    for w in sorted(occ):
        L = occ[w]
        perbox = collections.Counter(k for k, _li, _c, _t in L)
        colored = any(len(set(c)) == 1 and c[0] != '#000000' for _k, _li, c, _t in L)
        if not (max(perbox.values()) >= 2 or colored):
            continue
        if in_dict(w, words, flat, common):
            continue
        rule.append((w, L))
    seg = []
    for w, L in rule:
        core = re.sub(r'[0-9]+', '', w)
        if RX_CITE_TOK.search(w) or core.endswith(VERB_END) or seg_ordinary(core, D):
            continue
        seg.append((w, L))
    cset = sorted({re.sub(r'[0-9]+', '', w) for w, _L in seg})
    for w, L in seg:
        core = re.sub(r'[0-9]+', '', w)
        if any(len(v) >= 2 and v != core and v in core and seg_with(core, D, v) for v in cset):
            continue        # 다른 후보 + 사전 낱말로 된 구(「존기연출원」 = 「존기연」 + 출원) — 앱은 긴 말 먼저 굵게 하니 짧은 쪽만 둔다
        out.append((w, L))
    if stat is not None:
        stat.update(acr_rule=len(rule), acr_seg=len(seg), acr_final=len(out))
    return out


SUBJ_SUFFIX = ('장', '관', '인', '자', '원')
# 주체 아닌 끝맺음 — 낱말이 이것으로 끝나면 뺀다(「우선권주장」 · 「존속기간연장」 · 「권리범위확인」 · 「…출원」 = 신청 행위 · 「천만원」 = 금액)
SUBJ_STOP_END = ('주장', '연장', '확장', '보장', '입장', '시장', '현장', '문장', '등장', '도장', '인장', '성장', '신장', '공장', '확인', '승인', '부인',
                 '요인', '날인', '기인', '오인', '시인', '이자', '문자', '숫자', '투자', '보관', '소관', '외관', '주관', '객관', '통관', '상관', '지원', '자원', '재원',
                 '기원', '복원', '청원', '민원', '근원', '정원', '병원', '연원', '동원', '감원', '증원', '결원', '출원', '만원', '억원', '천원')
SUBJ_STOP = {'자자', '각자', '본인', '개인', '이인', '모든자', '그자', '해당자', '다른자', '한자', '등록자', '원인'}   # 「원인」은 끝맺음이 아니라 낱말째(「출원인」 은 산다)


def subj_candidates(jd):
    """주체 — 법조문 줄에서 「…장 · …관 · …인 · …자(· …원)」 꼴 명사 · 빈도 5 이상 · 조사가 붙어 나온 적이 있는 것만
       (서술격 「공유인 경우」 · 「계속 중인」 꼴은 조사가 안 붙어 빠진다)"""
    cnt, withp = collections.Counter(), collections.Counter()
    for t in jd['texts']:
        for w, _a, _b in tok_iter(t):
            noun, part = None, False
            if w.endswith(SUBJ_SUFFIX):
                noun = w
            else:
                for p in PARTICLES:
                    if w.endswith(p) and len(w) - len(p) >= 2 and w[:-len(p)].endswith(SUBJ_SUFFIX):
                        noun, part = w[:-len(p)], True
                        break
            if not noun or len(noun) < 2 or noun in SUBJ_STOP or noun.endswith(SUBJ_STOP_END):
                continue
            if re.search(r'[0-9]', noun.replace('제3자', '')):
                continue
            cnt[noun] += 1
            if part:
                withp[noun] += 1
    return sorted([(w, n) for w, n in cnt.items() if n >= SUBJ_MIN and withp[w] >= 1], key=lambda x: (-x[1], x[0]))


# ───────────────────────── 5. 표 ─────────────────────────
def read_text_any(path):
    b = open(path, 'rb').read()
    for enc in ('utf-8-sig', 'cp949'):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    raise SystemExit('★%s 를 utf-8 · cp949 로 못 읽었다 — 멈춘다.' % path)


def read_csv(path, header):
    rows = list(csv.reader(io.StringIO(read_text_any(path))))
    if not rows or [h.strip() for h in rows[0]] != header:
        raise SystemExit('★%s 머리 줄이 %s 가 아니다(%r) — 멈춘다.' % (os.path.basename(path), ','.join(header), rows[0] if rows else None))
    out = []
    for i, r in enumerate(rows[1:], 2):
        if not any(c.strip() for c in r):
            continue
        if len(r) > len(header) and any(c.strip() for c in r[len(header):]):
            raise SystemExit('★%s %d줄 칸이 %d 개다(머리 %d) — 쉼표가 든 칸은 따옴표로 감싸야 한다. 멈춘다.' % (os.path.basename(path), i, len(r), len(header)))
        r = (list(r) + [''] * len(header))[:len(header)]
        out.append((i, [c.strip() for c in r]))
    return out


def write_csv_bytes(header, rows):
    s = io.StringIO()
    w = csv.writer(s, lineterminator='\r\n')
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    return ('﻿' + s.getvalue()).encode('utf-8')


def theme_name(lines):
    if not lines:
        return ''
    first = ''.join(r['t'] for r in lines[0]['runs']).strip()
    m = re.match(r'^\{([^{}]+)\}', first)
    if m:
        return m.group(1).strip()
    s2 = re.sub(r'^\d{1,2}(?:[.\-]\d{1,2})*\.\s*', '', first)   # 「1.」 · 단계 번호 「3.3.」 · 「1-1.」 을 뗀다
    m = re.match(r'^\{([^{}]+)\}', s2)
    if m:
        return m.group(1).strip()
    return s2[:NAME_LEN].strip()


def box_text(lay):
    return '\n'.join(''.join(r['t'] for r in ln['runs']) for ln in lay['lines'])


def theme_jos(ks, lay, jd):
    """박스들 글의 특허법 조 인용(짧은꼴 · 번호순) — 표 조 칸 초안 규칙(지금 규칙)"""
    jos = set()
    for k in ks:
        for s, law in cites(box_text(lay[k]), jd['jo_keys']):
            if law == LAW:
                jos.add(s)
    return sorted(jos, key=jo_sort_key)


def draft_tables(X, lay, jd):
    """표 셋 초안(바이트) + 셈 — 큰 박스 70 = 한 줄씩 · 작은 조각·그림 도장은 안 붙인다(표가 정한다 · fix2 §A-1 거리 규칙 걷음) · bk 빈칸"""
    boxes = X['boxes']
    nsc = {b['k']: sum(1 for c in b['chars'] if c['t'] != ' ') for b in boxes}
    big = [b['k'] for b in boxes if nsc[b['k']] >= BIG]
    small = [b['k'] for b in boxes if 0 < nsc[b['k']] < BIG]
    trows = []
    for i, g in enumerate(big, 1):
        trows.append(['t%02d' % i, theme_name(lay[g]['lines']), str(g), '', ' '.join(theme_jos([g], lay, jd)), ''])
    ast = {}
    acr = acr_candidates(lay, jd, ast)
    arows = []
    for w, L in sorted(acr, key=lambda x: (min((k, li) for k, li, _c, _t in x[1]), x[0])):
        jos = set()
        for k, li, _c, t in L:
            for s, law in cites(t, jd['jo_keys']):
                if law == LAW:
                    jos.add(s)
        arows.append([w, '', ' '.join(sorted(jos, key=jo_sort_key))])
    subj = subj_candidates(jd)
    return dict(theme=write_csv_bytes(H_THEME, trows), acr=write_csv_bytes(H_ACR, arows),
                subj=('\n'.join(w for w, _n in subj) + '\n').encode('utf-8'),
                n_theme=len(trows), n_acr=len(arows), n_subj=len(subj), big=big, small=small, att={}, acr_list=acr, subj_list=subj, acr_stat=ast)


def parse_region(s, row, fname):
    nums = re.findall(r'-?\d+(?:\.\d+)?', s)
    if len(nums) != 5:
        raise SystemExit('★%s %d줄 구역 「%s」 — 「쪽 x0 y0 x1 y1」(수 다섯) 꼴이 아니다. 멈춘다.' % (fname, row, s))
    p = int(float(nums[0]))
    x0, y0, x1, y1 = (float(v) for v in nums[1:])
    if not (x1 > x0 and y1 > y0):
        raise SystemExit('★%s %d줄 구역 「%s」 — x1 > x0 · y1 > y0 이어야 한다. 멈춘다.' % (fname, row, s))
    return p, [x0, y0, x1, y1]


def parse_bk(s, row, fname):
    d = re.sub(r'[^01]', '', s)
    if s.strip() == '':
        return None
    if len(d) != 3:
        raise SystemExit('★%s %d줄 bk 「%s」 — 「110」(0·1 셋) 꼴이 아니다. 멈춘다.' % (fname, row, s))
    return [int(c) for c in d]


def read_tables(tdir, nbox):
    ft, fa, fs = (os.path.join(tdir, f) for f in (F_THEME, F_ACR, F_SUBJ))
    themes = []
    seen = set()
    for row, (tid, name, bx, reg, jo, bk) in read_csv(ft, H_THEME):
        if not tid:
            raise SystemExit('★%s %d줄 id 가 비었다 — 멈춘다.' % (F_THEME, row))
        if tid in seen:
            raise SystemExit('★%s %d줄 id 「%s」 가 겹친다 — 멈춘다.' % (F_THEME, row, tid))
        if '|' in tid:
            raise SystemExit('★%s %d줄 id 에 「|」 를 쓸 수 없다 — 멈춘다.' % (F_THEME, row))
        seen.add(tid)
        ks = []
        for tk in bx.replace(',', ' ').split():
            m = re.match(r'^\+?(\d+)$', tk)
            if not m or not (0 <= int(m.group(1)) < nbox):
                raise SystemExit('★%s %d줄 박스 「%s」 — 0~%d 의 k(앞 + 는 있어도 됨)가 아니다. 멈춘다.' % (F_THEME, row, tk, nbox - 1))
            if m.group(1) not in ks:
                ks.append(m.group(1))
        jos = []
        for tk in re.split(r'[\s,·/]+', jo.strip()):
            if not tk:
                continue
            c = jo_canon(tk)
            if c is None:
                raise SystemExit('★%s %d줄 조 「%s」 — 「16」 · 「42-2」 · 「36의2」 꼴이 아니다. 멈춘다.' % (F_THEME, row, tk))
            if c not in jos:
                jos.append(c)
        themes.append(dict(row=row, id=tid, n=name, boxes=ks, region=parse_region(reg, row, F_THEME) if reg.strip() else None,
                           jo=jos, bk=parse_bk(bk, row, F_THEME)))
    acr = collections.OrderedDict()
    for row, (w, m, jo) in read_csv(fa, H_ACR):
        if not w:
            continue
        if w in acr:
            raise SystemExit('★%s %d줄 말 「%s」 가 겹친다 — 멈춘다.' % (F_ACR, row, w))
        jos = []
        for tk in re.split(r'[\s,·/]+', jo.strip()):
            if not tk:
                continue
            c = jo_canon(tk)
            if c is None:
                raise SystemExit('★%s %d줄 조 「%s」 — 「16」 · 「42-2」 꼴이 아니다. 멈춘다.' % (F_ACR, row, tk))
            if c not in jos:
                jos.append(c)
        acr[w] = {'m': m, 'jo': jos}
    subj = []
    for ln in read_text_any(fs).splitlines():
        s = ln.strip()
        if s and not s.startswith('#') and s not in subj:
            subj.append(s)
    return themes, acr, subj


# ───────────────────────── 6. 구역 SVG ─────────────────────────
def svg_runs(gl, inside):
    """한 줄 글리프 → SVG text 조각 — 색이 바뀔 때 · 글리프 없이 뛴 자리 · 공백 둘 이상 · 구역 경계에서 끊는다
       (SVG text 는 연속 공백을 하나로 접으므로 정렬 공백에서 끊어 조각마다 제자리 x 에 둔다) · 앞뒤 공백은 뺀다"""
    runs, cur, prev = [], None, None

    def flush():
        if cur is None:
            return
        gs = cur['g']
        while gs and gs[-1]['t'] == ' ':
            gs = gs[:-1]
        if gs:
            runs.append(dict(c=cur['c'], g=gs))
    for g in gl['g']:
        if not inside(g, gl):
            flush()
            cur, prev = None, None
            continue
        if prev is not None and g['x0'] - prev['x1'] > gl['thr']:
            flush()
            cur = None
        prev = g
        if g['t'] == ' ':
            if cur is not None:
                cur['g'].append(g)
                cur['sp'] += 1
                if cur['sp'] >= 2:
                    flush()
                    cur = None
            continue
        if cur is not None and g['c'] != cur['c']:
            flush()
            cur = None
        if cur is None:
            cur = dict(c=g['c'], g=[], sp=0)
        cur['g'].append(g)
        cur['sp'] = 0
    flush()
    return runs


# ── 구역 그림 도장(_task_jo_theme_fix2 §A-3) ──
_PIC_SRC = {}    # PDF 자리 → (pikepdf.Pdf, [(쪽, 도장 주석, 쪽 높이)] — 도장 차례 = k)
_PIC = {}        # (PDF 자리, k) → 모양 갈래
_WEBP = {}       # (PDF 자리, k) → webp 바이트
_VEC_OPS_PATH = {'m', 'l', 'c', 'v', 'y', 'h', 're'}
_VEC_OPS_IGNORE = {'q', 'Q', 'W', 'W*', 'ri', 'i', 'w', 'j', 'J', 'M', 'd', 'cs', 'CS'}
_VEC_OPS_PAINT = {'f': ('fill', 'nonzero'), 'F': ('fill', 'nonzero'), 'f*': ('fill', 'evenodd'),
                  'S': ('stroke', None), 's': ('stroke', None), 'B': ('both', 'nonzero'), 'B*': ('both', 'evenodd'),
                  'b': ('both', 'nonzero'), 'b*': ('both', 'evenodd')}


def _stamp_list(pdf_path):
    if pdf_path not in _PIC_SRC:
        import pikepdf
        src = pikepdf.open(pdf_path)
        lst = []
        for pi, pg in enumerate(src.pages):
            H = float(pg.MediaBox[3])
            for a in pg.get('/Annots', []):
                if str(a.get('/Subtype')) == '/Stamp':
                    lst.append((pi + 1, a, H))
        _PIC_SRC[pdf_path] = (src, lst)
    return _PIC_SRC[pdf_path][1]


def _form_place(a):
    """도장 Rect · 모양 BBox → (x0, y0, x1, y1 PDF 좌표, sx, sy, tx, ty) — extract() 와 같은 자리 맞춤"""
    rc = [float(v) for v in a.Rect]
    x0, y0, x1, y1 = min(rc[0], rc[2]), min(rc[1], rc[3]), max(rc[0], rc[2]), max(rc[1], rc[3])
    bb = [float(v) for v in a.AP.N.BBox]
    bx0, by0, bx1, by1 = min(bb[0], bb[2]), min(bb[1], bb[3]), max(bb[0], bb[2]), max(bb[1], bb[3])
    sx = (x1 - x0) / (bx1 - bx0) if bx1 > bx0 else 1.0
    sy = (y1 - y0) / (by1 - by0) if by1 > by0 else 1.0
    return x0, y0, x1, y1, sx, sy, x0 - bx0 * sx, y0 - by0 * sy


def _mmul(a, b):
    """PDF 행렬 곱 a×b (a 먼저 적용) — [a b c d e f]"""
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3], a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def _vec_paths(k, a, H):
    """벡터 도장 모양 → [{segs:[(명령, 점…)], fill, fop, rule, stroke, sop, sw}](점 = 쪽 위 기준 pt) · 모르는 연산자·꼴이면 멈춘다(짐작 안 함)"""
    import pikepdf
    n = a.AP.N
    x0, y0, x1, y1, sx, sy, tx, ty = _form_place(a)
    base = [sx, 0, 0, sy, tx, ty]
    res = n.get('/Resources') or {}
    egs = res.get('/ExtGState') or {}
    st = dict(ctm=[1, 0, 0, 1, 0, 0], fc='#000000', sc='#000000', fop=1.0, sop=1.0, lw=1.0)
    stack, path, out = [], [], []

    def P2(x, y):
        m = _mmul(st['ctm'], base)
        X_ = m[0] * x + m[2] * y + m[4]
        Y_ = m[1] * x + m[3] * y + m[5]
        return (X_, H - Y_)

    def col(ops):
        v = tuple(float(q) for q in ops)
        return hexcol(v)
    cur = None
    for operands, op in pikepdf.parse_content_stream(n):
        op = str(op)
        if op == 'q':
            stack.append(dict(st, ctm=list(st['ctm'])))
        elif op == 'Q':
            if stack:
                st = stack.pop()
        elif op == 'cm':
            st['ctm'] = _mmul([float(q) for q in operands], st['ctm'])
        elif op == 're':
            x, y, w, h = (float(q) for q in operands)
            path.append(('M',) + P2(x, y))
            path.append(('L',) + P2(x + w, y))
            path.append(('L',) + P2(x + w, y + h))
            path.append(('L',) + P2(x, y + h))
            path.append(('Z',))
            cur = (x, y)
        elif op == 'm':
            x, y = (float(q) for q in operands)
            path.append(('M',) + P2(x, y))
            cur = (x, y)
        elif op == 'l':
            x, y = (float(q) for q in operands)
            path.append(('L',) + P2(x, y))
            cur = (x, y)
        elif op == 'c':
            v = [float(q) for q in operands]
            path.append(('C',) + P2(v[0], v[1]) + P2(v[2], v[3]) + P2(v[4], v[5]))
            cur = (v[4], v[5])
        elif op == 'v':
            v = [float(q) for q in operands]
            path.append(('C',) + P2(*cur) + P2(v[0], v[1]) + P2(v[2], v[3]))
            cur = (v[2], v[3])
        elif op == 'y':
            v = [float(q) for q in operands]
            path.append(('C',) + P2(v[0], v[1]) + P2(v[2], v[3]) + P2(v[2], v[3]))
            cur = (v[2], v[3])
        elif op == 'h':
            path.append(('Z',))
        elif op in ('sc', 'scn', 'rg', 'g', 'k'):
            st['fc'] = col(operands)
        elif op in ('SC', 'SCN', 'RG', 'G', 'K'):
            st['sc'] = col(operands)
        elif op == 'gs':
            g = egs.get(str(operands[0]))
            if g is None:
                raise SystemExit('★벡터 도장 k%d — ExtGState %s 를 못 찾았다. 멈춘다.' % (k, operands[0]))
            for key in g.keys():
                if key not in ('/Type', '/ca', '/CA', '/SMask', '/BM', '/AIS'):
                    raise SystemExit('★벡터 도장 k%d — ExtGState %s 의 %s 를 모른다. 판독기를 고쳐야 한다. 멈춘다.' % (k, operands[0], key))
            sm = g.get('/SMask')
            if sm is not None and str(sm) != '/None':
                raise SystemExit('★벡터 도장 k%d — ExtGState SMask 는 벡터로 옮기지 못한다. 멈춘다.' % k)
            if g.get('/ca') is not None:
                st['fop'] = float(g.get('/ca'))
            if g.get('/CA') is not None:
                st['sop'] = float(g.get('/CA'))
        elif op == 'w':
            st['lw'] = float(operands[0])
        elif op == 'n':
            path = []
        elif op in _VEC_OPS_PAINT:
            what, rule = _VEC_OPS_PAINT[op]
            if op in ('s', 'b', 'b*'):
                path.append(('Z',))
            m = _mmul(st['ctm'], base)
            scale = math.sqrt(abs(m[0] * m[3] - m[1] * m[2]))
            out.append(dict(segs=list(path), fill=st['fc'] if what in ('fill', 'both') else None, fop=st['fop'], rule=rule,
                            stroke=st['sc'] if what in ('stroke', 'both') else None, sop=st['sop'], sw=st['lw'] * scale))
            path = []
        elif op in _VEC_OPS_IGNORE:
            continue
        else:
            raise SystemExit('★벡터 도장 k%d — 연산자 %s 를 모른다. 판독기를 고쳐야 한다. 멈춘다.' % (k, op))
    return out


def pic_info(X, k):
    """그림 도장(글 없는 도장) 모양 갈래 — kind 'img'(그림 XObject · nat = 가장 큰 그림의 가로·세로 화소) · 'vec'(칠·선 연산 → vec) · 'empty'(그릴 것 없음)"""
    key = (X['pdf'], k)
    if key in _PIC:
        return _PIC[key]
    p, a, H = _stamp_list(X['pdf'])[k]
    n = a.AP.N
    nat = None
    for _nm, o in sorted((n.get('/Resources') or {}).get('/XObject', {}).items(), key=lambda kv: str(kv[0])):
        if str(o.get('/Subtype')) == '/Image':
            wh = (int(o.get('/Width')), int(o.get('/Height')))
            if nat is None or wh[0] * wh[1] > nat[0] * nat[1]:
                nat = wh
        elif str(o.get('/Subtype')) == '/Form':
            raise SystemExit('★그림 도장 k%d 안에 Form XObject — 판독기를 고쳐야 한다. 멈춘다.' % k)
    if nat is not None:
        r = dict(kind='img', nat=nat)
    else:
        vec = _vec_paths(k, a, H)
        r = dict(kind='vec', vec=vec) if vec else dict(kind='empty')
    _PIC[key] = r
    return r


def pic_webp(X, k):
    """그림 도장 k → webp 바이트 — 제자리 한 장 PDF(Rect 크기 쪽 · 모양 XObject 하나) 를 pymupdf 로 원본 그림 해상도 · 투명 바탕으로 그림
       (가로 배율 = 그림 가로 화소 / Rect 가로 pt · 세로도 따로) · 알파가 모두 255 면 RGB · webp q90 method 4"""
    key = (X['pdf'], k)
    if key in _WEBP:
        return _WEBP[key]
    import pikepdf, pymupdf
    from PIL import Image
    info = pic_info(X, k)
    if info['kind'] != 'img':
        raise SystemExit('★k%d 는 그림 도장이 아니다(%s) — 멈춘다.' % (k, info['kind']))
    p, a, H = _stamp_list(X['pdf'])[k]
    x0, y0, x1, y1, sx, sy, tx, ty = _form_place(a)
    W_, H_ = x1 - x0, y1 - y0
    dst = pikepdf.new()
    fx = dst.copy_foreign(a.AP.N)
    page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=[0, 0, W_, H_],
                              Resources=pikepdf.Dictionary(XObject=pikepdf.Dictionary(X0=fx)))
    page.Contents = dst.make_stream(('q %.6f 0 0 %.6f %.6f %.6f cm /X0 Do Q' % (sx, sy, tx - x0, ty - y0)).encode())
    dst.pages.append(pikepdf.Page(page))
    buf = io.BytesIO()
    dst.save(buf)
    doc = pymupdf.open('pdf', buf.getvalue())
    nat = info['nat']
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(nat[0] / W_, nat[1] / H_), alpha=True)
    im = Image.frombytes('RGBA', (pix.width, pix.height), pix.samples)
    if im.getchannel('A').getextrema()[0] == 255:
        im = im.convert('RGB')
    out = io.BytesIO()
    im.save(out, 'WEBP', quality=IMG_Q, method=IMG_METHOD)
    data = out.getvalue()
    doc.close()
    _WEBP[key] = data
    return data


def _vec_svg(v, rx0, ry0):
    d = []
    for s in v['segs']:
        if s[0] == 'Z':
            d.append('Z')
        else:
            pts = s[1:]
            d.append(s[0] + ' '.join('%s %s' % (fnum(pts[i] - rx0), fnum(pts[i + 1] - ry0)) for i in range(0, len(pts), 2)))
    at = ['d="%s"' % ' '.join(d)]
    if v['fill']:
        at.append('fill="%s"' % v['fill'])
        if v['fop'] < 1:
            at.append('fill-opacity="%s"' % fnum(v['fop']))
        if v['rule'] == 'evenodd':
            at.append('fill-rule="evenodd"')
    else:
        at.append('fill="none"')
    if v['stroke']:
        at.append('stroke="%s" stroke-width="%s"' % (v['stroke'], fnum(v['sw'])))
        if v['sop'] < 1:
            at.append('stroke-opacity="%s"' % fnum(v['sop']))
    return '<path %s/>' % ' '.join(at)


def svg_parts(X, lay, p, reg, members=None, pics=None, href=None):
    """구역(쪽 p · [x0,y0,x1,y1] pt 위 기준) 안 — 주석 차례대로 text 조각 · 그림 도장 · Ink path.
       글자 = members(구역 박스 k 집합 · None = 그 쪽 모든 도장 — 옛 꼴) 글리프 중 가운데(x · 기준선 − 0.35×크기)가 구역 안
       그림 도장 = pics(k 집합) — 그림이면 <image href=href(k)> · 벡터면 <path> · 모양 없으면 건너뜀
       Ink = 모든 점이 구역 안
       돌려줌 dict(parts, text, path(Ink), image, vpath(벡터 도장 path), texts(구역 박스 글 — 글리프 줄마다 구역 안 글자 · 테마 점 찾기용))"""
    rx0, ry0, rx1, ry1 = reg
    inside_pt = lambda x, y: rx0 <= x <= rx1 and ry0 <= y <= ry1
    inside_g = lambda g, gl: inside_pt((g['x0'] + g['x1']) / 2, gl['b'] - g['size'] * 0.35)
    pics = pics or set()
    parts, nt, npth, nimg, nvec, texts = [], 0, 0, 0, 0, []
    for kind, idx in X['order'].get(p, []):
        if kind == 'S':
            if idx in pics:
                info = pic_info(X, idx)
                if info['kind'] == 'img':
                    r = X['boxes'][idx]['rect']
                    parts.append('<image x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none" href="%s"/>' % (
                        fnum(r[0] - rx0), fnum(r[1] - ry0), fnum(r[2] - r[0]), fnum(r[3] - r[1]), _xesc(href(idx), {'"': '&quot;'})))
                    nimg += 1
                elif info['kind'] == 'vec':
                    for v in info['vec']:
                        parts.append(_vec_svg(v, rx0, ry0))
                        nvec += 1
                continue
            if members is not None and idx not in members:
                continue
            for gl in lay[idx]['glines']:
                tl = ''.join(g['t'] for g in gl['g'] if inside_g(g, gl)).strip()
                if tl:
                    texts.append(tl)
                for r in svg_runs(gl, inside_g):
                    gs = r['g']
                    parts.append('<text x="%s" y="%s" font-size="%s" fill="%s" textLength="%s" lengthAdjust="spacingAndGlyphs">%s</text>' % (
                        fnum(gs[0]['x0'] - rx0), fnum(gl['b'] - ry0), fnum(gs[0]['size']), r['c'], fnum(gs[-1]['x1'] - gs[0]['x0']),
                        _xesc(''.join(g['t'] for g in gs))))
                    nt += 1
        else:
            ink = X['inks'][idx]
            pts = [q for s in ink['pts'] for q in s]
            if not pts or not all(inside_pt(x, y) for x, y in pts):
                continue
            d = ' '.join('M' + ' L'.join('%s %s' % (fnum(x - rx0), fnum(y - ry0)) for x, y in s) for s in ink['pts'] if s)
            extra = (' stroke-opacity="%s"' % fnum(ink['op'])) if ink['op'] < 1 else ''
            if ink.get('bm'):
                extra += ' style="mix-blend-mode:%s"' % ink['bm']   # 형광펜 = 곱하기 섞기(아래 글자·그림이 비친다 — PDF 모양 그대로)
            parts.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"%s/>' % (
                d, ink['c'], fnum(ink['w']), extra))
            npth += 1
    return dict(parts=parts, text=nt, path=npth, image=nimg, vpath=nvec, texts=texts)


def make_svg(X, lay, p, reg, members=None, pics=None, href=None):
    sp = svg_parts(X, lay, p, reg, members, pics, href)
    W, H = reg[2] - reg[0], reg[3] - reg[1]
    s = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">%s</svg>' % (fnum(W), fnum(H), ''.join(sp['parts']))
    return s, sp


# ───────────────────────── 7. 굽기 ─────────────────────────
def layout_all(X):
    lay = {}
    for b in X['boxes']:
        lines, glines, wmed = box_layout(b)
        lay[b['k']] = dict(lines=lines, glines=glines, wmed=wmed)
    return lay


def green_marks(X, lay):
    """테마 점 「기간」 ① — 초록·연두 형광펜 획(GREEN_C · 굵기 ≥ GREEN_W) → [{j, p, cx, cy, k}]
       k = 획 점 사각 가운데가 든 박스 · 둘 이상이면 획 사각에 가장 가까운 글자의 박스(같으면 작은 사각 · 작은 k) · 없으면 None"""
    out = []
    for ink in X['inks']:
        if ink['c'] not in GREEN_C or ink['w'] < GREEN_W:
            continue
        pts = [q for s in ink['pts'] for q in s]
        if not pts:
            continue
        xs, ys = [q[0] for q in pts], [q[1] for q in pts]
        sb = [min(xs), min(ys), max(xs), max(ys)]
        cx, cy = (sb[0] + sb[2]) / 2, (sb[1] + sb[3]) / 2
        cand = [b for b in X['boxes'] if b['p'] == ink['p'] and b['rect'][0] <= cx <= b['rect'][2] and b['rect'][1] <= cy <= b['rect'][3]]
        k = None
        if len(cand) == 1:
            k = cand[0]['k']
        elif cand:
            best = None
            for b in cand:
                dmin = float('inf')
                for gl in lay[b['k']]['glines']:
                    for g in gl['g']:
                        if g['t'] == ' ':
                            continue
                        gb = [g['x0'], gl['b'] - g['size'] * 0.8, g['x1'], gl['b'] + g['size'] * 0.2]
                        dx = max(0.0, max(gb[0], sb[0]) - min(gb[2], sb[2]))
                        dy = max(0.0, max(gb[1], sb[1]) - min(gb[3], sb[3]))
                        dmin = min(dmin, math.hypot(dx, dy))
                r = b['rect']
                key = (dmin, (r[2] - r[0]) * (r[3] - r[1]), b['k'])
                if best is None or key < best[0]:
                    best = (key, b['k'])
            k = best[1]
        out.append(dict(j=ink['j'], p=ink['p'], cx=cx, cy=cy, k=k, n=len(cand)))
    return out


def bake_full(X, lay, pdf_md5, themes, acr, subj, jd):
    """돌려줌 (obj, raw, blob, info) — info = dict(svg={테마 id: 구역 셈}, bk={테마 id: 점 근거}, imgs={k: webp}(따로 둘 때만),
       mode('none' 구역 그림 없음 · 'embed' data URI · 'file' img\\<k>.webp), gz_embed(data URI 로 넣었을 때 gz 바이트), marks(초록 획))"""
    nsc = {b['k']: sum(1 for c in b['chars'] if c['t'] != ' ') for b in X['boxes']}
    marks = green_marks(X, lay)
    subj_l = sorted(set(subj))

    def build(mode):
        boxes = collections.OrderedDict()
        for b in X['boxes']:
            W, H = b['W'], b['H']
            r = b['rect']
            boxes[str(b['k'])] = {'p': b['p'], 'r': [round(r[0] / W, 5), round(r[1] / H, 5), round(r[2] / W, 5), round(r[3] / H, 5)],
                                  'lines': lay[b['k']]['lines'], 'svg': None}
        if mode == 'embed':
            href = lambda k: 'data:image/webp;base64,' + base64.b64encode(pic_webp(X, k)).decode('ascii')
        else:
            href = lambda k: IMG_HREF + '%d.webp' % k
        tout, svginfo, bkinfo, used = [], {}, {}, set()
        for t in themes:
            ks = list(t['boxes'])
            region = None
            texts = []
            if t['region']:
                p, reg = t['region']
                pw = [b for b in X['boxes'] if b['p'] == p]
                if not pw and p not in X['order']:
                    raise SystemExit('★%s %d줄 구역 쪽 %d 이 PDF 에 없다 — 멈춘다.' % (F_THEME, t['row'], p))
                W, H = X['boxes'][0]['W'], X['boxes'][0]['H']
                mem, keep = [], []
                for k in ks:
                    bb = X['boxes'][int(k)]
                    cx, cy = (bb['rect'][0] + bb['rect'][2]) / 2, (bb['rect'][1] + bb['rect'][3]) / 2
                    (mem if (bb['p'] == p and reg[0] <= cx <= reg[2] and reg[1] <= cy <= reg[3]) else keep).append(k)
                members = {int(k) for k in mem if nsc[int(k)] > 0}
                pics = {int(k) for k in mem if nsc[int(k)] == 0}
                svg, sp = make_svg(X, lay, p, reg, members, pics, href)
                rk = t['id'] + 'r'
                if rk in boxes:
                    raise SystemExit('★구역 박스 열쇠 %s 가 겹친다 — 멈춘다.' % rk)
                rr = [round(reg[0] / W, 5), round(reg[1] / H, 5), round(reg[2] / W, 5), round(reg[3] / H, 5)]
                boxes[rk] = {'p': p, 'r': rr, 'lines': [], 'svg': svg}
                region = {'p': p, 'r': rr}
                # 구역 박스 글자 중 구역 밖(줄 글에서도 빠져 어디에도 안 보일 글자) — 관문 0
                lost = 0
                for k in sorted(members):
                    for gl in lay[k]['glines']:
                        for g in gl['g']:
                            if g['t'] != ' ':
                                gx, gy = (g['x0'] + g['x1']) / 2, gl['b'] - g['size'] * 0.35
                                if not (reg[0] <= gx <= reg[2] and reg[1] <= gy <= reg[3]):
                                    lost += 1
                kinds = {k: pic_info(X, k)['kind'] for k in sorted(pics)}
                used |= {k for k, v in kinds.items() if v == 'img'}
                svginfo[t['id']] = dict(p=p, reg=reg, text=sp['text'], path=sp['path'], image=sp['image'], vpath=sp['vpath'],
                                        bytes=len(svg.encode('utf-8')), members=sorted(members), pics=kinds, lost=lost)
                texts += sp['texts']
                ks = [rk] + keep
            for k in ks:
                if k in boxes and not boxes[k]['svg']:
                    texts += [''.join(r['t'] for r in ln['runs']) for ln in lay[int(k)]['lines']]
            if t['bk'] is not None:
                bk = t['bk']
                bkinfo[t['id']] = dict(src='표')
            else:
                c0 = bk_of(t['jo'], jd['bk'])[0]
                sw = sorted({w for w in subj_l if any(w in s for s in texts)})
                kg = sum(s.count(KIGAN) for s in texts)
                gm = []
                for m in marks:
                    on = (m['k'] is not None and str(m['k']) in t['boxes'])
                    if not on and t['region']:
                        p, reg = t['region']
                        on = m['p'] == p and reg[0] <= m['cx'] <= reg[2] and reg[1] <= m['cy'] <= reg[3]
                    if on:
                        gm.append(m['j'])
                bk = [c0, 1 if sw else 0, 1 if (gm or kg) else 0]
                bkinfo[t['id']] = dict(src='셈', subj=sw, kigan=kg, green=gm)
            tout.append({'id': t['id'], 'n': t['n'], 'boxes': ks, 'region': region, 'jo': t['jo'], 'bk': bk})
        obj = collections.OrderedDict([('pdfMd5', pdf_md5), ('boxes', boxes), ('themes', tout),
                                       ('acr', collections.OrderedDict((w, {'m': v['m'], 'jo': v['jo']}) for w, v in acr.items())),
                                       ('subj', list(subj))])
        raw = json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        return obj, raw, gzip.compress(raw, compresslevel=9, mtime=0), svginfo, bkinfo, used

    obj, raw, blob, svginfo, bkinfo, used = build('file')
    mode, gz_embed, imgs = 'none', None, {}
    if used:
        e = build('embed')
        gz_embed = len(e[2])
        if gz_embed <= EMBED_MAX:
            obj, raw, blob, svginfo, bkinfo, used = e
            mode = 'embed'
        else:
            mode = 'file'
            imgs = {k: pic_webp(X, k) for k in sorted(used)}
    return obj, raw, blob, dict(svg=svginfo, bk=bkinfo, imgs=imgs, mode=mode, gz_embed=gz_embed, marks=marks)


def bake(X, lay, pdf_md5, themes, acr, subj, jd):
    """옛 꼴(하네스 _harness_theme_data 가 부른다) — (obj, raw, blob, 구역 셈)"""
    obj, raw, blob, info = bake_full(X, lay, pdf_md5, themes, acr, subj, jd)
    return obj, raw, blob, info['svg']


def d11_check(raw_text, name):
    """(걸림 수, 꼴 셈) · 스캐너를 못 부르면 None"""
    r = _roots.n_root()
    if not r or not os.path.isfile(os.path.join(r, '_d11_scan.py')):
        return None
    if r not in sys.path:
        sys.path.append(r)
    import _d11_scan
    H = _d11_scan.load_hash()
    if H is None:
        return None
    hits = _d11_scan.scan_text(raw_text, H, name, _d11_scan.load_allow())
    return len(hits), collections.Counter(k for _l, k in hits)


def write_verified(path, data):
    """N: 마이박스 — 한 파일 쓰고 0.5초 뒤 되읽어 대조(인접 파일 섞임 사고 · 2026-09-05)"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    time.sleep(0.5)
    if open(path, 'rb').read() != data:
        raise SystemExit('★되읽기 대조가 어긋났다: %s — 멈춘다.' % path)


def run(pdf, pdf1, tables, out, jodir, check=False, skip_pdf1=False, quiet=False):
    t0 = time.time()
    st = {}
    pdf_md5 = md5_file(pdf)
    X = extract(pdf)
    lay = layout_all(X)
    boxes = X['boxes']
    nsc = {b['k']: sum(1 for c in b['chars'] if c['t'] != ' ') for b in boxes}
    st['box_total'] = len(boxes)
    st['box_text'] = sum(1 for k in nsc if nsc[k] > 0)
    st['chars'] = sum(nsc.values())
    st['line_chars'] = sum(len(re.sub(r' ', '', r['t'])) for k in lay for ln in lay[k]['lines'] for r in ln['runs'])
    st['colors'] = sorted({c['c'] for b in boxes for c in b['chars'] if c['t'] != ' '})
    st['xrev'] = sum(xrev_count(lay[k]['glines']) for k in lay)
    st['lines'] = sum(len(lay[k]['lines']) for k in lay)
    st['inks'] = len(X['inks'])
    st['t_extract'] = time.time() - t0
    if not quiet:
        P('박스 %d(글 있음 %d · 빈 %d) · 글자 %d(줄 글자 %d) · 줄 %d · 색 %d · 줄 안 x 역전 %d · Ink %d · %.1fs' % (
            st['box_total'], st['box_text'], st['box_total'] - st['box_text'], st['chars'], st['line_chars'], st['lines'],
            len(st['colors']), st['xrev'], st['inks'], st['t_extract']))
    if st['chars'] != st['line_chars']:
        raise SystemExit('★줄로 묶은 글자 %d ≠ 박스 글자 %d — 멈춘다.' % (st['line_chars'], st['chars']))
    if not skip_pdf1:
        t1 = time.time()
        hit, miss, colsame = char_check(boxes, load_pdf1(pdf1))
        st['pdf1'] = dict(hit=hit, miss=miss, colsame=colsame)
        if not quiet:
            P('프1 대조 — 짝 %d · 못 찾음 %d · 색 같음 %d · %.1fs' % (hit, miss, colsame, time.time() - t1))
        if miss or hit != st['chars'] or st['chars'] != WANT_CHARS:
            raise SystemExit('★박스 글자 %d · 프1 짝 %d · 못 찾음 %d (지시서 %d) — 어긋났다. 멈춘다.' % (st['chars'], hit, miss, WANT_CHARS))
    jd = load_jodata(jodir)
    have = {f: os.path.isfile(os.path.join(tables, f)) for f in (F_THEME, F_ACR, F_SUBJ)}
    dr = None
    if not all(have.values()) or check:
        dr = draft_tables(X, lay, jd)
        st['draft'] = dict(theme=dr['n_theme'], acr=dr['n_acr'], subj=dr['n_subj'])
    if not all(have.values()):
        if check:
            tdir = os.path.join(_scratch_dir(), '_theme_check_tables')
            os.makedirs(tdir, exist_ok=True)
            for f, key in ((F_THEME, 'theme'), (F_ACR, 'acr'), (F_SUBJ, 'subj')):
                src = os.path.join(tables, f)
                data = open(src, 'rb').read() if have[f] else dr[key]
                with open(os.path.join(tdir, f), 'wb') as fh:
                    fh.write(data)
            tables_used = tdir
        else:
            for f, key in ((F_THEME, 'theme'), (F_ACR, 'acr'), (F_SUBJ, 'subj')):
                if not have[f]:
                    write_verified(os.path.join(tables, f), dr[key])
                    if not quiet:
                        P('초안 → %s' % os.path.join(tables, f))
            tables_used = tables
    else:
        tables_used = tables
    themes, acr, subj = read_tables(tables_used, len(boxes))
    t2 = time.time()
    obj, raw, blob, info = bake_full(X, lay, pdf_md5, themes, acr, subj, jd)
    svginfo, imgs = info['svg'], info['imgs']
    bkd = collections.Counter(''.join(map(str, t['bk'])) for t in obj['themes'])
    st.update(n_theme=len(obj['themes']), n_acr=len(obj['acr']), n_subj=len(obj['subj']), gz=len(blob), raw=len(raw),
              md5=hashlib.md5(blob).hexdigest(), svg=svginfo, pdfMd5=pdf_md5, bkinfo=info['bk'], img_mode=info['mode'],
              gz_embed=info['gz_embed'], imgs={k: (len(v), hashlib.md5(v).hexdigest()) for k, v in imgs.items()},
              marks=info['marks'], bk_dist=dict(sorted(bkd.items(), reverse=True)), t_bake=time.time() - t2)
    if not quiet:
        P('테마.json.gz %d B(풀면 %d) · md5 %s · 박스 %d(구역 박스 %d) · 테마 %d · 두문자 %d · 주체 %d · %.1fs' % (
            len(blob), len(raw), st['md5'], len(obj['boxes']), len(svginfo), st['n_theme'], st['n_acr'], st['n_subj'], st['t_bake']))
        kg = sum(1 for t in obj['themes'] if t['bk'][2])
        P('테마 점 bk(내용·주체·기간) 분포 %s · 기간 켜짐 %d(초록 획 %d · 「기간」 글 %d) · 초록 획 %d(박스 못 찾음 %d)' % (
            ' · '.join('(%s) %d' % (','.join(k), n) for k, n in st['bk_dist'].items()), kg,
            sum(1 for v in info['bk'].values() if v.get('green')), sum(1 for v in info['bk'].values() if v.get('kigan')),
            len(info['marks']), sum(1 for m in info['marks'] if m['k'] is None)))
        P('구역 그림 — %s · 따로 둔 그림 %d 장 %d B · (모두 data URI 로 넣으면 gz %s B · 문턱 %d B)' % (
            info['mode'], len(imgs), sum(len(v) for v in imgs.values()), info['gz_embed'], EMBED_MAX))
        for tid, v in svginfo.items():
            P('  구역 %s — %d쪽 %s · text %d · path %d · 그림 %d · 벡터 %d · %d B · 구역 밖 글자 %d' % (
                tid, v['p'], [fnum(x) for x in v['reg']], v['text'], v['path'], v['image'], v['vpath'], v['bytes'], v['lost']))
    d = d11_check(raw.decode('utf-8'), 'theme/patent_hr8/테마.json.gz')
    if d is None:
        P('[d11] NG — _d11_scan · _d11_hash.txt 를 못 읽었다 · 쓰지 않는다')
        st['d11'] = None
        return st, 2, obj, blob
    st['d11'] = d[0]
    if d[0]:
        P('[d11] 걸림 %d (%s) — 쓰지 않는다 · 값은 안 찍는다' % (d[0], ' · '.join('%s %d' % kv for kv in sorted(d[1].items()))))
        return st, 1, obj, blob
    if not quiet:
        P('[d11] 테마.json · 걸림 0(그림은 글 검사 밖 — minbeoppdf 비공개에만 둔다)')
    img_dir = os.path.join(os.path.dirname(out), IMG_DIR)
    plan = []
    for k in sorted(imgs):
        pth = os.path.join(img_dir, '%d.webp' % k)
        cur = open(pth, 'rb').read() if os.path.isfile(pth) else None
        plan.append((k, pth, imgs[k], 'same' if cur == imgs[k] else ('new' if cur is None else 'diff')))
    stale = sorted(f for f in (os.listdir(img_dir) if os.path.isdir(img_dir) else [])
                   if f.endswith('.webp') and not (f[:-5].isdigit() and int(f[:-5]) in imgs))
    st['img_stale'] = stale
    if stale:
        P('⚠ %s 에 지금 표가 안 쓰는 그림 %d — 지우지 않는다(사람이 본다): %s' % (img_dir, len(stale), ' '.join(stale)))
    if check:
        cur = open(out, 'rb').read() if os.path.isfile(out) else None
        P('--check: 쓰지 않음 · 있는 파일 %s · 그림 같음 %d · 다름 %d · 없음 %d' % (
            '없음' if cur is None else ('같음(바이트)' if cur == blob else '다름 — 만들면 바뀐다'),
            sum(1 for x in plan if x[3] == 'same'), sum(1 for x in plan if x[3] == 'diff'), sum(1 for x in plan if x[3] == 'new')))
        return st, 0, obj, blob
    nw = 0
    for k, pth, data, state in plan:
        if state == 'same':
            continue
        os.makedirs(img_dir, exist_ok=True)
        with open(pth, 'wb') as f:
            f.write(data)
        if open(pth, 'rb').read() != data:
            raise SystemExit('★되읽기 대조가 어긋났다: %s' % pth)
        nw += 1
    st['img_wrote'] = nw
    if plan and not quiet:
        P('그림 %d 장 중 %d 장 씀 → %s' % (len(plan), nw, img_dir))
    if os.path.isfile(out) and open(out, 'rb').read() == blob:
        if not quiet:
            P('변화 없음 — 쓰지 않음(%s)' % out)
        st['wrote'] = False
        return st, 0, obj, blob
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'wb') as f:
        f.write(blob)
    if open(out, 'rb').read() != blob:
        raise SystemExit('★되읽기 대조가 어긋났다: %s' % out)
    st['wrote'] = True
    if not quiet:
        P('썼다 → %s' % out)
    return st, 0, obj, blob


def _scratch_dir():
    import tempfile
    return tempfile.gettempdir()


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser(description='정리omr 테마 재료(테마.json.gz) + 표 초안')
    ap.add_argument('--check', action='store_true', help='만들지 않고 값만')
    ap.add_argument('--tables', help='표 폴더(기본 N: jopangi\\정리omr\\_테마)')
    ap.add_argument('--out', help='출력 파일(기본 MBPDF_ROOT\\theme\\patent_hr8\\테마.json.gz)')
    ap.add_argument('--no-pdf1', action='store_true', help='프1 대조를 건너뜀(하네스 되풀이 굽기 전용)')
    a = ap.parse_args()
    d = default_paths()
    tables = a.tables or d['tables']
    out = a.out or d['out']
    P('정리omr = %s' % d['pdf'])
    P('표 = %s · 출력 = %s · 조문 = %s' % (tables, out, d['jodata']))
    st, rc, _obj, _blob = run(d['pdf'], d['pdf1'], tables, out, d['jodata'], check=a.check, skip_pdf1=a.no_pdf1)
    sys.exit(rc)


if __name__ == '__main__':
    main()
