# Lesson 82 · What are Git hooks?

> Level 17 · Git hooks · ⏱ 15 minutes

## What are we learning?

Hooks are scripts Git runs automatically at certain moments: before a commit, after a checkout, before a push, when
a server receives a push. They let you automate checks and tasks. We look at where they live, write a first one, and
see the most common reason a hook "does nothing".

## Visual

```text
 Git operation          hook (script in .git/hooks/, exact name, executable)     effect
 ─────────────          ─────────────────────────────────────────────────         ──────────────────────────
 git commit       ──►   pre-commit        exit ≠ 0 → commit aborted              checks on the staged files
                        commit-msg        exit ≠ 0 → commit aborted              checks on the message
                        post-commit       (informational)                        notifications, logs
 git push         ──►   pre-push          exit ≠ 0 → push aborted                run tests before pushing
 server receives  ──►   pre-receive       exit ≠ 0 → push rejected               branch protection (lesson 59)
```

## Lab setup

<!-- test: contains=lesson-82 -->
```bash
bash scripts/new-lab.sh lesson-82 basic
cd ~/git-practice/lesson-82
```

## Demonstration

Every new repository comes with sample hooks (disabled: they end in `.sample`):

<!-- test: contains=pre-commit.sample; output -->
```bash
ls .git/hooks
```

```text
applypatch-msg.sample
commit-msg.sample
fsmonitor-watchman.sample
post-update.sample
pre-applypatch.sample
pre-commit.sample
pre-merge-commit.sample
pre-push.sample
pre-rebase.sample
pre-receive.sample
prepare-commit-msg.sample
push-to-checkout.sample
sendemail-validate.sample
update.sample
```

A first hook: after every commit, append a line to a local log.

<!-- test: contains=post-commit -->
```bash
cat > .git/hooks/post-commit << 'EOF'
#!/bin/sh
# post-commit: record every commit in a local log
echo "$(git log -1 --format='%h %s')" >> .git/commit-log.txt
EOF
chmod +x .git/hooks/post-commit
ls .git/hooks | grep -v sample
```

<!-- test: contains=Add green tea; output -->
```bash
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
cat .git/commit-log.txt
```

```text
6013d88 Add green tea
```

## Command breakdown

| Command / path | Use |
|---|---|
| `.git/hooks/NAME` | a hook for this clone (exact name, no extension, executable, with a `#!` line) |
| `git hook run NAME` | run a hook manually to test it |
| `git hook list NAME` | which hook scripts Git would run |
| `git config core.hooksPath DIR` | use hooks from another directory (lesson 85) |
| `git commit --no-verify` | skip `pre-commit` and `commit-msg` (lesson 83) |

## Hands-on exercise

**Instructions.** Run the post-commit hook by hand, without committing.

**Expected result.** A second line in `.git/commit-log.txt` (the same commit again).

<!-- test-run: cd ~/git-practice/lesson-82 && git hook run post-commit -->

**Verification.**

<!-- test: contains=2 -->
```bash
cd ~/git-practice/lesson-82
wc -l < .git/commit-log.txt
```

## Break it

A colleague writes a `pre-commit` hook that should block commits containing `TODO`, saving it as a nicely named
script file:

<!-- test: contains=TODO; output -->
```bash
cat > .git/hooks/pre-commit.sh << 'EOF'
#!/bin/sh
if git diff --cached | grep -q "^+.*TODO"; then echo "pre-commit: remove the TODO first"; exit 1; fi
EOF
chmod +x .git/hooks/pre-commit.sh
echo "TODO: add prices for tea" >> menu.txt && git commit -q -am "Add a TODO" && git log --oneline -1
```

```text
6760c7b (HEAD -> main) Add a TODO
```

## Troubleshoot

The commit went through: the hook never ran. Git looks for a file named exactly `pre-commit`; `pre-commit.sh` is just a
file. Ask Git:

<!-- test: fail; contains=pre-commit; output -->
```bash
git hook run pre-commit 2>&1
```

```text
error: cannot find a hook named pre-commit
```

## Fix

Rename it, undo the bad commit, and try again:

<!-- test: fail; contains=remove the TODO first; output -->
```bash
mv .git/hooks/pre-commit.sh .git/hooks/pre-commit
git reset -q --soft HEAD~1
git commit -m "Add a TODO" 2>&1
```

```text
pre-commit: remove the TODO first
```

The hook ran and blocked the commit (exit status 1).

## Real-world example

Teams use hooks for fast local feedback: formatting (`terraform fmt`, `black`), linting (`helm lint`,
`shellcheck`), secret scanning (`gitleaks protect --staged`), commit message rules. Because hooks live in `.git/`,
they are **not** cloned or pushed: sharing them needs a convention (lesson 85), and the same checks must also run in
CI, where nobody can skip them.

## Practice challenge

Write a `pre-push` hook that refuses to push when `prices.txt` contains a line without a price.

<details>
<summary>Solution</summary>

<!-- test: contains=pre-push: a menu item has no price; output -->
```bash
cd ~/git-practice/lesson-82
cat > .git/hooks/pre-push << 'EOF'
#!/bin/sh
if awk 'NF < 2' prices.txt | grep -q .; then echo "pre-push: a menu item has no price"; exit 1; fi
EOF
chmod +x .git/hooks/pre-push
echo "mocha" >> prices.txt
git hook run pre-push 2>&1 || true
```

```text
pre-push: a menu item has no price
```

</details>

## Recap

- Hooks are scripts in `.git/hooks/` named after an event; non-zero exit stops `pre-*` operations.
- Exact name, executable, with a `#!` line; test with `git hook run NAME`.
- Hooks are local and not cloned: CI must enforce what really matters.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-82
```

Next: [Lesson 83 · Pre-commit hook](../83-pre-commit-hook/README.md).
