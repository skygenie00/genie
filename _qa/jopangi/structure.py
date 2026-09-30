# -*- coding: utf-8 -*-
"""정리부 줄을 조문 구조(조머리/항/호/목/참고자료)로 찍는다.
   평문 앵커 대신 이 구조 대응으로 재부착한다 — 앵커 다중 문제가 원천적으로 없어진다."""
import re

HEAD = re.compile(r'^\s*제\d+조(?:의\d+)?')
HANG = re.compile(r'^\s*([①-⑳])')
HO   = re.compile(r'^\s*(\d+)\.')
MOK  = re.compile(r'^\s*([가-힣])\.')
REF  = re.compile(r'^\s*\[(전문개정|개정|신설|본조신설|제목개정|종전)')
FNDEF = re.compile(r'^\s*\[\^([^\]]+)\]:')
TAGLINE = re.compile(r'^\s*#[^\s#]\S*')
FM = re.compile(r'^---\s*$')
LINK_ANY = re.compile(r'\[\[([^\[\]]*?)\]\]')
LINK_D   = re.compile(r'\[\[([^\[\]|]*)\|([^\[\]|]*)\]\]')


def unlink(s):
    for _ in range(12):
        s2 = LINK_D.sub(lambda m: m.group(2), s)
        s2 = LINK_ANY.sub(lambda m: m.group(1), s2)
        if s2 == s:
            break
        s = s2
    return s


def demark(s):
    """마크업만 걷어낸다 — 각주참조 [^n] · 블록ID ^x · 임베드 ![[..]] 는 남긴다."""
    s = re.sub(r'<font[^>]*>|</font>', '', s, flags=re.I)
    s = re.sub(r'<span[^>]*>|</span>', '', s, flags=re.I)
    s = re.sub(r'</?u>', '', s, flags=re.I)
    s = s.replace('==', '')
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s, flags=re.S)
    s = re.sub(r'(?<!\*)\*(?!\*)', '', s)
    s = s.replace('~~', '')
    return s


def classify(lines):
    """줄 배열 → [(키, 줄)] · 키는 구조 경로 튜플. 프론트매터는 ('FM',) 로 묶는다."""
    out = []
    hang = None
    ho = None
    ref_i = 0
    etc_i = 0
    in_fm = False
    seen_head = False
    in_tail = False          # 두문자 태그줄·각주정의줄 뒤는 전부 꼬리부다
    for i, ln0 in enumerate(lines):
        # ⚠ 판정은 마크업을 걷어낸 사본으로 한다 — 「==④==」 처럼 형광펜에 싸인
        #    항 번호를 못 읽으면 그 항이 통째로 중복 생성된다(상-제3조 사고).
        ln = demark(unlink(ln0)) if ('=' in ln0 or '*' in ln0 or '<' in ln0
                                     or '[[' in ln0) else ln0
        s = ln.strip()
        if not s:
            out.append((('빈줄', i), ln0))
            continue
        if in_tail:
            # ⚠ 꼬리부의 「① 청구범위 X」 같은 메모줄을 항으로 오인하면 본문에 섞인다
            out.append((('꼬리', i), ln0))
            continue
        if FM.match(ln) and not seen_head:
            in_fm = not in_fm
            out.append((('FM', i), ln0))
            continue
        if in_fm:
            out.append((('FM', i), ln0))
            continue
        if not seen_head and HEAD.match(ln):
            seen_head = True
            out.append((('H',), ln0))
            continue
        if FNDEF.match(ln):
            in_tail = True
            out.append((('각주정의', s.split(']')[0]), ln0))
            continue
        if TAGLINE.match(ln):
            in_tail = True
            out.append((('두문자', etc_i), ln0))
            etc_i += 1
            continue
        m = HANG.match(ln)
        if m:
            hang = m.group(1)
            ho = None
            out.append((('항', hang), ln0))
            continue
        # 목이 호보다 먼저 — '가.' 가 HO 에 안 걸리게 순서 주의
        m = MOK.match(ln)
        if m and ho is not None:
            out.append((('항', hang, '호', ho, '목', m.group(1)) if hang
                        else ('호', ho, '목', m.group(1)), ln0))
            continue
        m = HO.match(ln)
        if m:
            ho = m.group(1)
            out.append((('항', hang, '호', ho) if hang else ('호', ho), ln0))
            continue
        if REF.match(ln):
            out.append((('R', ref_i), ln0))
            ref_i += 1
            continue
        out.append((('기타', etc_i), ln0))
        etc_i += 1
    return out


def body_slots(items, limit=None):
    """항 번호가 없는 조(한 문단짜리 본문)는 '기타'로 떨어진다.
       그런 줄에 ('본문', n) 키를 매겨 구조 대응에 태운다 — 안 그러면
       새 본문이 반영되지 않고 현행 줄이 그대로 남는다(중첩 링크가 살아남는 원인).
       limit = 새 본문이 가진 본문 줄 수. 그보다 뒤의 줄은 사용자 메모이므로 건드리지 않는다."""
    out = []
    n = 0
    seen_struct = False
    for k, ln in items:
        if k[0] in ('항', '호'):
            seen_struct = True
        if k[0] == '기타' and not seen_struct and (limit is None or n < limit):
            out.append((('본문', n), ln))
            n += 1
            continue
        out.append((k, ln))
    return out


def count_body(items):
    return sum(1 for k, _ in body_slots(items) if k[0] == '본문')


def struct_key(k):
    """대응에 쓰는 키 — 빈줄·기타·두문자처럼 위치성 키는 제외한다."""
    return k if k and k[0] in ('H', '항', '호', 'R', '본문') else None
