# Module 20 · GitHub advanced · Assessment

> Lessons 93–98 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`) · everything is
> local: no GitHub account needed for this assessment

## Lab setup

<!-- test: contains=labs ready -->
```bash
bash scripts/new-lab.sh assess-20-practical basic
bash scripts/new-lab.sh assess-20-broken basic
(cd ~/git-practice/assess-20-practical &&
  git tag -a v1.0.0 -m "Release 1.0.0" &&
  echo "green tea" >> menu.txt && git commit -q -am "feat(menu): add green tea (closes #4)" &&
  sed -i 's/cappuccino 3.40/cappuccino 3.50/' prices.txt && git commit -q -am "fix(prices): cappuccino costs 3.50 (fixes #7)" &&
  echo "Open 8-18" >> README.md && git commit -q -am "docs: add opening hours" &&
  echo "chai" >> menu.txt && git commit -q -am "feat(menu): add chai (resolves #9)")
(cd ~/git-practice/assess-20-broken && mkdir -p .github/workflows &&
  printf 'name: check-prices\non:\n  push:\n    branches: [master]\n  pull_request:\njobs:\n  check:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: grep -q espresso prices.txt\n' > .github/workflows/check.yml &&
  git add .github && git commit -q -m "ci: check the price file")
echo "labs ready"
```

## Quiz

1. When does `Fixes #12` in a commit message close issue 12?
2. Why must a label exist before `gh issue edit --add-label` can use it?
3. How does a milestone show progress, and how are issues matched to it?
4. Which extra token scope does the CLI need for GitHub Projects?
5. What is a GitHub Release, compared with a tag?
6. Following semantic versioning, what is the next version after `v1.4.2` for: only fixes; a new feature; a breaking
   change?
7. Which file starts GitHub Actions, and which events can trigger a workflow?
8. Why can a release version never be reused for different content?

<details>
<summary>Answers</summary>

1. When the commit (or the PR that says it) reaches the default branch (lesson 93).
2. Labels are repository objects; unknown names are refused (lesson 94).
3. Closed versus total issues and PRs assigned to it; by exact milestone title (lesson 95).
4. `project` (or `read:project` for reading) (lesson 96).
5. A tag plus a page: title, notes and downloadable assets (lesson 97).
6. `v1.4.3`, `v1.5.0`, `v2.0.0` (lesson 97).
7. A YAML file in `.github/workflows/`; events such as `push`, `pull_request`, tag pushes, `workflow_dispatch` (lesson 98).
8. Users, caches and lock files already refer to it; changed content needs a new version (lesson 97).

</details>

## Practical challenge

In `~/git-practice/assess-20-practical` (tag `v1.0.0` plus four Conventional Commits after it):

1. Decide the next version from the commits (`feat` → minor, only `fix` → patch, `!`/`BREAKING CHANGE` → major) and
   create it as an annotated tag.
2. Write `RELEASE_NOTES.md` for it, generated from the commits: a "Features" section, a "Fixes" section, and a
   "Closes" line listing the issue numbers referenced with closing keywords.

<details>
<summary>Reference solution</summary>

<!-- test: contains=v1.1.0; output -->
```bash
cd ~/git-practice/assess-20-practical
subjects=$(git log --format=%s v1.0.0..HEAD)
if echo "$subjects" | grep -qE '^[a-z]+(\(.+\))?!:|BREAKING CHANGE'; then bump=major
elif echo "$subjects" | grep -qE '^feat'; then bump=minor; else bump=patch; fi
IFS=. read -r major minor patch <<< "$(git describe --abbrev=0 | sed 's/^v//')"
case $bump in major) next="$((major + 1)).0.0" ;; minor) next="$major.$((minor + 1)).0" ;; patch) next="$major.$minor.$((patch + 1))" ;; esac
{
  echo "# Release v$next"
  echo; echo "## Features"; git log --format='- %s' v1.0.0..HEAD --grep='^feat' -E
  echo; echo "## Fixes";    git log --format='- %s' v1.0.0..HEAD --grep='^fix' -E
  echo; echo "Closes: $(git log --format=%s v1.0.0..HEAD | grep -oiE '(close|fix|resolve)(s|d|es|ed)? #[0-9]+' | grep -oE '#[0-9]+' | sort -t'#' -k2 -n | paste -sd' ')"
} > RELEASE_NOTES.md
git add RELEASE_NOTES.md && git commit -q -m "docs: release notes for v$next"
git tag -a "v$next" -m "Release $next"
cat RELEASE_NOTES.md
git describe
```

