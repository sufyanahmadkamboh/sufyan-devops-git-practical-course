# Lesson 36 · Managing stashes

> Level 7 · Stash · ⏱ 15 minutes

## What are we learning?

How to keep several stashes under control: list them, see what is inside, apply a specific one, turn one into a branch,
clean up, and recover a stash dropped by mistake.

## Visual

```text
 stash@{0}  On main: menu ideas         ← newest (always @{0})
 stash@{1}  On main: price draft
 stash@{2}  WIP on main: 4267004 ...    ← oldest

 git stash show -p stash@{1}     look inside
 git stash apply stash@{1}       use it
 git stash branch NAME stash@{1} new branch from where it was made + apply + drop
 git stash drop stash@{1}        delete one        git stash clear: delete ALL
```

## Lab setup

<!-- test: contains=lesson-36 -->
```bash
bash scripts/new-lab.sh lesson-36 basic
cd ~/git-practice/lesson-36
for idea in "price draft" "menu ideas"; do
  echo "$idea" >> notes.txt && git add notes.txt && git stash push -q -m "$idea"
done
git stash list
```

## Demonstration

Inspect before using:

<!-- test: contains=+price draft; output -->
```bash
git stash show -p 'stash@{1}'
```

```text
diff --git a/notes.txt b/notes.txt
new file mode 100644
index 0000000..62384f0
--- /dev/null
+++ b/notes.txt
@@ -0,0 +1 @@
+price draft
```

`show` without `-p` only shows the file statistics. Turn the older idea into a proper branch:

<!-- test: contains=On branch price-draft; output -->
```bash
git stash branch price-draft 'stash@{1}'
git stash list
```

```text
Switched to a new branch 'price-draft'
On branch price-draft
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   notes.txt

Dropped stash@{1} (5545d628d5b9d9794910986d30f97cd7b7bc972a)
stash@{0}: On main: menu ideas
```

`git stash branch` created `price-draft` at the commit where the stash was made, applied it and dropped it. Use it when
`main` has moved on and the stash would conflict there.

## Command breakdown

| Command | What it does |
|---|---|
| `git stash list` | all stashes, newest first |
| `git stash show [-p] stash@{N}` | files changed / full diff |
| `git stash apply stash@{N}` | apply a specific stash |
| `git stash branch NAME [stash@{N}]` | new branch from the stash's base, apply, drop |
| `git stash drop stash@{N}` | delete one |
| `git stash clear` | delete all (careful) |

## Hands-on exercise

**Instructions.** Commit the branch's work, go back to `main` and delete the remaining stash.

**Expected result.** `git stash list` is empty.

<!-- test-run: cd ~/git-practice/lesson-36 && git commit -q -m "Price draft" && git switch -q main && git stash drop -q -->

**Verification.**

<!-- test: contains=0 -->
```bash
cd ~/git-practice/lesson-36
git stash list | wc -l
```

## Break it

Clear the shelf, then realise one stash was still needed:

<!-- test: contains=0 -->
```bash
echo "important recipe" > recipe.txt && git add recipe.txt && git stash push -q -m "recipe"
git stash clear
git stash list | wc -l
```

## Troubleshoot

`git stash clear` removed the `refs/stash` entries, but stashes are commits: the objects are still in the repository
until Git's garbage collection removes unreachable objects. `git fsck` lists unreachable commits; stash commits have
the message `On <branch>: <message>`:

<!-- test: contains=On main: recipe; output -->
```bash
for c in $(git fsck --no-reflogs --unreachable 2>/dev/null | awk '/commit/ {print $3}'); do
  git log -1 --format='%h %s' "$c"
done | grep "On main"
```

```text
5545d62 On main: price draft
186e3ba On main: recipe
62fcf1b On main: menu ideas
```

## Fix

<!-- test: contains=important recipe; output -->
```bash
lost=$(for c in $(git fsck --no-reflogs --unreachable 2>/dev/null | awk '/commit/ {print $3}'); do
  git log -1 --format='%H %s' "$c"; done | awk '/On main: recipe/ {print $1}')
git stash apply -q "$lost"
cat recipe.txt
```

```text
important recipe
```

## Real-world example

`git stash list` on a laptop after a busy month often shows 15 anonymous entries. Clean up regularly: look at each
(`git stash show -p`), turn the valuable ones into branches (`git stash branch`) or commits, drop the rest. Work that
matters belongs in a branch that is pushed, not on a local shelf.

## Practice challenge

Write a one-liner that prints, for every stash, its name and the number of files it changes.

<details>
<summary>Solution</summary>

<!-- test: contains=stash@{0}; output -->
```bash
cd ~/git-practice/lesson-36
git stash push -q -m "recipe again"
git stash list --format=%gd | while read -r s; do echo "$s $(git stash show --name-only "$s" | wc -l) file(s)"; done
```

```text
stash@{0} 1 file(s)
```

</details>

## Recap

- `git stash list` / `show -p` to know what you have; apply a specific `stash@{N}`.
- `git stash branch` turns a stash into a branch, avoiding conflicts with a moved `main`.
- Dropped stashes are unreachable commits: `git fsck --unreachable` can still find them for a while.

## Cleanup

<!-- test -->
```bash
rm -rf ~/git-practice/lesson-36
```

Next: [Module 09 · Lesson 37 · What is a remote?](../../09-remotes/37-what-is-remote/README.md).
