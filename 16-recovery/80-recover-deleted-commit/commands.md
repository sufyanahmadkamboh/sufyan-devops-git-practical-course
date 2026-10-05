<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 80 · Recover a deleted commit · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-80 history
cd ~/git-practice/lesson-80
git init -q --bare ../lesson-80-server.git && git remote add origin ../lesson-80-server.git
git log --oneline -4
```

## Demonstration

```bash
GIT_SEQUENCE_EDITOR="sed -i '/Add mocha/s/^pick/drop/'" git rebase -q -i HEAD~3
git log --oneline -4
grep mocha menu.txt || echo "mocha has a price but is not on the menu!"
```

```bash
git reflog | grep "Add mocha"
```

```bash
dropped=$(git reflog --format=%h --grep-reflog="commit: Add mocha" | head -1)
git cherry-pick "$dropped" > /dev/null
git log --oneline -3
grep mocha menu.txt
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-80
git reflog -2
git log -1 --format=%s 'HEAD@{1}'
```

## Break it

```bash
git push -q -u origin main
git reset -q --hard HEAD~1
git reflog expire --expire=now --all
git gc -q --prune=now
git reflog | wc -l
```

## Troubleshoot

```bash
git fsck --unreachable --no-reflogs 2> /dev/null | wc -l
git log --oneline main | grep -c chai || true
```

```bash
git log --oneline -1 origin/main
```

## Fix

```bash
git reset -q --hard origin/main
git log --oneline -2
grep chai prices.txt
```

## Practice challenge

```bash
cd ~/git-practice/lesson-80
git reflog --date=relative | tail -1 | sed -E 's/\{[0-9]+ (seconds?|minutes?) ago\}/{N seconds ago}/'
git config --get gc.reflogExpire || echo "gc.reflogExpire not set: default 90 days"
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-80 ~/git-practice/lesson-80-server.git
```
