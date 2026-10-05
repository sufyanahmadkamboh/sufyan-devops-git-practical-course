#!/usr/bin/env bash
# check-exam.sh: grade the final exam. Run inside ~/git-practice/exam.
# shellcheck disable=SC2016  # the checks are single-quoted on purpose: check() evaluates them later
set -u  # no pipefail: "git log | grep -q" must not fail when grep stops reading early
score=0
check() {
  if (eval "$3") > /dev/null 2>&1; then echo "ok       $1. $2"; score=$((score + 1)); else echo "MISSING  $1. $2"; fi
}

check 1 "branch winter-menu has the winter menu commit" 'git show winter-menu:winter.txt | grep -q "hot chocolate"'
check 2 "branch seasonal is back" 'git log --oneline seasonal | grep -q "Add pumpkin latte"'
check 3 "the typo in 'Add the meun board' is fixed" \
  'git log --format=%s main | grep -qx "Add the menu board" && ! git log --format=%s main | grep -q meun'
check 4 "debug.log removed from history, *.log ignored" \
  '[ -z "$(git log --format=%h main -- debug.log)" ] && git check-ignore -q debug.log && git log -1 --format=%s main~0 > /dev/null'
check 5 "the stash is committed and the stash list is empty" \
  'git show main:README.md | grep -q "single or double" && [ -z "$(git stash list)" ]'
check 6 "origin points to exam-server.git" 'git remote get-url origin | grep -q "exam-server.git$"'
check 7 "the experimental pricing is reverted (not rewritten)" \
  'git log --format=%s main | grep -q "^Revert \"Add experimental pricing\"" && git log --format=%s main | grep -qx "Add experimental pricing" && ! git show main:prices.txt | grep -q truffle'
check 8 "feature-tea merged, latte at 3.40, green tea on the menu" \
  'git merge-base --is-ancestor feature-tea main && git show main:prices.txt | grep -qx "latte 3.40" && git show main:menu.txt | grep -q "green tea"'
check 9 "main pushed; hotfix pushed and tracking origin/hotfix" \
  '[ "$(git rev-parse main)" = "$(git ls-remote origin refs/heads/main | cut -f1)" ] && [ "$(git rev-parse --abbrev-ref hotfix@{u})" = origin/hotfix ]'
check 10 "annotated v1.0.0 on 'Add prices' (pushed), no v1.0" \
  '[ "$(git cat-file -t v1.0.0)" = tag ] && [ "$(git log -1 --format=%s "v1.0.0^{commit}")" = "Add prices" ] && ! git rev-parse -q --verify refs/tags/v1.0 && git ls-remote --exit-code origin refs/tags/v1.0.0'

echo
echo "score: $score / 10"
