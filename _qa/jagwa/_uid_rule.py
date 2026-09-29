# -*- coding: utf-8 -*-
"""자과 생물·지학 문항 번호 새 꼴(_task_jagwa_uid §A-2) — ⚙ 와 앱(jagwa/index.html jgNewUid)이 같은 규칙

  과목 글자: 생물(bio) B · 지학(earth) G · 물리 = 없음(무변)
  기출(옛 「G회차-순번」): 글자 + (회차+1963) 뒤 두 자리 + '-' + 회차 + '-' + 순번 두 자리   G57-05 → B20-57-05
  비기출: 글자 + 옛 번호에서 갈래 글자 뺀 몸통 + 갈래 글자                                  T012 → B012T · C1-010 → G1-010C
"""
import re

LETTER = {'bio': 'B', 'earth': 'G'}
KIND = {'T': '타기출', 'E': '예상', 'C': '확인'}


def new_uid(subj, old):
    L = LETTER[subj]
    m = re.fullmatch(r'G(\d+)-(\d\d)', old)
    if m:
        rn = int(m.group(1))
        return '%s%s-%s-%s' % (L, str(rn + 1963)[2:], m.group(1), m.group(2))
    if old and old[0] in KIND:
        return L + old[1:] + old[0]
    raise ValueError('모르는 옛 uid 꼴: %r' % old)


def check_row(subj, r):
    """옛 uid 꼴과 행 칸이 맞는가(기출 = 연도·회차 · 비기출 = 유형)"""
    old = r.get('옛uid') or r['uid']
    m = re.fullmatch(r'G(\d+)-(\d\d)', old)
    if m:
        rn = int(m.group(1))
        return r.get('유형') == '기출' and str(r.get('회차')) == str(rn) and str(r.get('연도')) == str(rn + 1963)
    return r.get('유형') == KIND.get(old[:1])
