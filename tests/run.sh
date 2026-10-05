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
lab_home="${LAB_HOME:-$(mktemp -d)}"
mkdir -p "$lab_home"
# the form Git prints (C:/Users/... on Windows) is what the output masking needs
if pwd -W > /dev/null 2>&1; then masked=$(cd "$lab_home" && pwd -W); else masked=$lab_home; fi

export HOME="$lab_home" MDRUN_HOME="$masked"
export GIT_CONFIG_NOSYSTEM=1 GIT_PAGER=cat PAGER=cat GIT_EDITOR=true GIT_TERMINAL_PROMPT=0
# In a terminal, git log shows branch labels (HEAD -> main); piped into the runner it would not.
# Show them anyway, so the recorded outputs look like your terminal (environment-only config, no file is changed).
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=log.decorate GIT_CONFIG_VALUE_0=short
unset GIT_CONFIG_GLOBAL GIT_DIR GIT_WORK_TREE

py=python3
command -v python3 > /dev/null 2>&1 && python3 -c "" > /dev/null 2>&1 || py=python
exec "$py" "$root/tests/mdrun.py" "$@"
