# Problem 8 · Push rejected

> Troubleshooting lab · run every command from the course folder · related lessons: [40](../09-remotes/40-git-fetch/README.md), [41](../09-remotes/41-git-pull/README.md), [42](../09-remotes/42-git-push/README.md)

## Problem

Your push to `main` is rejected right after a teammate pushed.

<!-- test: contains=lesson-t08 -->
```bash
bash scripts/new-lab.sh lesson-t08 remote
cd ~/git-practice/lesson-t08
(cd grace && echo "Open 8-18" >> README.md && git commit -q -am "Add opening hours" && git push -q)
cd ada && echo "chai" >> menu.txt && git commit -q -am "Add chai"
```

## Symptoms

<!-- test: fail; contains=[rejected]; output -->
```bash
git push 2>&1
```

```text
To ~/git-practice/lesson-t08/server/cafe.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '~/git-practice/lesson-t08/server/cafe.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

## Investigation

What does the server have that you do not, and the other way round?

<!-- test: contains=Add opening hours; output -->
```bash
git fetch
git status | head -3
echo "theirs:"; git log --oneline main..origin/main
echo "mine:";   git log --oneline origin/main..main
```

```text
From ~/git-practice/lesson-t08/server/cafe
   4267004..19d3b5e  main       -> origin/main
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
theirs:
19d3b5e (origin/main, origin/HEAD) Add opening hours
mine:
2e934e1 (HEAD -> main) Add chai
```

## Commands

| Command | Shows |
|---|---|
| `git fetch` | updates `origin/*` without touching your branch |
| `git status` | "have diverged, and have 1 and 1 different commits each" |
| `git log main..origin/main` / `origin/main..main` | incoming / outgoing commits |

## Understand the output

`! [rejected] main -> main (fetch first)`: the server's `main` contains a commit ("Add opening hours") that your
`main` does not. Accepting your push would remove it from `main`. After fetching, `git status` shows the divergence:
one commit on each side.

## Root cause

Someone pushed to the same branch since your last pull. Normal teamwork, not an error.

## Fix

Integrate their work, then push. Rebase keeps the history linear (your commit goes on top):

<!-- test: contains=main -> main; output -->
```bash
git pull --rebase 2>&1 | tail -1
git push 2>&1 | tail -1
```

```text
Rebasing (1/1)
Successfully rebased and updated refs/heads/main.
   19d3b5e..f26df62  main -> main
```

Never "fix" this with `git push --force` on a shared branch: it would delete your teammate's commit from the server.

## Verification

<!-- test: contains=Add chai; contains=Add opening hours; output -->
```bash
git log --oneline -3
git status | head -2
```

```text
f26df62 (HEAD -> main, origin/main, origin/HEAD) Add chai
19d3b5e Add opening hours
4267004 Add prices
On branch main
Your branch is up to date with 'origin/main'.
```

## Prevention

- `git pull --rebase` (or `fetch` + look) before pushing; `pull.rebase true` as default.
- Work on branches and merge through PRs: then two people rarely push the same branch.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t08
```

Next: [Problem 9 · Non-fast-forward error](problem-09-non-fast-forward.md)
