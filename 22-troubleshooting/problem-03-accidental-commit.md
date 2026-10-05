# Problem 3 · Accidental commit

> Troubleshooting lab · run every command from the course folder · related lessons: [30](../07-undoing/30-unstage-files/README.md), [31](../07-undoing/31-git-reset/README.md), [73](../14-advanced-git/73-gitignore/README.md)

## Problem

`git add .` and `git commit` included a file that should never be in the repository: a 200 kB debug log, next to the
real change.

<!-- test: contains=lesson-t03 -->
```bash
bash scripts/new-lab.sh lesson-t03 basic
cd ~/git-practice/lesson-t03
echo "chai" >> menu.txt
head -c 200000 /dev/zero | tr '\0' 'x' > debug.log
git add . && git commit -q -m "Add chai"
```

## Symptoms

The commit looks bigger than the change; a reviewer asks "what is debug.log?".

<!-- test: contains=debug.log; output -->
```bash
git show --stat --format=%s HEAD
```

```text
Add chai

 debug.log | 1 +
 menu.txt  | 1 +
 2 files changed, 2 insertions(+)
```

## Investigation

Is the commit pushed? What exactly is in it?

<!-- test: contains=debug.log; output -->
```bash
git status | head -2
git show --name-status --format= HEAD
```

```text
On branch main
nothing to commit, working tree clean
A	debug.log
M	menu.txt
```

## Commands

| Command | Shows |
|---|---|
| `git show --stat HEAD` | files and sizes changed by the last commit |
| `git show --name-status HEAD` | A(dded) / M(odified) / D(eleted) per file |
| `git log origin/main..HEAD` | commits not pushed yet (with a remote) |

## Understand the output

`A debug.log`: the file was added by this commit, alongside `M menu.txt`. No remote exists, so nothing is shared: the
commit can be rewritten safely.

## Root cause

`git add .` stages everything untracked; the log file was not ignored.

## Fix

Take the file out of the commit, keep the real change, and ignore such files from now on:

<!-- test: contains=menu.txt; output -->
```bash
git rm -q --cached debug.log
echo "*.log" >> .gitignore && git add .gitignore
git commit -q --amend --no-edit
git show --name-status --format=%s HEAD
```

```text
Add chai

A	.gitignore
M	menu.txt
```

Pushed already? Then the file is in shared history: remove it with a new commit (`git rm --cached`, commit), and if it
contained secrets follow Problem 12.

## Verification

<!-- test: contains=debug.log is ignored; output -->
```bash
git ls-files | grep -c debug.log || true
git check-ignore -q debug.log && echo "debug.log is ignored"
```

```text
0
debug.log is ignored
```

## Prevention

- Read `git status` (or `git diff --cached --stat`) before every commit.
- Add files by name or with `git add -p`; keep a good `.gitignore`.
- A pre-commit hook that blocks large files (lesson 83).

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t03
```

Next: [Problem 4 · Accidental reset](problem-04-accidental-reset.md)
