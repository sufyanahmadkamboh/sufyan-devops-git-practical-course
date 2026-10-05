# Lesson 79 · Recover a deleted branch

> Level 16 · Advanced recovery · ⏱ 20 minutes

## What are we learning?

Deleting a branch deletes a pointer; the commits remain until garbage collection removes unreachable objects (weeks,
by default). We recover deleted branches three ways: from the reflog, from another clone, and with `git fsck` when the
reflog has nothing.

## Visual

```text
 git branch -D feature        refs/heads/feature deleted (and its own reflog with it)
                              commits: still in .git/objects, now unreachable

 where to find them again:
   1. git reflog              if HEAD was ever on the branch (you worked on it)
   2. another clone / server  origin/feature in a teammate's clone, the PR on GitHub (refs/pull/N/head)
   3. git fsck --unreachable  lists commits nothing points to (last resort, before gc)
```

## Lab setup

<!-- test: contains=lesson-79 -->
```bash
bash scripts/new-lab.sh lesson-79 remote
cd ~/git-practice/lesson-79/ada
```

## Demonstration

Ada works on a branch, pushes it, then deletes it locally and on the server (thinking it was merged):

<!-- test: contains=Deleted branch feature-hours; output -->
```bash
git switch -q -c feature-hours
echo "Open 8-18" > hours.txt && git add hours.txt && git commit -q -m "Add opening hours"
echo "Closed on Mondays" >> hours.txt && git commit -q -am "Close on Mondays"
git push -q -u origin feature-hours
git switch -q main
git branch -D feature-hours
git push -q origin --delete feature-hours
```

```text
Deleted branch feature-hours (was fc584d2).
```

**Way 1: the reflog.** Ada had the branch checked out, so `HEAD`'s reflog knows its last commit:

<!-- test: contains=Close on Mondays; output -->
```bash
git reflog | grep -m1 "Close on Mondays"
git branch feature-hours "$(git reflog --format=%h --grep-reflog='commit: Close on Mondays' | head -1)"
git log --oneline -2 feature-hours
```

```text
fc584d2 HEAD@{1}: commit: Close on Mondays
fc584d2 (feature-hours) Close on Mondays
9f7b5af Add opening hours
```

**Way 2: another clone.** Grace had fetched the branch before it was deleted; her `origin/feature-hours` still has it,
and she can push it back:

<!-- test: contains=[new branch]; output -->
```bash
cd ../grace && git fetch -q origin feature-hours 2> /dev/null || true
cd ../ada && git push origin feature-hours 2>&1
```

```text
To ~/git-practice/lesson-79/server/cafe.git
 * [new branch]      feature-hours -> feature-hours
```

## Command breakdown

| Situation | Recovery |
|---|---|
| you had the branch checked out | `git reflog` → `git branch NAME SHA` |
| it was pushed / a teammate has it | `git branch NAME origin/NAME` in their clone, push it back |
| a PR existed on GitHub | "Restore branch" button on the closed PR, or `git fetch origin pull/N/head:NAME` |
| none of the above | `git fsck --unreachable --no-reflogs` → inspect → `git branch NAME SHA` |

## Hands-on exercise

**Instructions.** Show that the server has `feature-hours` again, with both commits.

**Expected result.** `refs/heads/feature-hours` in `git ls-remote`, two commits after `main`.

**Verification.**

<!-- test: contains=refs/heads/feature-hours -->
```bash
cd ~/git-practice/lesson-79/ada
git ls-remote --heads origin
git log --oneline main..feature-hours
```

## Break it

Grace reviewed a branch of Ada's that she **never checked out** (only fetched it). Then the branch is deleted
everywhere, and Grace prunes:

<!-- test: contains=[deleted]; output -->
```bash
cd ~/git-practice/lesson-79/ada
git switch -q -c review-me && echo "seasonal: pumpkin" > seasonal.txt && git add seasonal.txt && git commit -q -m "Add the seasonal menu" && git push -q -u origin review-me
git switch -q main && git branch -q -D review-me
cd ../grace && git fetch -q && git log --oneline -1 origin/review-me
cd ../ada && git push -q origin --delete review-me
cd ../grace && git fetch --prune 2>&1
git reflog | grep -c "seasonal" || true
```

```text
2f48634 (origin/review-me) Add the seasonal menu
From ~/git-practice/lesson-79/server/cafe
 - [deleted]         (none)     -> origin/review-me
0
```

## Troubleshoot

Grace's reflog has no entry: her `HEAD` was never on that branch, and the reflog of `origin/review-me` was deleted
with the reference. The commit is still in her object store, though, unreferenced. `git fsck` finds such commits:

<!-- test: contains=Add the seasonal menu; output -->
```bash
for c in $(git fsck --unreachable --no-reflogs 2> /dev/null | awk '$2 == "commit" {print $3}'); do
  git log -1 --format='%h %s' "$c"
done
```

```text
2f48634 Add the seasonal menu
```

## Fix

<!-- test: contains=Add the seasonal menu; output -->
```bash
lost=$(for c in $(git fsck --unreachable --no-reflogs 2> /dev/null | awk '$2 == "commit" {print $3}'); do
  git log -1 --format='%H %s' "$c"; done | awk '/Add the seasonal menu/ {print $1}')
git branch review-me "$lost"
git push -q -u origin review-me
git log --oneline -1 review-me
```

```text
2f48634 (origin/review-me, review-me) Add the seasonal menu
```

## Real-world example

A teammate deletes `release/2.3` on GitHub by mistake. Recovery, fastest first: GitHub shows "Restore branch" on the
last PR of that branch; anyone with a recent clone has `origin/release/2.3` and can `git push origin
origin/release/2.3:refs/heads/release/2.3`; your own reflog if you worked on it. Branch protection (lesson 59) can
forbid deleting important branches in the first place.

## Practice challenge

Protect yourself: make Git keep unreachable objects for 90 days in this clone, and show the setting.

<details>
<summary>Solution</summary>

<!-- test: contains=90.days.ago; output -->
```bash
cd ~/git-practice/lesson-79/grace
git config gc.pruneExpire 90.days.ago
git config gc.reflogExpireUnreachable 90.days.ago
git config --get gc.pruneExpire
```

```text
90.days.ago
```

The defaults are 2 weeks (`gc.pruneExpire`) and 30 days (`gc.reflogExpireUnreachable`).

</details>

## Recap

- A deleted branch is a deleted pointer; the commits stay until garbage collection.
- Reflog (if you were on it) → another clone or the PR → `git fsck --unreachable` as a last resort.
- `git branch NAME SHA` recreates it; push it back if it lived on the server.

## Cleanup

<!-- test -->
```bash
cd ~ && rm -rf ~/git-practice/lesson-79
```

Next: [Lesson 80 · Recover a deleted commit](../80-recover-deleted-commit/README.md).
