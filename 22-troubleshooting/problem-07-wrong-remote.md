# Problem 7 · Wrong remote

> Troubleshooting lab · run every command from the course folder · related lessons: [37](../09-remotes/37-what-is-remote/README.md), [38](../09-remotes/38-git-remote/README.md), [25](../06-merging/25-three-way-merge/README.md)

## Problem

You copied a project folder to start a new service, but `origin` still points to the **old** project's repository.
Your first pull brings in a stranger's history.

<!-- test: contains=lesson-t07 -->
```bash
bash scripts/new-lab.sh lesson-t07 remote
cd ~/git-practice/lesson-t07
git init -q --bare other-project.git
git init -q -b main menu-service && cd menu-service
echo "# Menu service" > README.md && git add README.md && git commit -q -m "Start the menu service"
git remote add origin ../server/cafe.git
```

The service should push to `other-project.git`; `origin` was copied from the cafe project by mistake.

## Symptoms

<!-- test: fail; contains=refusing to merge unrelated histories; output -->
```bash
git pull --no-rebase origin main 2>&1 | tail -2
test "${PIPESTATUS[0]}" -eq 0
```

```text
 * [new branch]      main       -> origin/main
fatal: refusing to merge unrelated histories
```

## Investigation

Where does `origin` point, and what is there?

<!-- test: contains=cafe.git; output -->
```bash
git remote -v
git ls-remote origin
git log --oneline -1 FETCH_HEAD
```

```text
origin	../server/cafe.git (fetch)
origin	../server/cafe.git (push)
4267004871ae95e12690719f02460f9e3c935cf5	HEAD
4267004871ae95e12690719f02460f9e3c935cf5	refs/heads/main
4267004 (origin/main) Add prices
```

## Commands

| Command | Shows |
|---|---|
| `git remote -v` | each remote's URL |
| `git ls-remote REMOTE` | what the remote really contains |
| `git merge-base HEAD FETCH_HEAD` | whether two histories share any commit (no output: unrelated) |

## Understand the output

`origin` is `../server/cafe.git`, a different project whose newest commit is "Add prices". The two histories have no
commit in common, which is why Git refuses to merge them. Had you pushed, the menu service would have landed in the
cafe repository.

## Root cause

The remote URL was copied with the folder (or added from the wrong snippet).

## Fix

Point `origin` at the right repository and push:

<!-- test: contains=[new branch]; output -->
```bash
git remote set-url origin ../other-project.git
git push -u origin main 2>&1 | grep -v "^To "
```

```text
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

## Verification

<!-- test: contains=other-project.git; contains=refs/heads/main; output -->
```bash
git remote get-url origin
git ls-remote origin
```

```text
../other-project.git
0158457ced28d04495e0c8f2d4eb047c5b5d554b	HEAD
0158457ced28d04495e0c8f2d4eb047c5b5d554b	refs/heads/main
```

## Prevention

- After cloning or copying, run `git remote -v` before the first push.
- Start new projects with `git init` (or from a template repository), not by copying another project's `.git`.
- Never answer "refusing to merge unrelated histories" with `--allow-unrelated-histories` before understanding why.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t07
```

Next: [Problem 8 · Push rejected](problem-08-push-rejected.md)
