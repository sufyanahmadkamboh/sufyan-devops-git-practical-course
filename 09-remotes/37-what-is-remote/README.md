# Lesson 37 · What is a remote?

> Level 8 · Remote repositories · ⏱ 15 minutes

## What are we learning?

A remote is another copy of the repository that yours knows by a short name, usually `origin`. We look at how your
clone remembers the remote's branches (`origin/main`) and why they are only a snapshot of the last time you talked to
it.

## Visual

```text
        ┌──────────── server (GitHub) ────────────┐
        │  cafe.git     main → 4267004             │
        └───────▲──────────────────────┬───────────┘
          push  │                      │  fetch / pull / clone
        ┌───────┴──────────────────────▼───────────┐
        │  your clone                              │
        │    main          → your branch           │
        │    origin/main   → where main was on the │
        │                    server LAST TIME you  │
        │                    fetched (read-only)   │
        └──────────────────────────────────────────┘
```

In this course the "server" is a bare repository on your disk (`server/cafe.git`), which behaves exactly like GitHub
for Git's purposes; module 10 uses the real GitHub.

## Lab setup

<!-- test: contains=lesson-37 -->
```bash
bash scripts/new-lab.sh lesson-37 remote
cd ~/git-practice/lesson-37
ls
```

`server/cafe.git` is the shared repository; `ada/` and `grace/` are two developers' clones of it.

## Demonstration

<!-- test: contains=origin; output -->
```bash
cd ada
git remote -v
```

```text
origin	~/git-practice/lesson-37/server/cafe.git (fetch)
origin	~/git-practice/lesson-37/server/cafe.git (push)
```

`origin` is the name, the path is the address (on GitHub it is `https://github.com/...` or `git@github.com:...`). One
for fetching, one for pushing; they are usually the same.

<!-- test: contains=remotes/origin/main; output -->
```bash
git branch -a
git log --oneline --graph --all
```

```text
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
* 4267004 (HEAD -> main, origin/main, origin/HEAD) Add prices
* fc345e6 Add the menu
* d6df412 Add README
```

`origin/main` (shown as `remotes/origin/main`) is a **remote-tracking branch**: your clone's memory of the server's
`main`. You cannot commit to it; it only moves when you talk to the server.

## Command breakdown

| Command | What it shows |
|---|---|
| `git remote` | remote names |
| `git remote -v` | names with URLs |
| `git remote show origin` | details: branches, tracking, push/pull config (contacts the server) |
| `git branch -r` | remote-tracking branches |
| `git branch -a` | local and remote-tracking branches |

## Hands-on exercise

**Instructions.** Show the details of `origin` in Grace's clone, including which local branch pulls from where.

**Expected result.** `HEAD branch: main` and `main merges with remote main`.

**Verification.**

<!-- test: contains=merges with remote main -->
```bash
cd ~/git-practice/lesson-37/grace
git remote show origin
```

## Break it

Grace commits and pushes. Ada looks at `origin/main`, expecting to see Grace's commit:

<!-- test: absent=Add opening hours; output -->
```bash
echo "Open 8-18" >> README.md && git commit -q -am "Add opening hours" && git push -q
cd ../ada
git log --oneline -1 origin/main
```

```text
4267004 (HEAD -> main, origin/main, origin/HEAD) Add prices
```

## Troubleshoot

Ada's `origin/main` still shows `Add prices`. Remote-tracking branches are **not live**: they are updated only by
`git fetch`, `git pull` or `git push`. Ada's clone has not talked to the server since Grace pushed.

## Fix

<!-- test: contains=Add opening hours; output -->
```bash
git fetch
git log --oneline -1 origin/main
```

```text
From ~/git-practice/lesson-37/server/cafe
   4267004..958330b  main       -> origin/main
958330b (origin/main, origin/HEAD) Add opening hours
```

## Real-world example

"But the branch exists on GitHub!": a colleague created `feature-login` and pushed it; your `git branch -a` does not
show it until you `git fetch`. Before any decision based on `origin/...` (comparing, merging, deleting), fetch first.

## Practice challenge

Without fetching, find out what the server's `main` points to **right now**, and compare it with Ada's `origin/main`.

<details>
<summary>Solution</summary>

<!-- test: contains=refs/heads/main; output -->
```bash
cd ~/git-practice/lesson-37/ada
git ls-remote origin main
git rev-parse origin/main
```

```text
958330b4325970f21538eb43bc187658891a6c0c	refs/heads/main
958330b4325970f21538eb43bc187658891a6c0c
```

`git ls-remote` asks the server directly without updating anything locally.

</details>

## Recap

- A remote is a named URL of another copy; `origin` is the default name after cloning.
- `origin/main` is a local, read-only snapshot of the server's `main`, updated only by fetch/pull/push.
- `git ls-remote` asks the server live.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-37
```

Next: [Lesson 38 · git remote](../38-git-remote/README.md).
