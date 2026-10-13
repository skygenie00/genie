# -*- coding: utf-8 -*-
r"""글 그대로 꼴 패치 넣기 — 지시서 패치 txt(⟦N 찾기⟧ · ⟦N 바꿈⟧ · ⟦끝⟧) 를 앱 파일에 차례로 한 번씩 · 2026-10-13 채팅이 만듦(작은 고침 10 분 · 규칙 (96) ④)

  python _qa/_qa_apply_patches.py <패치.txt> <앱 파일> [--expect <LF md5 앞 8 자>]
  칸 글 = 머리 줄 다음 줄부터 다음 머리 줄 앞까지(다음 머리 앞 줄바꿈 하나는 칸 글 아님) · 찾는 글이 딱 1 회가 아니면 멈춤(종료 2) · 넣은 뒤 LF md5 · 바이트를 찍음 · --expect 와 다르면 종료 3.
"""
import hashlib, re, sys

txt, app = sys.argv[1], sys.argv[2]
exp = sys.argv[sys.argv.index('--expect') + 1] if '--expect' in sys.argv else None
L = open(txt, encoding='utf-8').read().split('\n')
P, cur, buf = [], None, []
for line in L:
    m = re.fullmatch(r'⟦(\d+) (찾기|바꿈)⟧|⟦끝⟧', line)
    if m:
        if cur:
            P.append((cur, '\n'.join(buf)))
        if line == '⟦끝⟧':
            cur = None
            break
        cur, buf = line, []
    else:
        buf.append(line)
assert len(P) % 2 == 0, '찾기 · 바꿈 짝이 안 맞음'
s = open(app, encoding='utf-8', newline='').read().replace('\r\n', '\n')
for k in range(0, len(P), 2):
    a, b = P[k][1], P[k + 1][1]
    n = s.count(a)
    if n != 1:
        print('멈춤: %s 찾는 글 %d 회' % (P[k][0], n))
        sys.exit(2)
    s = s.replace(a, b, 1)
open(app, 'w', encoding='utf-8', newline='').write(s)
h = hashlib.md5(s.encode('utf-8')).hexdigest()
print('쌍 %d · LF md5 %s · %d B' % (len(P) // 2, h[:8], len(s.encode('utf-8'))))
if exp and not h.startswith(exp):
    print('멈춤: md5 가 지시서 값 %s 와 다름' % exp)
    sys.exit(3)
