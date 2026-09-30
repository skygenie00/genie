# -*- coding: utf-8 -*-
"""공개 저장소로 나가기 전 개인정보·워터마크 검사 — D11 넷째 가드(_task_env_lanes_fix A-3 · 2026-09-29)

    python _d11_scan.py <파일 …>                 그 파일들
    python _d11_scan.py --staged [--repo <저장소>] 그 저장소 스테이징 blob(없으면 _roots.genie() = GENIE_ROOT)
    python _d11_scan.py --tree <폴더> [...]       폴더 아래 글 파일 전부(.git · node_modules 뺌)
  찾는 것: 메일 꼴 · 한국 휴대전화 꼴(구분자 있음·없음 · +82) · 토큰 꼴(ghp_ · github_pat_ · gho_ · sk- · AKIA · xox · AIza)
           · 워터마크 값(_d11_hash.txt 의 길이·md5 와 맞는 조각 — 8판 · 7판)
  찍는 것: 「파일:줄 · 꼴」 뿐 — **값은 어디에도 찍지 않는다**(화면 · 파일 · 결정로그).
  종료 코드: 0 깨끗 · 1 걸림 · 2 해시 파일 없음·읽기 실패(= 걸림과 같이 밀지 않는다 · fails closed)
  _d11_hash.txt · _d11_allow.txt 는 이 파일 옆(N: 작업 폴더)에만 둔다 — genie 에 안 올린다.
  허용: 개인정보가 아닌 주소(git@github.com · …@users.noreply.github.com · noreply@anthropic.com)는 늘 뺀다.
        _d11_allow.txt 의 「파일 끝 자리 · md5 · 꼴」 줄 = 그 파일의 그 값만 뺀다(값은 두지 않는다 · 워터마크는 뺄 수 없다).
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HASHF = os.path.join(HERE, '_d11_hash.txt')
ALLOWF = os.path.join(HERE, '_d11_allow.txt')
RX_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![A-Za-z0-9])")
RX_PHONE = re.compile(r"(?<![\d+])(?:\+82[-\s.]?1[016789]|01[016789])[-\s.]?\d{3,4}[-\s.]?\d{4}(?!\d)")
RX_TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|ghu_[A-Za-z0-9]{20,}|ghs_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}"
                      r"|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|xox[abprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35})")
RX_SAFE_MAIL = re.compile(r"^(?:git@github\.com|[A-Za-z0-9._%+-]+@users\.noreply\.github\.com|noreply@anthropic\.com)$", re.I)
RX_HANGUL = re.compile(r"[가-힣]+")
SKIP_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.ico', '.pdf', '.zip', '.woff', '.woff2', '.ttf', '.otf', '.mp4', '.mp3', '.bundle')
SKIP_DIR = {'.git', 'node_modules', '__pycache__'}


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def load_hash():
    """[(길이, md5, 이름)] · 파일이 없거나 못 읽으면 None"""
    try:
        rows = []
        for ln in open(HASHF, encoding='utf-8'):
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            L, h, k = ln.split(None, 2)
            rows.append((int(L), h.lower(), k.split()[0]))
        return rows or None
    except Exception:
        return None


def load_allow():
    """[(파일 끝 자리, md5, 꼴)] — 없으면 빈 목록"""
    out = []
    try:
        for ln in open(ALLOWF, encoding='utf-8'):
            ln = ln.split('#', 1)[0].strip()
            if ln:
                p, h, k = ln.split(None, 2)
                out.append((p.replace('\\', '/').lower(), h.lower(), k.strip()))
    except FileNotFoundError:
        pass
    return out


def _allowed(name, allow):
    n = str(name).replace('\\', '/').lower()
    return {h for p, h, _ in allow if n == p or n.endswith('/' + p)}


def scan_text(t, H, name='', allow=()):
    """[(줄 번호, 꼴)] — 값은 돌려주지 않는다"""
    hits = []
    hmap = {}
    for L, h, k in (H or []):
        hmap.setdefault(L, {})[h] = k
    names = {L: v for L, v in hmap.items() if any(k.endswith('name') for k in v.values())}
    ok = _allowed(name, allow)
    for i, line in enumerate(t.split('\n'), 1):
        kinds = []
        for m in RX_MAIL.finditer(line):
            v = m.group(0)
            k = hmap.get(len(v), {}).get(md5(v))
            if k:
                kinds.append('워터마크(%s)' % k)
            elif not RX_SAFE_MAIL.match(v) and md5(v) not in ok:
                kinds.append('메일 꼴')
        for m in RX_PHONE.finditer(line):
            v = m.group(0); d = re.sub(r'\D', '', v)
            if d.startswith('82'):
                d = '0' + d[2:]
            k = hmap.get(len(d), {}).get(md5(d)) or hmap.get(len(v), {}).get(md5(v))
            if k:
                kinds.append('워터마크(%s)' % k)
            elif md5(d) not in ok and md5(v) not in ok:
                kinds.append('휴대전화 꼴')
        if RX_TOKEN.search(line):
            kinds.append('토큰 꼴')
        if names:
            for m in RX_HANGUL.finditer(line):
                run = m.group(0)
                for L, hs in names.items():
                    for j in range(0, len(run) - L + 1):
                        k = hs.get(md5(run[j:j + L]))
                        if k:
                            kinds.append('워터마크(%s)' % k)
        for k in dict.fromkeys(kinds):
            hits.append((i, k))
    return hits


def texts_from_files(paths):
    for p in paths:
        if p.lower().endswith(SKIP_EXT):
            continue
        try:
            b = open(p, 'rb').read()
        except Exception:
            yield p, None; continue
        try:
            yield p, b.decode('utf-8')
        except UnicodeDecodeError:
            continue   # 글 아닌 파일(바이너리) — 건너뜀


def texts_from_staged(repo):
    names = subprocess.run(['git', '-C', repo, '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
                           capture_output=True).stdout.decode('utf-8').split('\n')
    for n in [x for x in names if x]:
        if n.lower().endswith(SKIP_EXT):
            continue
        b = subprocess.run(['git', '-C', repo, 'show', ':' + n], capture_output=True).stdout
        try:
            yield n, b.decode('utf-8')
        except UnicodeDecodeError:
            continue


def walk(dirs):
    for d in dirs:
        for dp, dns, fns in os.walk(d):
            dns[:] = [x for x in dns if x not in SKIP_DIR]
            for fn in fns:
                yield os.path.join(dp, fn)


def main(argv):
    H = load_hash()
    allow = load_allow()
    if '--staged' in argv:
        repo = argv[argv.index('--repo') + 1] if '--repo' in argv else None
        if not repo:
            sys.path.append(HERE)
            import _roots
            repo = _roots.genie()
        src = texts_from_staged(repo); what = '스테이징(%s)' % repo
    elif '--tree' in argv:
        ds = [a for a in argv[argv.index('--tree') + 1:] if not a.startswith('--')]
        src = texts_from_files(walk(ds)); what = '폴더 %d' % len(ds)
    else:
        fs = [a for a in argv if not a.startswith('--')]
        src = texts_from_files(fs); what = '파일 %d' % len(fs)
    nfile = nhit = 0; bad = []
    for name, t in src:
        nfile += 1
        if t is None:
            bad.append(name); continue
        for ln, k in scan_text(t, H, name, allow):
            nhit += 1
            print('[d11] %s:%d · %s' % (name, ln, k))
    if bad:
        print('[d11] 못 읽음 %d' % len(bad))
    if H is None:
        print('[d11] NG — 워터마크 해시 파일(_d11_hash.txt)을 못 읽었다 · 밀지 않는다')
        return 2
    print('[d11] %s · 글 파일 %d · 걸림 %d%s' % (what, nfile, nhit, '' if not nhit else ' — 밀지 않는다'))
    return 1 if (nhit or bad) else 0


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(errors='replace')   # 콘솔 기본 인코딩 그대로(g_push 의 CP949 창) · 못 쓰는 글자만 바꿈
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
