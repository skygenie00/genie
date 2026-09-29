# -*- coding: utf-8 -*-
"""앱 저장소 자리 한 곳 — GENIE_ROOT · SPD_ROOT · MBPDF_ROOT (_task_env_lanes 2026-09-29 A-1)

  하네스·⚙·도구가 어느 사본(본 폴더 · 워크트리 · 클라우드)에서 돌든 **그 사본**을 재게 한다.
    genie(*parts)  = GENIE_ROOT(genie 공개 저장소)        아래 parts · 없으면 ~/Documents/genie
    spd(*parts)    = SPD_ROOT(studyplandata 기록·데이터)   아래 parts · 없으면 ~/Documents/studyplandata
    mbpdf(*parts)  = MBPDF_ROOT(minbeoppdf 교재)           아래 parts · 없으면 ~/Documents/minbeoppdf
  환경변수가 없으면 지금까지의 자리 그대로다(옛 판 무변).

  부르는 쪽 머리(파일마다 한 번 · 위 폴더로 올라가며 이 파일을 찾는다 · N: 에서도 genie/_qa/ 사본에서도 같다):
    import os as _os_r, sys as _sys_r   # env_lanes — _roots.py 를 위 폴더에서 찾는다
    _d_r = _os_r.path.dirname(_os_r.path.abspath(__file__))
    while not _os_r.path.isfile(_os_r.path.join(_d_r, '_roots.py')) and _os_r.path.dirname(_d_r) != _d_r:
        _d_r = _os_r.path.dirname(_d_r)
    _sys_r.path.append(_d_r); import _roots   # noqa: E402

  ⚠ 기본 자리 글자는 **이 파일에만** 둔다 — 자리 전수 잣대(_harness_env_lanes.py B-1)가 이 파일만 뺀다.
"""
import os
import subprocess

_HOME = os.path.expanduser('~')
DEFAULT = {
    'GENIE_ROOT': os.path.join(_HOME, 'Documents', 'genie'),
    'SPD_ROOT': os.path.join(_HOME, 'Documents', 'studyplandata'),
    'MBPDF_ROOT': os.path.join(_HOME, 'Documents', 'minbeoppdf'),
}


def root(var):
    v = os.environ.get(var)
    return v if v else DEFAULT[var]


def genie(*parts):
    return os.path.join(root('GENIE_ROOT'), *parts)


def spd(*parts):
    return os.path.join(root('SPD_ROOT'), *parts)


def mbpdf(*parts):
    return os.path.join(root('MBPDF_ROOT'), *parts)


def _norm(p):
    return os.path.normcase(os.path.normpath(os.path.abspath(p)))


def is_default(var='GENIE_ROOT'):
    """그 변수가 가리키는 자리가 기본 자리(본 폴더)인가 — 워크트리·클라우드 사본이면 False"""
    return _norm(root(var)) == _norm(DEFAULT[var])


def branch(repo=None):
    """저장소의 지금 브랜치 이름(분리된 HEAD 면 '')"""
    r = subprocess.run(['git', '-C', repo or root('GENIE_ROOT'), 'branch', '--show-current'], capture_output=True, text=True)
    return (r.stdout or '').strip()


def base_rev(repo=None):
    """헛잣대(바탕) 판 — main 이면 HEAD · 워크트리 브랜치면 분기점(git merge-base main HEAD) (_task_env_lanes A-4-1)"""
    repo = repo or root('GENIE_ROOT')
    if branch(repo) in ('main', ''):
        return 'HEAD'
    r = subprocess.run(['git', '-C', repo, 'merge-base', 'main', 'HEAD'], capture_output=True, text=True)
    return (r.stdout or '').strip() or 'HEAD'
