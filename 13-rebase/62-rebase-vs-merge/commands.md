<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 62 · Rebase vs merge · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-62 diverged
cd ~/git-practice/lesson-62
git switch -q feature-tea && echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea" && git switch -q main
git branch merge-way main && git branch rebase-way feature-tea
```

## Demonstration

```bash
git switch -q merge-way && git merge -q --no-edit feature-tea
git log --oneline --graph merge-way
```

```bash
git switch -q rebase-way && git rebase -q main
git log --oneline --graph rebase-way
```

```bash
git diff --quiet merge-way rebase-way && echo "identical files"
echo "merge-way: $(git rev-list --count merge-way) commits, rebase-way: $(git rev-list --count rebase-way) commits"
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-62
for b in merge-way rebase-way; do echo "$b: $(git rev-list --merges --count "$b")"; done
```

## Break it

```bash
git init -q --bare ../lesson-62-server.git && git remote add origin ../lesson-62-server.git
git push -q origin main feature-tea
git clone -q -b feature-tea ../lesson-62-server.git ../lesson-62-grace
(cd ../lesson-62-grace && git config user.name "Grace Hopper" && git config user.email grace@example.com &&
  echo "green tea is popular" > notes.txt && git add notes.txt && git commit -q -m "Add notes")
git switch -q feature-tea && git rebase -q main && git push -q --force-with-lease origin feature-tea
cd ../lesson-62-grace && git pull -q --no-rebase --no-edit
git log --oneline --graph | head -12
```

## Troubleshoot

```bash
git log --oneline | grep -c "Price green tea"
```

## Fix

```bash
git reset -q --hard ORIG_HEAD
git rebase origin/feature-tea 2>&1 | grep -v "^hint:" || true
git log --oneline | grep -c "Price green tea"
git log --oneline --graph | head -5
```

## Practice challenge

```bash
cd ~/git-practice/lesson-62-grace
git fetch -q
git log --oneline --cherry-mark --left-right origin/main...HEAD
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-62 ~/git-practice/lesson-62-server.git ~/git-practice/lesson-62-grace
```
