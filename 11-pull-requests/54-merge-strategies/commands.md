<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 54 · Merge strategies · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-54-gh github
```

```bash
bash scripts/new-lab.sh lesson-54 diverged
cd ~/git-practice/lesson-54
git switch -q feature-tea
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git switch -q main
for s in merge squash rebase; do git branch "main-$s" main; git branch "pr-$s" feature-tea; done
git log --oneline --graph --all | head -8
```

## Demonstration

```bash
git switch -q main-merge
git merge -q --no-ff -m "Merge pull request #1 from pr-merge" pr-merge
git log --oneline --graph -5
```

```bash
git switch -q main-squash
git merge -q --squash pr-squash
git commit -q -m "Green tea (#2)"
git log --oneline --graph -3
git show --stat --format=%s HEAD
```

```bash
git switch -q pr-rebase
git rebase -q main-rebase
git switch -q main-rebase
git merge -q --ff-only pr-rebase
git log --oneline --graph -4
```

```bash
for s in merge squash rebase; do echo "$s: $(git rev-parse "main-$s^{tree}" | cut -c1-7)  $(git rev-list --count "main-$s") commits"; done
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-54
git log --oneline main-squash..pr-squash
```

## Break it

```bash
git switch -q main-squash
git branch -d pr-squash 2>&1
```

## Troubleshoot

```bash
git diff --quiet main-squash pr-squash -- menu.txt prices.txt && echo "identical content: the work is on main-squash"
```

## Fix

```bash
git branch -D pr-squash
```

## Practice challenge

```bash
cd ~/git-practice/lesson-54-gh
git push -q origin --delete chai 2> /dev/null || true
git switch -q -c chai
echo "chai" >> menu.txt && git commit -q -am "Add chai"
echo "chai 3.10" >> prices.txt && git commit -q -am "Price chai"
git push -q -u origin chai 2> /dev/null
gh pr create --base main --title "Add chai" --body "Chai on the menu, with its price." > /dev/null
gh pr merge chai --squash --delete-branch > /dev/null 2>&1
git switch -q main && git pull -q
git log --oneline -1
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-54 ~/git-practice/lesson-54-gh
```
