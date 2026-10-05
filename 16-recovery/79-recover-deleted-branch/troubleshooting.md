<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 79 · Recover a deleted branch · troubleshooting

> The full lesson: [README.md](README.md)

## Break it

Grace reviewed a branch of Ada's that she **never checked out** (only fetched it). Then the branch is deleted
everywhere, and Grace prunes:

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

```bash
for c in $(git fsck --unreachable --no-reflogs 2> /dev/null | awk '$2 == "commit" {print $3}'); do
  git log -1 --format='%h %s' "$c"
done
```

```text
2f48634 Add the seasonal menu
```

## Fix

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
