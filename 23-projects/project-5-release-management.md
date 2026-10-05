# Project 5 · Release management

> Level 24 · Projects · advanced · ⏱ 90 minutes · lessons 58, 67–69, 84, 97

## Brief

The cafe ships its menu as versioned releases. Run three release cycles with branches, Conventional Commits, annotated
tags and a generated changelog, including an urgent fix for an old release that must be **backported**.

```text
 main      ──●──●──────────●──●───────────●──►
               │ v1.0.0     │  │ v1.1.0
 release/1.0   └──●(fix)────┼──┘
                   v1.0.1   │                  (backport with cherry-pick -x)
```

## Requirements

1. Commits use Conventional Commits (`feat:`, `fix:`, `docs:`).
2. Tags `v1.0.0`, `v1.1.0` on `main`; a branch `release/1.0` with tag `v1.0.1`; all tags annotated.
3. The fix is made once on `main` and **cherry-picked with `-x`** to `release/1.0`.
4. A `CHANGELOG.md` with a section per version, generated from the commit subjects between tags.
5. `git describe` on `main` names the latest release.

## Starting point

<!-- test: contains=lab ready -->
```bash
bash scripts/new-lab.sh project-5 basic
cd ~/git-practice/project-5
git log --oneline
```

## Hints

- `git tag -a v1.0.0 -m …`, `git switch -c release/1.0 v1.0.0`, `git cherry-pick -x SHA` (lessons 67, 69).
- Changelog: `git log --format='- %s' vA..vB --no-merges` for each range.

## Reference solution

<details>
<summary>Show the reference solution</summary>

Release 1.0.0 and the next feature:

<!-- test: contains=v1.0.0; output -->
```bash
cd ~/git-practice/project-5
git tag -a v1.0.0 -m "Release 1.0.0"
echo "green tea" >> menu.txt && git commit -q -am "feat(menu): add green tea"
echo "green tea 2.80" >> prices.txt && git commit -q -am "feat(prices): price green tea"
git log --oneline --decorate -3
```

```text
80c7f76 (HEAD -> main) feat(prices): price green tea
bfd032f feat(menu): add green tea
4267004 (tag: v1.0.0) Add prices
```

A bug is reported against 1.0.0 (the espresso is priced too low). Fix it on `main`, then backport:

<!-- test: contains=cherry picked from commit; output -->
```bash
sed -i 's/espresso 2.50/espresso 2.60/' prices.txt && git commit -q -am "fix(prices): espresso costs 2.60"
fix=$(git rev-parse HEAD)
git switch -q -c release/1.0 v1.0.0
git cherry-pick -x "$fix" > /dev/null
git tag -a v1.0.1 -m "Release 1.0.1"
git log -1 --format=%B
```

```text
fix(prices): espresso costs 2.60

(cherry picked from commit a6c6c16811b381c7fbf0487604a2dc361540ada4)
```

Release 1.1.0 from `main`, and generate the changelog:

<!-- test: contains=## v1.1.0; output -->
```bash
git switch -q main
git tag -a v1.1.0 -m "Release 1.1.0"
{
  echo "# Changelog"
  for range in "v1.0.0..v1.1.0 v1.1.0" "v1.0.0..v1.0.1 v1.0.1"; do
    set -- $range
    echo; echo "## $2"; git log --format='- %s' --no-merges "$1"
  done
  echo; echo "## v1.0.0"; echo "- First release"
} > CHANGELOG.md
git add CHANGELOG.md && git commit -q -m "docs: add the changelog"
cat CHANGELOG.md
git describe
```

```text
# Changelog

## v1.1.0
- fix(prices): espresso costs 2.60
- feat(prices): price green tea
- feat(menu): add green tea

## v1.0.1
- fix(prices): espresso costs 2.60

## v1.0.0
- First release
v1.1.0-1-g01111a2
```

</details>

## Self-check

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/project-5
check() { if eval "$2" > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "annotated tags v1.0.0 v1.0.1 v1.1.0" 'for t in v1.0.0 v1.0.1 v1.1.0; do [ "$(git cat-file -t $t)" = tag ] || exit 1; done'
check "v1.0.1 is on release/1.0, not main"  'git merge-base --is-ancestor v1.0.1 release/1.0 && ! git merge-base --is-ancestor v1.0.1 main'
check "the backport records its origin"     'git log -1 --format=%B v1.0.1 | grep -q "cherry picked from commit"'
check "v1.0.1 does not contain green tea"   '! git show v1.0.1:menu.txt | grep -q "green tea"'
check "Conventional Commits since v1.0.0"   '! git log --format=%s --no-merges v1.0.0..main | grep -vqE "^(feat|fix|docs|chore)(\(.+\))?: "'
check "CHANGELOG has a section per version" 'grep -q "## v1.1.0" CHANGELOG.md && grep -q "## v1.0.1" CHANGELOG.md'
check "git describe names the release"      'git describe | grep -q "^v1.1.0"'
```

```text
ok       annotated tags v1.0.0 v1.0.1 v1.1.0
ok       v1.0.1 is on release/1.0, not main
ok       the backport records its origin
ok       v1.0.1 does not contain green tea
ok       Conventional Commits since v1.0.0
ok       CHANGELOG has a section per version
ok       git describe names the release
```

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/project-5
```

Next: [Project 6 · DevOps repository](project-6-devops-repository.md)
