# -*- coding: utf-8 -*-
"""_qa_trace — 하네스가 실제로 읽은 파일과 쓴 파일을 적는다(_task_qa_baseline A-1 · A-3 · 입력은 짐작 말고 잰다).
   _qa_chain.py 가 PYTHONPATH 맨 앞에 이 폴더를 두고 아래 환경을 넘긴다 — QA_TRACE_OUT 이 없으면 아무것도 안 한다.
     QA_TRACE_OUT   적을 파일(줄마다 JSON · 하위 파이썬 프로세스도 같은 파일에 덧붙인다 · pid 칸)
     QA_TRACE_ROOTS 「이름=자리」 를 ; 로 이음(genie · n · spd · mbpdf) — 자리 밖(임시 폴더 · 파이썬 설치)은 안 적는다
     QA_TRACE_BAK   쓰기 · 지우기 전에 원래 파일을 떠 둘 폴더(실행기가 하네스가 끝난 뒤 되돌린다)
   적는 것: open(읽기) · mod(끝날 때 올라온 모듈 파일) · w(쓰기로 연 파일 · 지운 파일 · 옮긴 파일 — 처음 한 번만 · 원래 있던 것은 떠 둔다)
            · mkdir(새로 만든 폴더)"""
import os as _o
_OUT = _o.environ.get('QA_TRACE_OUT')
if _OUT:
    import atexit as _ax, builtins as _bi, io as _io, json as _js, shutil as _sh, sys as _sy
    _BAK = _o.environ.get('QA_TRACE_BAK') or ''
    _R = []
    for _kv in (_o.environ.get('QA_TRACE_ROOTS') or '').split(';'):
        if '=' in _kv:
            _n, _p = _kv.split('=', 1)
            if _p:
                _R.append((_n, _o.path.normcase(_o.path.abspath(_p)).rstrip('\\/') + _o.sep))
    _R.sort(key=lambda x: -len(x[1]))
    _SEEN = set()
    _open0 = _bi.open
    _mk0, _mkd0 = _o.mkdir, _o.makedirs
    _rm0, _ul0, _rp0, _rn0, _rt0 = _o.remove, _o.unlink, _o.replace, _o.rename, _sh.rmtree

    def _rel(p):
        try:
            a = _o.path.normcase(_o.path.abspath(_o.fspath(p)))
        except Exception:
            return None
        for n, r in _R:
            if a.startswith(r):
                return n, a[len(r):].replace('\\', '/')
        return None

    def _log(d):
        d['pid'] = _o.getpid()
        try:
            with _open0(_OUT, 'a', encoding='utf-8') as f:
                f.write(_js.dumps(d, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def _rec(kind, p):
        x = _rel(p)
        if not x or (kind, x) in _SEEN:
            return
        _SEEN.add((kind, x))
        _log({'k': kind, 'r': x[0], 'p': x[1]})

    def _guard(p, how):
        # 쓰기 · 지우기 바로 앞 — 자리 안 파일이면 한 번만 적고, 원래 있던 파일은 BAK 에 떠 둔다(이미 떠 두었으면 그대로)
        x = _rel(p)
        if not x or ('w', x) in _SEEN:
            return
        _SEEN.add(('w', x))
        a = _o.path.abspath(_o.fspath(p))
        ex = _o.path.isfile(a)
        d = {'k': 'w', 'r': x[0], 'p': x[1], 'how': how, 'new': not ex}
        if ex and _BAK:
            b = _o.path.join(_BAK, x[0], *x[1].split('/'))
            if not _o.path.exists(b):
                try:
                    _mkd0(_o.path.dirname(b), exist_ok=True)
                    with _open0(a, 'rb') as s, _open0(b, 'wb') as t:
                        t.write(s.read())
                    d['bak'] = 1
                except Exception as e:
                    d['bakerr'] = str(e)[:120]
            else:
                d['bak'] = 1
        _log(d)

    def _open(file, mode='r', *a, **k):
        try:
            if isinstance(file, (str, bytes, _o.PathLike)):
                if any(c in mode for c in 'wax+'):
                    _guard(file, 'open:' + mode)
                else:
                    _rec('open', file)
        except Exception:
            pass
        return _open0(file, mode, *a, **k)

    def _remove(p, *a, **k):
        try:
            _guard(p, 'remove')
        except Exception:
            pass
        return _rm0(p, *a, **k)

    def _unlink(p, *a, **k):
        try:
            _guard(p, 'unlink')
        except Exception:
            pass
        return _ul0(p, *a, **k)

    def _replace(s, d, *a, **k):
        try:
            _guard(s, 'replace-src')
            _guard(d, 'replace-dst')
        except Exception:
            pass
        return _rp0(s, d, *a, **k)

    def _rename(s, d, *a, **k):
        try:
            _guard(s, 'rename-src')
            _guard(d, 'rename-dst')
        except Exception:
            pass
        return _rn0(s, d, *a, **k)

    def _rmtree(p, *a, **k):
        try:
            if _rel(p) and _o.path.isdir(p):
                for dp, dns, fns in _o.walk(p):
                    for fn in fns:
                        _guard(_o.path.join(dp, fn), 'rmtree')
                _log({'k': 'rmtree', 'r': _rel(p)[0], 'p': _rel(p)[1]})
        except Exception:
            pass
        return _rt0(p, *a, **k)

    def _mkdir(p, *a, **k):
        try:
            x = _rel(p)
            if x and not _o.path.isdir(p):
                _log({'k': 'mkdir', 'r': x[0], 'p': x[1]})
        except Exception:
            pass
        return _mk0(p, *a, **k)

    _bi.open = _open
    _io.open = _open
    _o.remove, _o.unlink, _o.replace, _o.rename, _o.mkdir = _remove, _unlink, _replace, _rename, _mkdir
    _sh.rmtree = _rmtree

    def _mods():
        for m in list(_sy.modules.values()):
            f = getattr(m, '__file__', None)
            if f:
                _rec('mod', f)
    _ax.register(_mods)
