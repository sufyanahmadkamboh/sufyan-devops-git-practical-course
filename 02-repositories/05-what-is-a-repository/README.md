# Lesson 05 · What is a Git repository?

> Level 2 · Repositories · ⏱ 15 minutes

## What are we learning?

What makes a folder a Git repository: the hidden `.git` folder, and what it contains.

## Visual

```text
cafe/                       ← the WORKING DIRECTORY: your files, as you edit them
├── README.md
├── menu.txt
├── prices.txt
└── .git/                   ← the REPOSITORY: everything Git knows
    ├── HEAD                   which branch you are on
    ├── config                 this repository's settings (lesson 04)
    ├── objects/               every version of every file, every commit (compressed)
    ├── refs/heads/            branches: one small file per branch, holding a commit ID
    └── index                  the staging area (lesson 10)
```

Delete `.git` and the folder is an ordinary folder again: the files stay, the history is gone.

## Lab setup

<!-- test: contains=lesson-05 -->
```bash
bash scripts/new-lab.sh lesson-05 basic
cd ~/git-practice/lesson-05
```

## Demonstration

<!-- test: contains=.git; output -->
```bash
ls -A
```

```text
.git
README.md
menu.txt
prices.txt
```

Inside `.git`:

<!-- test: contains=HEAD; output -->
```bash
ls -F .git
```

```text
COMMIT_EDITMSG
HEAD
config
description
hooks/
index
info/
logs/
objects/
refs/
```

The most important small files, read directly:

<!-- test: contains=ref: refs/heads/main; output -->
```bash
cat .git/HEAD
cat .git/refs/heads/main
git log --oneline -1
```

```text
ref: refs/heads/main
4267004871ae95e12690719f02460f9e3c935cf5
4267004 Add prices
```

`HEAD` says "the current branch is `main`"; `refs/heads/main` holds a commit ID; that ID is the latest commit. A branch
is just a file with a commit ID in it (lesson 77 goes deeper). And every version of every file is an object:

<!-- test: contains=count; output -->
```bash
git count-objects -v | head -2
find .git/objects -type f | head -3
```

```text
count: 9
size: 0
.git/objects/42/67004871ae95e12690719f02460f9e3c935cf5
.git/objects/58/13ff596a4ca95cdeb8b6777f5e30fa427ee0e8
.git/objects/6c/76265ddb2eef943f09b0eac893294d1827affa
```

## Command breakdown

| Command / file | What it shows |
|---|---|
| `ls -A` | including hidden entries such as `.git` |
| `.git/HEAD` | the current branch |
| `.git/refs/heads/<branch>` | the commit a branch points to |
| `.git/objects/` | the content database: files, folders, commits |
| `git count-objects -v` | how many objects, and their size |
| `git rev-parse --git-dir` | where the repository of the current folder is |

## Hands-on exercise

**Instructions.** From a subfolder of the lab, ask Git where the repository is.

**Expected result.** Git finds `.git` in the parent folder: commands work from anywhere inside the project.

**Verification.**

<!-- test: contains=.git -->
```bash
cd ~/git-practice/lesson-05
mkdir -p docs/notes && cd docs/notes
git rev-parse --show-toplevel --git-dir
```

## Break it

Run a Git command outside any repository:

<!-- test: fail; contains=not a git repository; output -->
```bash
mkdir -p ~/git-practice/lesson-05-plain && cd ~/git-practice/lesson-05-plain
git status 2>&1
```

```text
fatal: not a git repository (or any of the parent directories): .git
```

## Troubleshoot

`fatal: not a git repository (or any of the parent directories): .git`: Git looked for `.git` here and in every
parent folder, and found none. Either you are in the wrong folder, or the project was never initialised (or someone
deleted `.git`). Check where you are:

<!-- test -->
```bash
pwd
ls -A
```

## Fix

Go to the project folder (here, the lab):

<!-- test: contains=On branch main -->
```bash
cd ~/git-practice/lesson-05
git status
```

## Real-world example

A CI job fails with `not a git repository` because the checkout step was skipped or ran in a different folder, or a
Docker build copied the code without `.git` (a `.dockerignore` usually excludes it, on purpose). Knowing that "a
repository = a folder with `.git`" makes that error obvious.

## Practice challenge

Without `git log`, find the commit message of the latest commit by following `HEAD` yourself with
`git cat-file -p`.

<details>
<summary>Solution</summary>

<!-- test: contains=Add prices; output -->
```bash
cd ~/git-practice/lesson-05
ref=$(sed 's/ref: //' .git/HEAD)
id=$(cat ".git/$ref")
git cat-file -p "$id"
```

```text
tree edd9d5aca7be17de9c83a80dc687991f6f56e24d
parent fc345e6b28df7fdfd7f872b37d78b47d0d024103
author Ada Lovelace <ada@example.com> 1767603780 +0000
committer Ada Lovelace <ada@example.com> 1767603780 +0000

Add prices
```

`HEAD` → `refs/heads/main` → a commit ID → the commit object, with its tree, parent, author and message. Lesson 75
explores objects in depth.

</details>

## Recap

- A repository is the `.git` folder; the files around it are the working directory.
- `HEAD` names the current branch; a branch is a file holding a commit ID.
- `fatal: not a git repository` means no `.git` here or above: wrong folder, or never initialised.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-05 ~/git-practice/lesson-05-plain
```

Next: [Lesson 06 · git init](../06-git-init/README.md).
