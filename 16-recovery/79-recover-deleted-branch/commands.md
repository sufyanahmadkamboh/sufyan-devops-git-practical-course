<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 79 · Recover a deleted branch · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-79 remote
cd ~/git-practice/lesson-79/ada
```

## Demonstration

```bash
git switch -q -c feature-hours
echo "Open 8-18" > hours.txt && git add hours.txt && git commit -q -m "Add opening hours"
echo "Closed on Mondays" >> hours.txt && git commit -q -am "Close on Mondays"
git push -q -u origin feature-hours
git switch -q main
git branch -D feature-hours
git push -q origin --delete feature-hours
```

```bash
git reflog | grep -m1 "Close on Mondays"
git branch feature-hours "$(git reflog --format=%h --grep-reflog='commit: Close on Mondays' | head -1)"
git log --oneline -2 feature-hours
```

```bash
cd ../grace && git fetch -q origin feature-hours 2> /dev/null || true
cd ../ada && git push origin feature-hours 2>&1
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-79/ada
git ls-remote --heads origin
git log --oneline main..feature-hours
```

## Break it

```bash
cd ~/git-practice/lesson-79/ada
git switch -q -c review-me && echo "seasonal: pumpkin" > seasonal.txt && git add seasonal.txt && git commit -q -m "Add the seasonal menu" && git push -q -u origin review-me
git switch -q main && git branch -q -D review-me
cd ../grace && git fetch -q && git log --oneline -1 origin/review-me
cd ../ada && git push -q origin --delete review-me
cd ../grace && git fetch --prune 2>&1
git reflog | grep -c "seasonal" || true
```

## Troubleshoot

```bash
for c in $(git fsck --unreachable --no-reflogs 2> /dev/null | awk '$2 == "commit" {print $3}'); do
  git log -1 --format='%h %s' "$c"
done
```

## Fix

```bash
lost=$(for c in $(git fsck --unreachable --no-reflogs 2> /dev/null | awk '$2 == "commit" {print $3}'); do
  git log -1 --format='%H %s' "$c"; done | awk '/Add the seasonal menu/ {print $1}')
git branch review-me "$lost"
git push -q -u origin review-me
git log --oneline -1 review-me
```

## Practice challenge

```bash
cd ~/git-practice/lesson-79/grace
git config gc.pruneExpire 90.days.ago
git config gc.reflogExpireUnreachable 90.days.ago
git config --get gc.pruneExpire
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-79
```
