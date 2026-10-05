# Lesson 39 · git clone

> Level 8 · Remote repositories · ⏱ 15 minutes

## What are we learning?

`git clone URL` copies a whole repository (every commit, every branch) and sets up `origin` and the local `main`. We
also see shallow clones and cloning a specific branch, both common in CI.

## Visual

```text
 git clone URL [FOLDER]
   1. create FOLDER, git init
   2. git remote add origin URL
   3. git fetch origin            ← all commits and branches → origin/*
   4. create local main from origin/main and check it out (main tracks origin/main)
```

## Lab setup

<!-- test: contains=lesson-39 -->
```bash
bash scripts/new-lab.sh lesson-39 remote
cd ~/git-practice/lesson-39
(cd ada && git switch -q -c feature-tea && echo "green tea" >> menu.txt && git commit -q -am "Add green tea" && git push -q -u origin feature-tea)
```

The server now has two branches: `main` and `feature-tea`.

## Demonstration

<!-- test: contains=origin/feature-tea; output -->
```bash
git clone server/cafe.git linus
cd linus
git branch -a
git log --oneline --all
```

```text
Cloning into 'linus'...
done.
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature-tea
  remotes/origin/main
647ed23 (origin/feature-tea) Add green tea
4267004 (HEAD -> main, origin/main, origin/HEAD) Add prices
fc345e6 Add the menu
d6df412 Add README
```

Only `main` is a local branch, but every commit is there: `feature-tea` exists as `origin/feature-tea`. Switching to
it creates the local branch automatically:

<!-- test: contains=set up to track 'origin/feature-tea'; output -->
```bash
git switch feature-tea
```

```text
Switched to a new branch 'feature-tea'
branch 'feature-tea' set up to track 'origin/feature-tea'.
```

## Command breakdown

| Command | What it does |
|---|---|
| `git clone URL` | clone into a folder named after the repository |
| `git clone URL DIR` | clone into DIR |
| `git clone --branch B URL` | check out B instead of the default branch |
| `git clone --depth 1 URL` | shallow: only the latest commit (fast, for CI) |
| `git clone --single-branch --branch B URL` | only fetch branch B |

## Hands-on exercise

**Instructions.** Make a shallow clone with only the latest commit of `feature-tea`.

**Expected result.** `git log` shows exactly one commit.

<!-- test-run: cd ~/git-practice/lesson-39 && git clone -q --no-local --depth 1 --branch feature-tea server/cafe.git shallow -->

**Verification.**

<!-- test: contains=1 -->
```bash
cd ~/git-practice/lesson-39/shallow
git log --oneline | wc -l
git rev-parse --is-shallow-repository
```

Solution: `git clone --no-local --depth 1 --branch feature-tea server/cafe.git shallow`. For a local path, `--depth`
needs `--no-local` (or a `file://` URL); otherwise Git copies the files directly and ignores it. A GitHub URL needs
neither.

## Break it

Clone into a folder that already has files:

<!-- test: fail; contains=already exists and is not an empty directory; output -->
```bash
cd ~/git-practice/lesson-39
git clone server/cafe.git ada 2>&1
```

```text
fatal: destination path 'ada' already exists and is not an empty directory.
```

## Troubleshoot

`destination path 'ada' already exists and is not an empty directory.`: Git never clones over existing files. Either
the repository is already there (then you need `git pull` inside it, not a new clone), or choose another folder.

<!-- test: contains=origin -->
```bash
git -C ada remote -v
```

## Fix

<!-- test: contains=ada-2 -->
```bash
git clone -q server/cafe.git ada-2
ls
```

## Real-world example

CI pipelines clone the repository on every run. GitHub Actions' `actions/checkout` does a shallow clone (`depth 1`) by
default for speed; jobs that need history (`git describe`, changelogs, `git log` between tags) set `fetch-depth: 0`.
A "fatal: no tag exactly matches" or empty changelog in CI is very often a shallow clone.

## Practice challenge

Your shallow clone needs the full history after all. Get it without cloning again.

<details>
<summary>Solution</summary>

<!-- test: contains=false; output -->
```bash
cd ~/git-practice/lesson-39/shallow
git fetch -q --unshallow
git log --oneline | wc -l
git rev-parse --is-shallow-repository
```

```text
4
false
```

</details>

## Recap

- `git clone` = init + add origin + fetch everything + check out the default branch.
- Remote branches arrive as `origin/*`; `git switch NAME` creates the local tracking branch.
- `--depth 1` for fast CI clones; `--unshallow` to get the history later.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-39
```

Next: [Lesson 40 · git fetch](../40-git-fetch/README.md).
