<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 61 · Basic rebase · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-61 diverged
cd ~/git-practice/lesson-61
git switch -q feature-tea
echo "green tea 2.80" >> prices.txt && git commit -q -am "Price green tea"
git log --oneline --graph --all
```

## Demonstration

```bash
git rebase main
git log --oneline --graph --all
```

```bash
git switch -q main && git merge --ff-only feature-tea
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-61
git rev-list --count feature-chai..main
git log --oneline -2 feature-chai
```

## Break it

```bash
git switch -q main && git switch -q -c feature-mocha HEAD~3
echo "mocha" > specials.txt && git add specials.txt && git commit -q -m "Add mocha special"
sed -i 's/espresso 2.50/espresso 2.55/' prices.txt
git rebase main 2>&1
```

## Fix

```bash
git rebase --autostash main 2>&1 | grep -v "^hint:" || true
git status --short
```

## Practice challenge

```bash
cd ~/git-practice/lesson-61
git stash -q && git switch -q main
git rebase main feature-mocha
git branch --show-current
git log --oneline main..feature-mocha
git stash pop -q
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-61
```
