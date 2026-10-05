# Module 17 · Git hooks · Assessment

> Lessons 82–85 · ⏱ 45 minutes · run every command from the course folder (`git-practical-course/`)

## Lab setup

<!-- test: contains=labs ready -->
```bash
bash scripts/new-lab.sh assess-17-practical basic
bash scripts/new-lab.sh assess-17-broken basic
(cd ~/git-practice/assess-17-broken &&
  printf '#!/bin/sh\ngrep -Eq "^CAFE-[0-9]+: " "$1" || { echo "commit-msg: start with a ticket, e.g. CAFE-12: ..."; exit 1; }\n' > .git/hooks/commit-msg &&
  chmod +x .git/hooks/commit-msg && mkdir -p .githooks && git config core.hooksPath .githooks)
echo "labs ready"
```

## Quiz

1. Where do a clone's hooks live by default, and are they pushed or cloned?
2. Which hook can reject a commit based on its message, and what does it receive as `$1`?
3. What exactly should a `pre-commit` hook check: the working directory or the staged changes? Which command shows them?
4. How can anyone skip `pre-commit` and `commit-msg`?
5. How do teams share hooks, and what one-time step does each clone need?
6. Why must CI run the same checks even when every developer has the hooks installed?
7. Which command runs a hook by hand, without committing?

<details>
<summary>Answers</summary>

1. `.git/hooks/`; neither pushed nor cloned (lesson 82).
2. `commit-msg`; the path of the file holding the message (lesson 84).
3. The staged changes: `git diff --cached` (lesson 83).
4. `git commit --no-verify` (lesson 83).
5. Commit them to a folder such as `.githooks/` and set `git config core.hooksPath .githooks` per clone (lesson 85).
6. Local hooks are optional: skipped with `--no-verify`, not installed, other machines; CI is the enforcement (lesson 85).
7. `git hook run NAME` (lesson 82).

</details>

## Practical challenge

In `~/git-practice/assess-17-practical`, create team hooks in `.githooks/` and activate them:

1. `pre-commit` rejects staged changes with trailing whitespace (use `git diff --cached --check`).
2. `commit-msg` requires a ticket prefix: `CAFE-<number>: description`.
3. Both are committed in the repository, and active in this clone.

<details>
<summary>Reference solution</summary>

<!-- test: contains=CAFE-1: add the team hooks; output -->
```bash
cd ~/git-practice/assess-17-practical
mkdir -p .githooks
printf '#!/bin/sh\nexec git diff --cached --check\n' > .githooks/pre-commit
printf '#!/bin/sh\ngrep -Eq "^CAFE-[0-9]+: " "$1" || { echo "commit-msg: start with a ticket, e.g. CAFE-12: ..."; exit 1; }\n' > .githooks/commit-msg
chmod +x .githooks/pre-commit .githooks/commit-msg
git config core.hooksPath .githooks
git add .githooks && git commit -q -m "CAFE-1: add the team hooks"
git log --oneline -1
```

```text
93670d4 (HEAD -> main) CAFE-1: add the team hooks
```

</details>

Self-check:

<!-- test: absent=MISSING; output -->
```bash
cd ~/git-practice/assess-17-practical
check() { if (eval "$2") > /dev/null 2>&1; then echo "ok       $1"; else echo "MISSING  $1"; fi; }
check "hooks committed"                   'git ls-files .githooks | grep -q commit-msg && git ls-files .githooks | grep -q pre-commit'
check "hooks active in this clone"        '[ "$(git config core.hooksPath)" = .githooks ]'
check "trailing whitespace is rejected"   'echo "mocha   " >> menu.txt && git add menu.txt && ! git commit -q -m "CAFE-2: add mocha"; s=$?; git reset -q --hard; exit $s'
check "a message without ticket fails"    'echo mocha >> menu.txt && git add menu.txt && ! git commit -q -m "add mocha"; s=$?; git reset -q --hard; exit $s'
check "a valid commit passes"             'echo mocha >> menu.txt && git commit -q -am "CAFE-2: add mocha"'
```

```text
ok       hooks committed
ok       hooks active in this clone
ok       trailing whitespace is rejected
ok       a message without ticket fails
ok       a valid commit passes
```

## Troubleshooting challenge

In `~/git-practice/assess-17-broken`, the `commit-msg` hook in `.git/hooks/` should reject messages without a ticket,
but this commit goes through:

<!-- test: contains=add chai; output -->
```bash
cd ~/git-practice/assess-17-broken
echo chai >> menu.txt && git commit -q -am "add chai"
git log --oneline -1
```

```text
87cc231 (HEAD -> main) add chai
```

Find out why and fix it, then undo the bad commit and commit properly.

<details>
<summary>Solution</summary>

Git looks for hooks in `core.hooksPath` when it is set: here `.githooks/`, which is empty, so `.git/hooks/commit-msg`
is ignored:

<!-- test: contains=.githooks; output -->
```bash
git config --show-origin core.hooksPath
git rev-parse --git-path hooks/commit-msg
```

```text
file:.git/config	.githooks
.githooks/commit-msg
```

The team's hooks belong in `.githooks/` (committed): move the hook there.

<!-- test: contains=CAFE-7: add chai; output -->
```bash
mv .git/hooks/commit-msg .githooks/commit-msg
git reset -q --soft HEAD~1
git commit -q -m "add chai" 2>&1 || true
git commit -q -m "CAFE-7: add chai"
git log --oneline -1
```

```text
commit-msg: start with a ticket, e.g. CAFE-12: ...
718a4bf (HEAD -> main) CAFE-7: add chai
```

</details>

Verification:

<!-- test: contains=start with a ticket; output -->
```bash
cd ~/git-practice/assess-17-broken
git commit --allow-empty -m "no ticket" 2>&1 || true
```

```text
commit-msg: start with a ticket, e.g. CAFE-12: ...
```

## Real-world scenario

Your team adds a `gitleaks` pre-commit hook after a leaked key. Two weeks later another key is found in `main`. The
developer says: "the hook was installed". What happened, and what do you change?

<details>
<summary>Model answer</summary>

Local hooks can be bypassed: `--no-verify` in a hurry, a GUI client or IDE committing without hooks, a fresh clone
without the setup step, a commit made on another machine, or a web edit on GitHub. Keep the hook for fast feedback,
but enforce on the server side: a CI job running the same scanner on every PR (required by branch protection), GitHub
secret scanning with push protection, and rotation of the leaked key immediately (lessons 83, 85, 89).

</details>

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/assess-17-practical ~/git-practice/assess-17-broken
```
