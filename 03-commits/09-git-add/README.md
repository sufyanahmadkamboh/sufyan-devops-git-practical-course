# Lesson 09 · git add

> Level 2 · Commits · ⏱ 15 minutes

## What are we learning?

`git add` copies changes from the working directory into the **staging area**: the draft of your next commit. We
compare `git add FILE` with `git add .` and `git add -A`.

## Visual

```text
 Working Directory              Staging Area (index)             Repository
 ─────────────────              ────────────────────             ──────────
 menu.txt  (edited)   git add    menu.txt (that version)  commit  snapshot
 notes.txt (new)     ─────────►                          ───────►
 prices.txt (edited)            (not added: stays out of the next commit)
```

## Lab setup

<!-- test: contains=lesson-09 -->
```bash
bash scripts/new-lab.sh lesson-09 basic
cd ~/git-practice/lesson-09
```

## Demonstration

Three changes:

<!-- test: output -->
```bash
echo "green tea" >> menu.txt
sed -i 's/latte 3.20/latte 3.30/' prices.txt
echo "Ideas for next season" > notes.txt
git status --short
```

```text
 M menu.txt
 M prices.txt
?? notes.txt
```

Stage exactly one file:

<!-- test: contains=M  menu.txt; output -->
```bash
git add menu.txt
git status --short
```

```text
M  menu.txt
 M prices.txt
?? notes.txt
```

`menu.txt` moved to the first column (staged); the others did not. Now everything at once:

<!-- test: contains=A  notes.txt; output -->
```bash
git add .
git status --short
```

```text
M  menu.txt
A  notes.txt
M  prices.txt
```

`git add .` stages every change **in the current folder and below**: modified and new files (and deletions too,
since Git 2.0). `git add -A` does the same for the **whole repository**, whatever folder you are in.

Important detail: `git add` stages a file's content **at that moment**. Edit it again afterwards and the new edit is
not staged:

<!-- test: contains=MM menu.txt; output -->
```bash
echo "chai" >> menu.txt
git status --short
```

```text
MM menu.txt
A  notes.txt
M  prices.txt
```

`MM`: the staged version has `green tea`; the working directory also has `chai`, which is not staged.

## Command breakdown

| Command | Stages |
|---|---|
| `git add FILE...` | those files (or folders) |
| `git add .` | everything under the current folder |
| `git add -A` | everything in the repository |
| `git add -u` | only changes to files already tracked (no new files) |
| `git add -p` | interactively, hunk by hunk (pick parts of a file) |
| `git add -n .` | dry run: show what would be staged |

## Hands-on exercise

**Instructions.** Stage the extra `chai` line too, but use a dry run first to check what `git add` would do.

**Expected result.** The dry run lists `add 'menu.txt'`; afterwards `menu.txt` shows `M ` (fully staged).

<!-- test-run: cd ~/git-practice/lesson-09 && git add menu.txt -->

**Verification.**

<!-- test: contains=M  menu.txt -->
```bash
cd ~/git-practice/lesson-09
git add -n .
git status --short
```

## Break it

Stage a file that should never be committed (a local secret) with a careless `git add .`:

<!-- test: contains=A  .env -->
```bash
echo "DB_PASSWORD=example-only-not-a-real-secret" > .env
git add .
git status --short
```

## Troubleshoot

`A  .env`: the secrets file is staged. It is **not committed yet**: the staging area is a draft, and you can take
things out of it before the commit. That is the moment to look at `git status` before every commit.

## Fix

Unstage it (lesson 30 covers `git restore --staged`), and make Git ignore it from now on (lesson 73):

<!-- test: absent=.env; output -->
```bash
git restore --staged .env
echo ".env" > .gitignore
git add .gitignore
git status --short
```

```text
A  .gitignore
M  menu.txt
A  notes.txt
M  prices.txt
```

`.env` disappeared from the list entirely: it is ignored, so `git add .` will never pick it up again.

## Real-world example

In a DevOps repository a single change often touches several files: a Kubernetes manifest, the Helm values, the
README. Stage them deliberately (`git add k8s/deployment.yaml helm/values.yaml`) and leave unrelated edits out, so
that the commit is one coherent change that can be reviewed and reverted on its own.

## Practice challenge

Create two new files in a subfolder `docs/` and one modified file at the top level. From inside `docs/`, stage only
the two new files with one command, then stage everything with another.

<details>
<summary>Solution</summary>

<!-- test: contains=A  a.md; contains=M  ../README.md; output -->
```bash
cd ~/git-practice/lesson-09
git add -A && git commit -q -m "Save the lesson's changes"
mkdir -p docs && echo "a" > docs/a.md && echo "b" > docs/b.md && echo "x" >> README.md
cd docs
git add .
git status --short
echo "---"
git add -A
git status --short
```

```text
 M ../README.md
A  a.md
A  b.md
---
M  ../README.md
A  a.md
A  b.md
```

From `docs/`, `git add .` staged only `docs/` (`README.md` one folder up stays ` M`); `git add -A` staged it
too. Paths in `git status` are shown relative to the folder you are in.

</details>

## Recap

- `git add` copies the current content of a file into the staging area.
- `.` = this folder and below; `-A` = whole repository; `-u` = tracked files only; `-p` = hunk by hunk.
- Staged content is a snapshot: later edits need another `git add`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-09
```

Next: [Lesson 10 · The staging area](../10-staging-area/README.md).
