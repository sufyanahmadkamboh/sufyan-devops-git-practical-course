# Lesson 30 · Unstage files

> Level 6 · Undoing changes · ⏱ 10 minutes

## What are we learning?

How to take a file back out of the next commit without losing your edit: `git restore --staged FILE`. This undo is
completely safe.

## Visual

```text
 Working directory      Staging area             Repository
      │                      │                        │
      │  git add FILE ─────► │                        │
      │                      │ ◄── git restore --staged FILE
      │                      │     copies the COMMITTED version into the staging area;
      │                      │     your working directory file is NOT touched
```

## Lab setup

<!-- test: contains=lesson-30 -->
```bash
bash scripts/new-lab.sh lesson-30 basic
cd ~/git-practice/lesson-30
```

## Demonstration

Two changes staged, but only one belongs in the next commit:

<!-- test: contains=M  prices.txt; output -->
```bash
echo "mocha" >> menu.txt
sed -i 's/latte 3.20/latte 3.30/' prices.txt
git add .
git status --short
```

```text
M  menu.txt
M  prices.txt
```

Unstage `prices.txt`:

<!-- test: contains= M prices.txt; output -->
```bash
git restore --staged prices.txt
git status --short
git diff prices.txt
```

```text
M  menu.txt
 M prices.txt
diff --git a/prices.txt b/prices.txt
index 5813ff5..ddaed76 100644
--- a/prices.txt
+++ b/prices.txt
@@ -1,3 +1,3 @@
 espresso 2.50
-latte 3.20
+latte 3.30
 cappuccino 3.40
```

Column one (staged) is empty for `prices.txt`, column two (unstaged) shows `M`: the edit is still in the file, just not
in the next commit. Commit the menu alone:

<!-- test: contains=1 file changed -->
```bash
git commit -m "Add mocha"
```

## Command breakdown

| Command | What it does |
|---|---|
| `git restore --staged FILE` | unstage FILE, keep the edit |
| `git restore --staged .` | unstage everything |
| `git restore --staged -p FILE` | unstage hunk by hunk |
| `git reset FILE` | the older command for the same thing (lesson 31) |
| `git rm --cached FILE` | stop tracking FILE but keep it on disk (lesson 73) |

## Hands-on exercise

**Instructions.** Stage both `prices.txt` and a new file `notes.txt`, then unstage only `notes.txt`.

**Expected result.** `notes.txt` shows as untracked (`??`), `prices.txt` stays staged.

<!-- test-run: cd ~/git-practice/lesson-30 && echo "call supplier" > notes.txt && git add prices.txt notes.txt && git restore --staged notes.txt -->

**Verification.**

<!-- test: contains=?? notes.txt; contains=M  prices.txt -->
```bash
cd ~/git-practice/lesson-30
git status --short
```

## Break it

Unstage the file in a brand-new repository, before the first commit:

<!-- test: fail; contains=could not resolve 'HEAD'; output -->
```bash
mkdir -p ~/git-practice/lesson-30-new && cd ~/git-practice/lesson-30-new && git init -q
echo hello > hello.txt && git add hello.txt
git restore --staged hello.txt 2>&1
```

```text
fatal: could not resolve 'HEAD'
```

## Troubleshoot

`could not resolve 'HEAD'`: `git restore --staged` copies the version from `HEAD`, and a new repository has no commit yet.
`git status` itself tells you what to use instead:

<!-- test: contains=git rm --cached; output -->
```bash
cd ~/git-practice/lesson-30-new
git status | grep -A1 "Changes to be committed"
```

```text
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
```

## Fix

<!-- test: contains=?? hello.txt -->
```bash
git rm -q --cached hello.txt
git status --short
cd ~/git-practice/lesson-30
```

## Real-world example

`git add .` picked up `.env` with local passwords, together with your real change. Before committing, `git status`
shows it staged: `git restore --staged .env` takes it out, then add `.env` to `.gitignore` (lesson 73) so it cannot
happen again. If it was already **committed** and pushed, unstaging is not enough: see lesson 90.

## Practice challenge

Stage everything, unstage everything, and prove that no edit was lost.

<details>
<summary>Solution</summary>

<!-- test: contains=prices.txt; output -->
```bash
cd ~/git-practice/lesson-30
git add .
git restore --staged .
git status --short
git diff --stat
```

```text
 M prices.txt
?? notes.txt
 prices.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

</details>

## Recap

- `git restore --staged FILE` removes a file from the next commit; the edit stays.
- It is always safe: it never touches your working directory.
- Before the first commit, use `git rm --cached FILE`.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-30 ~/git-practice/lesson-30-new
```

Next: [Lesson 31 · git reset: soft, mixed and hard](../31-git-reset/README.md).
