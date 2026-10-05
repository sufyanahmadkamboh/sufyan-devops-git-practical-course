#!/usr/bin/env bash
# Run lessons exactly as a learner types them, but in a sandbox:
#   * a fresh HOME (your ~/.gitconfig, ~/.ssh and ~/git-practice are never touched)
#   * no system Git config (installers add settings such as core.autocrlf that would change the outputs)
#   * no pager, no editor, no password prompts (a test must never wait for input)
#
#   bash tests/run.sh [--update] [--record DIR] FILE.md [FILE.md ...]
#   LAB_HOME=/some/dir bash tests/run.sh ...      reuse a sandbox HOME between runs
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
py=python3
command -v python3 > /dev/null 2>&1 && python3 -c "" > /dev/null 2>&1 || py=python

# tools installed with "pip install --user" (git-filter-repo, lesson 90) live in the user's scripts folder;
# find it before HOME changes, since on Linux it is inside HOME
user_scripts=$("$py" -c 'import os, sysconfig; print(sysconfig.get_path("scripts", os.name + "_user"))' 2> /dev/null || true)
if [ -n "$user_scripts" ] && command -v cygpath > /dev/null 2>&1; then user_scripts=$(cygpath -u "$user_scripts"); fi

lab_home="${LAB_HOME:-$(mktemp -d)}"
mkdir -p "$lab_home"
# the form Git prints (C:/Users/... on Windows) is what the output masking needs
if pwd -W > /dev/null 2>&1; then masked=$(cd "$lab_home" && pwd -W); else masked=$lab_home; fi

export HOME="$lab_home" MDRUN_HOME="$masked" MDRUN_HOME_POSIX="posix:$lab_home"  # the prefix stops MSYS from converting the path
# the lessons run from a copy of the course inside the sandbox, without .git (see MDRUN_CWD in mdrun.py)
work="$lab_home/git-practical-course"
rm -rf "$work" && mkdir -p "$work"
(cd "$root" && tar --exclude=./.git --exclude=./video --exclude=./tests/out -cf - .) | tar -xf - -C "$work"
export MDRUN_CWD="posix:$work"  # the prefix stops MSYS from converting the path
# kind and kubectl use this file only (never your real ~/.kube/config); masked as ~/.kube/config in outputs
mkdir -p "$lab_home/.kube" && export KUBECONFIG="$lab_home/.kube/config"
GIT_CEILING_DIRECTORIES=$(dirname "$lab_home")  # Git never looks for a repository above the sandbox
export GIT_CEILING_DIRECTORIES
export PATH="$root/tests/shims:$PATH${user_scripts:+:$user_scripts}"  # ssh uses the sandbox ~/.ssh
# a tools folder next to the course (kind, used by project 6 and the capstone), if there is one
if [ -d "$root/../.tools" ]; then tools=$(cd "$root/../.tools" && pwd); export PATH="$PATH:$tools"; fi
export GIT_CONFIG_NOSYSTEM=1 GIT_PAGER=cat PAGER=cat GIT_EDITOR=true GIT_TERMINAL_PROMPT=0
# In a terminal, git log shows branch labels (HEAD -> main); piped into the runner it would not.
# Show them anyway, so the recorded outputs look like your terminal (environment-only config, no file is changed).
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=log.decorate GIT_CONFIG_VALUE_0=short
unset GIT_CONFIG_GLOBAL GIT_DIR GIT_WORK_TREE GIT_ASKPASS SSH_ASKPASS  # never a GUI password dialog

exec "$py" "$root/tests/mdrun.py" "$@"
