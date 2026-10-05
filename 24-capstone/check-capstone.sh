#!/usr/bin/env bash
# check-capstone.sh [OWNER/REPO]: grade the capstone
#
# Run inside your capstone repository. Without an argument it checks the local repository; with OWNER/REPO it also
# checks the GitHub side (needs gh, logged in).
# shellcheck disable=SC2016  # the checks are single-quoted on purpose: check() evaluates them later
set -u  # no pipefail: "git log | grep -q" must not fail when grep stops reading early
repo="${1:-}"
missing=0
check() {
  if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; missing=$((missing + 1)); fi
}

echo "== the repository"
check "clean history: no wip/asdf/fix/changes messages" \
  '! git log --all --format=%s | grep -qxiE "(wip|asdf|fix|fix again|changes|first commit|chai \+ latte)"'
check "Conventional Commits on main (merges excepted)" \
  '! git log --no-merges --format=%s main | grep -vqE "^(feat|fix|docs|chore|ci|refactor|test|build)(\(.+\))?!?: "'
check "no .env in any commit" '[ -z "$(git log --all --format=%h -- .env)" ]'
check "no password in any commit" '! git grep -q "Cafe-2026-not-a-real-password" $(git rev-list --all)'
check "no file over 1 MB in any commit" \
  '! git rev-list --objects --all | git cat-file --batch-check="%(objecttype) %(objectsize)" | awk "\$1==\"blob\" && \$2>1000000 {f=1} END {exit !f}"'
check ".gitignore ignores .env" 'git check-ignore -q .env'
check "chai on main, latte at the agreed 3.40" \
  'git show main:application/menu.json | grep -q chai && git show main:application/menu.json | grep -q "\"latte\", \"price\": \"3.40\""'
check "repository checks pass on main" 'git stash -q -u 2> /dev/null; git switch -q main && bash scripts/ci.sh; s=$?; git stash pop -q 2> /dev/null; exit $s'
check "CI and release workflows" '[ -f .github/workflows/ci.yml ] && [ -f .github/workflows/release.yml ]'
check "README and CONTRIBUTING" '[ -f README.md ] && [ -f docs/CONTRIBUTING.md ]'
check "annotated tag v1.0.0 on main" '[ "$(git cat-file -t v1.0.0)" = tag ] && git merge-base --is-ancestor v1.0.0 main'
check "no badly named tags" '[ -z "$(git tag -l | grep -vE "^v[0-9]+\.[0-9]+\.[0-9]+$")" ]'

if [ -n "$repo" ]; then
  echo "== GitHub ($repo)"
  check "main is protected (pull requests required)" \
    "gh api repos/$repo/branches/main/protection --jq .required_pull_request_reviews"
  check "force pushes to main are blocked" \
    "[ \"\$(gh api repos/$repo/branches/main/protection --jq .allow_force_pushes.enabled)\" = false ]"
  check "status check required on main" \
    "gh api repos/$repo/branches/main/protection --jq '.required_status_checks.contexts[]' | grep -q ."
  check "at least one merged pull request" "[ \"\$(gh pr list -R $repo --state merged --json number --jq length)\" -ge 1 ]"
  check "release v1.0.0 with the Helm chart" "gh release view v1.0.0 -R $repo --json assets --jq '.assets[].name' | grep -q '^cafe-.*\.tgz$'"
  check "the release workflow (build, GHCR, deploy) succeeded" \
    "gh run list -R $repo --workflow release --limit 5 --json conclusion --jq '.[].conclusion' | grep -qx success"
  check "the latest CI run on main succeeded" \
    "[ \"\$(gh run list -R $repo --workflow ci --branch main --limit 1 --json conclusion --jq '.[0].conclusion')\" = success ]"
fi

echo
if [ $missing -eq 0 ]; then echo "capstone complete"; else echo "$missing requirement(s) missing"; exit 1; fi
