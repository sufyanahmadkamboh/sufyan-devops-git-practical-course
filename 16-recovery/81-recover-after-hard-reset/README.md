# Lesson 81 · Recover after a hard reset

> Level 16 · Advanced recovery · ⏱ 25 minutes

## What are we learning?

`git reset --hard` is the most feared command, but what it destroys depends on how far your work got: **committed**
work is fully recoverable, **staged** work is recoverable with some digging (`git fsck --lost-found`), and only
**unstaged** work is really gone. We recover each case carefully.

## Visual

```text
 how far did the work get?        after git reset --hard            recovery
 ───────────────────────────      ─────────────────────────         ─────────────────────────────────────
 committed                        commits unreachable               git reflog / ORIG_HEAD → reset or branch
 staged (git add)                 blobs dangling, no names          git fsck --lost-found → .git/lost-found/other/
 only edited in the folder        overwritten                       none (editor history at best)
```

## Lab setup

<!-- test: contains=lesson-81 -->
```bash
bash scripts/new-lab.sh lesson-81 basic
cd ~/git-practice/lesson-81
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git log --oneline -3
```

## Demonstration

**Committed work.** Reset two commits too far:

<!-- test: contains=Add prices; output -->
```bash
git reset --hard HEAD~2
git log --oneline -1
```

```text
HEAD is now at 4267004 Add prices
4267004 (HEAD -> main) Add prices
```

Check before acting: what was the state before the reset? `ORIG_HEAD` and the reflog agree:

<!-- test: contains=Price green tea; output -->
```bash
git log --oneline -1 ORIG_HEAD
git reflog -3
```

```text
d37a774 Price green tea
4267004 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~2
d37a774 HEAD@{1}: commit: Price green tea
67d67a6 HEAD@{2}: commit: Add green tea
```

Recover by moving the branch back (nothing else changed since):

<!-- test: contains=Price green tea; output -->
```bash
git reset --hard ORIG_HEAD
git log --oneline -3
```

```text
HEAD is now at d37a774 Price green tea
d37a774 (HEAD -> main) Price green tea
67d67a6 Add green tea
4267004 Add prices
```

## Command breakdown

| Command | Use |
|---|---|
| `ORIG_HEAD` | where HEAD was before the last reset / merge / rebase |
| `git reflog` | every earlier position, with what moved it |
| `git branch rescue HEAD@{N}` | keep a position under a name before experimenting further |
| `git fsck --lost-found` | write dangling commits/blobs to `.git/lost-found/` |
| `git show BLOB` | read a recovered blob's content |

## Hands-on exercise

**Instructions.** Before any risky operation, leave yourself a rescue point: create a branch `before-cleanup` at the
current commit, reset hard to `HEAD~1`, and verify the rescue branch still has "Price green tea".

**Expected result.** `before-cleanup` points to "Price green tea"; `main` to "Add green tea".

<!-- test-run: cd ~/git-practice/lesson-81 && git branch before-cleanup && git reset -q --hard HEAD~1 -->

**Verification.**

<!-- test: contains=Price green tea; contains=Add green tea -->
```bash
cd ~/git-practice/lesson-81
git log --oneline -1 before-cleanup
git log --oneline -1 main
```

## Break it

Work was **staged** but not committed, and a hard reset wipes it:

<!-- test: absent=flat white; output -->
```bash
git reset -q --hard before-cleanup
printf 'flat white\ncortado\n' >> menu.txt
git add menu.txt
git reset --hard
cat menu.txt
```

```text
HEAD is now at d37a774 Price green tea
espresso
latte
cappuccino
green tea
```

## Troubleshoot

There is no commit, so the reflog has nothing. But `git add` wrote the file's content as a **blob** into the object
store; the reset removed it from the index, leaving the blob dangling (no name, no reference):

<!-- test: contains=dangling blob; output -->
```bash
git fsck --lost-found 2> /dev/null
```

```text
dangling blob bca981e9bc8b69d16bce2150e069815457e5b744
```

## Fix

`--lost-found` copied the dangling objects to `.git/lost-found/other/`. Find the one with your content and restore it:

<!-- test: contains=cortado; output -->
```bash
for f in .git/lost-found/other/*; do
  grep -l "cortado" "$f" > /dev/null 2>&1 && cp "$f" menu.txt && echo "restored from $(basename "$f")"
done
cat menu.txt
```

```text
restored from bca981e9bc8b69d16bce2150e069815457e5b744
espresso
latte
cappuccino
green tea
flat white
cortado
```

The file name is not stored in a blob: if several files were staged, you identify them by content. Edits that were
**never staged** leave no blob at all: stage often, or commit "WIP" on a branch.

## Real-world example

"I ran `git reset --hard` instead of `--soft` and my whole afternoon is gone." First question: did you commit? Then
`git reset --hard ORIG_HEAD` (if nothing else happened) or `git reflog`. Did you at least `git add`? Then `git fsck
--lost-found` and search the blobs by content, newest first (`ls -t .git/lost-found/other`). Do not run `git gc` while
recovering.

## Practice challenge

Recover a commit after a reset **and** a second operation (so `ORIG_HEAD` no longer helps).

<details>
<summary>Solution</summary>

<!-- test: contains=Price green tea; output -->
```bash
cd ~/git-practice/lesson-81
git reset -q --hard before-cleanup && git branch -D before-cleanup > /dev/null
git reset -q --hard HEAD~1
git commit -q --allow-empty -m "Something else"
git log --oneline -1 ORIG_HEAD
target=$(git reflog --format='%h %gs' | awk '/commit: Price green tea/ {print $1; exit}')
git branch rescued "$target" && git log --oneline -1 rescued
```

```text
d37a774 Price green tea
d37a774 (rescued) Price green tea
```

`ORIG_HEAD` now points elsewhere; the reflog still lists the "Price green tea" commit.

</details>

## Recap

- Committed work survives `reset --hard`: `ORIG_HEAD`, reflog.
- Staged work survives as dangling blobs: `git fsck --lost-found`.
- Unstaged work does not survive: commit or stash before risky commands.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-81
```

Next: [Module 17 · Lesson 82 · What are Git hooks?](../../17-hooks/82-what-are-hooks/README.md).
