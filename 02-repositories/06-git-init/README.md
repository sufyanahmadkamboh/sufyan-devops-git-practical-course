# Lesson 06 · git init

> Level 2 · Repositories · ⏱ 15 minutes

## What are we learning?

Turning a folder into a repository with `git init`, and exactly what that does (and does not do).

## Visual

```text
 git-demo/            git init            git-demo/
 └── (files)        ─────────────►        ├── (files)       ← untouched: still untracked
                                          └── .git/         ← new, empty history
                                                HEAD → refs/heads/main   (a branch with no commits yet)
```

## Lab setup

<!-- test: contains=lesson-06 -->
```bash
mkdir -p ~/git-practice/lesson-06 && cd ~/git-practice/lesson-06
pwd
```

## Demonstration

<!-- test: contains=Initialized empty Git repository; output -->
```bash
mkdir git-demo
cd git-demo
git init
```

```text
Initialized empty Git repository in ~/git-practice/lesson-06/git-demo/.git/
```

<!-- test: contains=No commits yet; output -->
```bash
git status
```

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

What happened, exactly: a `.git` folder appeared. Nothing else. `HEAD` points to `main`, but `main` has no commit yet,
so the branch file does not exist:

<!-- test: contains=ref: refs/heads/main; output -->
```bash
cat .git/HEAD
ls .git/refs/heads/ | wc -l
```

```text
ref: refs/heads/main
0
```

Files that were already in the folder are not added automatically:

<!-- test: contains=Untracked files; output -->
```bash
echo "# Demo" > README.md
git status --short
git status | sed -n '1,6p'
```

```text
?? README.md
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
```

`??` means untracked: Git sees the file, but you have not told it to version it (lesson 09).

## Command breakdown

| Command | What it does |
|---|---|
| `git init` | create `.git` in the current folder (safe to run again: it reinitialises, it does not wipe history) |
| `git init NAME` | create the folder `NAME` and a repository in it |
| `git init -b main` | choose the first branch's name explicitly |
| `git init --bare` | a repository without a working directory, for servers (lesson 02) |

## Hands-on exercise

**Instructions.** Create a second repository called `notes` with one command, choosing the branch name `trunk`.

**Expected result.** `~/git-practice/lesson-06/notes` exists, and `git status` there says `On branch trunk`.

<!-- test-run: cd ~/git-practice/lesson-06 && git init -q -b trunk notes -->

**Verification.**

<!-- test: contains=On branch trunk -->
```bash
cd ~/git-practice/lesson-06/notes
git status | head -1
```

## Break it

The most common mistake: `git init` in the wrong place, typically your home folder. Simulate it:

<!-- test: output -->
```bash
cd ~/git-practice/lesson-06
mkdir -p home-sim/projects/website && cd home-sim
git init -q
cd projects/website
echo "<h1>Hi</h1>" > index.html
git status --short
git rev-parse --show-toplevel
```

```text
?? ../
~/git-practice/lesson-06/home-sim
```

## Troubleshoot

`git status` inside `website` shows files from the wrong level, and `--show-toplevel` reveals the repository root is
`home-sim`, two levels up: every folder below it is now "inside" that accidental repository. Symptoms in real life:
`git status` listing your whole home folder, or a project that suddenly "has" thousands of untracked files.

## Fix

Remove the accidental `.git` (only the one you created by mistake: check the path first!), then initialise in the
right folder:

<!-- test: contains=website -->
```bash
cd ~/git-practice/lesson-06/home-sim
ls -A
rm -rf .git
cd projects/website && git init -q
git rev-parse --show-toplevel
```

## Real-world example

Starting a new infrastructure repository: `mkdir terraform-network && cd terraform-network && git init -b main`, add a
`.gitignore` (lesson 73) before the first commit so that state files and secrets never get tracked, then connect it to
GitHub (lesson 46).

## Practice challenge

Run `git init` a second time in `git-demo` after making a commit. Prove that the commit survives.

<details>
<summary>Solution</summary>

<!-- test: contains=Reinitialized existing Git repository; contains=First commit; output -->
```bash
cd ~/git-practice/lesson-06/git-demo
git add README.md && git commit -q -m "First commit"
git init
git log --oneline
```

```text
Reinitialized existing Git repository in ~/git-practice/lesson-06/git-demo/.git/
3b90ce3 (HEAD -> main) First commit
```

`Reinitialized existing Git repository`: `git init` never deletes history.

</details>

## Recap

- `git init` creates `.git`; existing files stay untracked until you add them.
- A new branch has no commit, so `refs/heads/main` does not exist until the first commit.
- Check where you are before `git init`; `git rev-parse --show-toplevel` shows which repository you are in.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-06
```

Next: [Lesson 07 · The working directory](../07-working-directory/README.md).
