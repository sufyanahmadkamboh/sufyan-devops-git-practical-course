# Lesson 85 · Git hooks in teams

> Level 17 · Git hooks · ⏱ 20 minutes

## What are we learning?

Hooks in `.git/hooks/` belong to one clone: they are never committed, cloned or pushed. Teams share hooks by
committing them to a normal folder and pointing Git at it with `core.hooksPath`, and they enforce the important checks
in CI, because local hooks are optional by nature.

## Visual

```text
 repository (committed)              each developer, once after cloning
 .githooks/                          git config core.hooksPath .githooks
 ├── pre-commit                            │
 └── commit-msg                            ▼
                                     Git runs .githooks/* instead of .git/hooks/*

 local hooks  = fast feedback, skippable (--no-verify, not installed, other machine)
 CI checks    = the same checks on every PR, required by branch protection: not skippable
```

## Lab setup

<!-- test: contains=lesson-85 -->
```bash
bash scripts/new-lab.sh lesson-85 remote
cd ~/git-practice/lesson-85/ada
```

## Demonstration

Ada commits the team's hook to the repository:

<!-- test: contains=.githooks/commit-msg -->
```bash
mkdir -p .githooks
cat > .githooks/commit-msg << 'EOF'
#!/usr/bin/env bash
# commit-msg: require a type prefix such as "feat:" or "fix:"
head -n 1 "$1" | grep -Eq '^(Merge|Revert|(feat|fix|docs|chore|refactor|test|ci)(\([a-z0-9-]+\))?!?: )' && exit 0
echo "commit-msg: start the message with a type, e.g. \"feat: add green tea\""; exit 1
EOF
chmod +x .githooks/commit-msg
git add .githooks && git commit -q -m "chore: add the team's Git hooks"
git push -q
git ls-files .githooks
```

…and enables it for herself:

<!-- test: fail; contains=start the message with a type; output -->
```bash
git config core.hooksPath .githooks
echo "green tea" >> menu.txt && git commit -am "green tea" 2>&1
```

```text
commit-msg: start the message with a type, e.g. "feat: add green tea"
```

## Command breakdown

| Command / tool | Use |
|---|---|
| `git config core.hooksPath .githooks` | use the committed hooks folder (per clone) |
| `git config --global core.hooksPath ~/.githooks` | personal hooks for every repository |
| `git hook list commit-msg` | which hook Git would run |
| `make setup` / `npm prepare` / `pre-commit install` | a setup step that installs hooks automatically |
| CI job running the same checks | the real enforcement |

## Hands-on exercise

**Instructions.** Commit Ada's change with a valid message and push it.

**Expected result.** `feat: add green tea` on the server.

<!-- test-run: cd ~/git-practice/lesson-85/ada && git commit -q -am "feat: add green tea" && git push -q -->

**Verification.**

<!-- test: contains=feat: add green tea -->
```bash
cd ~/git-practice/lesson-85
git --git-dir=server/cafe.git log --oneline -1
```

## Break it

Grace pulls the hooks, but her commits are not checked:

<!-- test: contains=whatever; output -->
```bash
cd ~/git-practice/lesson-85/grace && git pull -q
ls .githooks
echo "mocha" >> menu.txt && git commit -q -am "whatever" && git log --oneline -1
```

```text
commit-msg
739ddf2 (HEAD -> main) whatever
```

## Troubleshoot

The hook files arrived with `git pull`, but Git does not run them: `core.hooksPath` is configuration of Ada's clone, not
part of the repository. Git never enables hooks automatically after a clone or pull (that would let any repository
run code on your machine).

<!-- test: contains=not set; output -->
```bash
git config core.hooksPath || echo "core.hooksPath not set in Grace's clone"
```

```text
core.hooksPath not set in Grace's clone
```

## Fix

Grace enables the hooks (in real projects: a documented one-time setup step), then fixes her message before pushing:

<!-- test: contains=feat: add mocha; output -->
```bash
git config core.hooksPath .githooks
git commit -q --amend -m "feat: add mocha"
git log --oneline -1
```

```text
891bba6 (HEAD -> main) feat: add mocha
```

And the check that cannot be skipped runs on the server side, for every pushed commit, for example in CI:

<!-- test: contains=all commit messages follow the convention; output -->
```bash
git log --format=%s origin/main..HEAD | grep -Ev '^(Merge|(feat|fix|docs|chore|refactor|test|ci)(\(.+\))?!?: )' && exit 1 || echo "all commit messages follow the convention"
```

```text
all commit messages follow the convention
```

## Real-world example

A typical setup: `.pre-commit-config.yaml` in the repository; the README says "run `pre-commit install` once"; a CI
job `pre-commit run --all-files` on every PR; branch protection requires that job. Developers get feedback in a
second on their machine, and the repository is protected even when someone never installed the hooks.

## Practice challenge

Show the path of the `commit-msg` hook Git uses in Grace's clone now.

<details>
<summary>Solution</summary>

<!-- test: contains=.githooks/commit-msg; output -->
```bash
cd ~/git-practice/lesson-85/grace
git rev-parse --git-path hooks/commit-msg
```

```text
.githooks/commit-msg
```

`--git-path` resolves paths inside the repository's Git directory, honouring `core.hooksPath`.

</details>

## Recap

- Hooks are not cloned; share them as files in the repository plus `core.hooksPath`.
- Git never activates hooks by itself: a setup step is needed per clone.
- Local hooks give fast feedback; CI with branch protection gives enforcement.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-85
```

Next: [Module 18 · Lesson 86 · Git submodules](../../18-advanced-repositories/86-git-submodules/README.md).
