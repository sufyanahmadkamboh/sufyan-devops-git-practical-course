# Problem 2 · Merge conflict

> Troubleshooting lab · run every command from the course folder · related lessons: [26](../06-merging/26-merge-conflicts/README.md), [27](../06-merging/27-resolving-conflicts/README.md), [28](../06-merging/28-abort-merge/README.md)

## Problem

Merging a feature branch into `main` stops with a conflict.

<!-- test: contains=lesson-t02 -->
```bash
bash scripts/new-lab.sh lesson-t02 conflict
cd ~/git-practice/lesson-t02
```

<!-- test: fail; contains=CONFLICT; output -->
```bash
git merge feature-tea 2>&1
```

```text
Auto-merging prices.txt
CONFLICT (content): Merge conflict in prices.txt
Automatic merge failed; fix conflicts and then commit the result.
```

## Symptoms

`Automatic merge failed; fix conflicts and then commit the result.` The prompt shows `MERGING`; files contain
`<<<<<<<` markers; commits are refused.

## Investigation

<!-- test: contains=both modified; output -->
```bash
git status --short
git status | grep -A2 "Unmerged paths"
git diff
```

```text
UU prices.txt
Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   prices.txt
diff --cc prices.txt
index ddaed76,09437d0..0000000
--- a/prices.txt
+++ b/prices.txt
@@@ -1,3 -1,3 +1,7 @@@
  espresso 2.50
++<<<<<<< HEAD
 +latte 3.30
++=======
+ latte 3.50
++>>>>>>> feature-tea
  cappuccino 3.40
```

Who changed the line on each side, and why?

<!-- test: contains=Raise the latte price; output -->
```bash
git log --oneline --merge -- prices.txt
```

```text
594657b (HEAD -> main) Raise the latte price to 3.30
00931cc (feature-tea) Raise the latte price to 3.50
```

## Commands

| Command | Shows |
|---|---|
| `git status` | the conflicted files ("both modified") |
| `git diff` | the conflict hunks (with `merge.conflictStyle zdiff3`: also the base) |
| `git log --merge -- FILE` | the commits on both sides that touched FILE |
| `git merge --abort` | the way back, if needed |

## Understand the output

`UU prices.txt` / "both modified": both branches changed the latte line differently since their merge base (3.30 on
`main` by Grace, 3.50 on `feature-tea` by Ada). Git cannot choose; everything else merged automatically.

## Root cause

Two branches changed the same lines in parallel. Not an error in Git: a decision only a person can make.

## Fix

Decide the correct content (here, after asking both: 3.40), remove the markers, mark resolved, commit:

<!-- test: contains=Merge branch 'feature-tea'; output -->
```bash
printf 'espresso 2.50\nlatte 3.40\ncappuccino 3.40\n' > prices.txt
git add prices.txt
git commit -q --no-edit
git log --oneline --graph -4
```

```text
*   2280763 (HEAD -> main) Merge branch 'feature-tea'
|\  
| * 00931cc (feature-tea) Raise the latte price to 3.50
* | 594657b Raise the latte price to 3.30
|/  
* 4267004 Add prices
```

## Verification

No markers left anywhere, and the merge has two parents:

<!-- test: contains=no markers; output -->
```bash
git grep -n -E '^(<<<<<<<|=======|>>>>>>>)' || echo "no markers"
git log -1 --format='parents: %p'
```

```text
no markers
parents: 594657b 00931cc
```

## Prevention

- Small, short-lived branches; merge `main` into your branch often (lesson 56).
- `git config --global merge.conflictStyle zdiff3` to see the base when conflicts happen.
- `git config --global rerere.enabled true` to reuse resolutions.

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-t02
```

Next: [Problem 3 · Accidental commit](problem-03-accidental-commit.md)