```text
# Release v1.1.0

## Features
- feat(menu): add chai (resolves #9)
- feat(menu): add green tea (closes #4)

## Fixes
- fix(prices): cappuccino costs 3.50 (fixes #7)

Closes: #4 #7 #9
v1.1.0
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-20-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "annotated tag v1.1.0"               '[ "$(git cat-file -t v1.1.0)" = tag ]'
check "release notes list both features"   'grep -q "add green tea" RELEASE_NOTES.md && grep -q "add chai" RELEASE_NOTES.md'
check "release notes list the fix"         'sed -n "/## Fixes/,/^$/p" RELEASE_NOTES.md | grep -q cappuccino'
check "docs commits are not listed"        '! grep -q "opening hours" RELEASE_NOTES.md'
check "closed issues #4 #7 #9"             'grep -q "Closes: #4 #7 #9" RELEASE_NOTES.md'
```

```text
ok       annotated tag v1.1.0
ok       release notes list both features
ok       release notes list the fix
ok       docs commits are not listed
ok       closed issues #4 #7 #9
```

## Troubleshooting challenge

In `~/git-practice/assess-20-broken`, the team pushes to `main` every day, but the `check-prices` workflow has
never run on a push. Check the workflow file with a script, as a reviewer would:

<!-- test: fail; contains=never runs on pushes to main; output -->
```bash
cd ~/git-practice/assess-20-broken
cat > ../assess-20-check-workflow.sh << 'EOF'
#!/usr/bin/env bash
# check-workflow.sh FILE: does a push to the default branch trigger this workflow?
default=$(git symbolic-ref --short HEAD)
branches=$(sed -n '/^  push:/,/^  [a-z_]*:$/p' "$1" | sed -n 's/.*branches: *\[\(.*\)\]/\1/p' | tr -d ' ')
if [ -z "$branches" ] || echo ",$branches," | grep -q ",$default,"; then echo "ok: runs on pushes to $default"
else echo "problem: push trigger lists [$branches]; the workflow never runs on pushes to $default"; exit 1; fi
EOF
bash ../assess-20-check-workflow.sh .github/workflows/check.yml
```

```text
problem: push trigger lists [master]; the workflow never runs on pushes to main
```

Fix it.

<details>
<summary>Solution</summary>

The push trigger lists `master`, but the default branch is `main` (a template copied from an older repository).
Workflows only run for the branches their trigger names:

<!-- test: contains=ok: runs on pushes to main; output -->
```bash
sed -i 's/branches: \[master\]/branches: [main]/' .github/workflows/check.yml
git commit -q -am "ci: run the price check on pushes to main"
bash ../assess-20-check-workflow.sh .github/workflows/check.yml
```

```text
ok: runs on pushes to main
```

</details>

Verification:

<!-- test: contains=branches: [main]; output -->
```bash
cd ~/git-practice/assess-20-broken
grep -A1 "push:" .github/workflows/check.yml
git log --oneline -1
```

```text
  push:
    branches: [main]
af3a425 (HEAD -> main) ci: run the price check on pushes to main
```

## Real-world scenario

Release day: the milestone "v2.3.0" shows 14 of 16 issues closed. The two open ones are a minor UI glitch and a
database migration that is half done. Product asks you to "just tag it". What do you do?

<details>
<summary>Model answer</summary>

Do not tag unfinished work into a release: move the two open issues to the next milestone (v2.4.0 or a v2.3.1 patch
for the glitch), make sure the half-done migration is not merged or is behind a feature flag, then close the milestone.
Tag `v2.3.0` on the commit CI tested, with release notes generated from the merged PRs, and let the tag trigger the
release workflow (build, publish, deploy). A version is permanent: shipping a broken migration under v2.3.0 forces a
v2.3.1 anyway (lessons 95, 97, 98).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-20-practical ~/git-practice/assess-20-broken ~/git-practice/assess-20-check-workflow.sh
```
