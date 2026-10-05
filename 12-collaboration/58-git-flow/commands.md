<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 58 · Git Flow · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-58 basic
cd ~/git-practice/lesson-58
git tag -a v1.0.0 -m "Release 1.0.0" && git switch -q -c develop
git log --oneline --decorate --all
```

## Demonstration

```bash
git switch -q -c feature/green-tea develop
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git switch -q develop && git merge -q --no-ff --no-edit feature/green-tea && git branch -d -q feature/green-tea
git log --oneline -1
```

```bash
git switch -q -c release/1.1.0 develop
echo "1.1.0" > VERSION && git add VERSION && git commit -q -m "Bump version to 1.1.0"
git switch -q main && git merge -q --no-ff --no-edit release/1.1.0 && git tag -a v1.1.0 -m "Release 1.1.0"
git switch -q develop && git merge -q --no-ff --no-edit release/1.1.0 && git branch -d -q release/1.1.0
git log --oneline --graph --all | head -12
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-58
git tag -n --format='%(refname:short) %(*objectname:short) %(contents:subject)'
```

## Break it

```bash
git switch -q -c hotfix/1.1.1 main
sed -i 's/latte 3.20/latte 3.30/' prices.txt && git commit -q -am "Fix the latte price"
git switch -q main && git merge -q --no-ff --no-edit hotfix/1.1.1 && git tag -a v1.1.1 -m "Release 1.1.1"
git switch -q develop && grep latte prices.txt
```

## Troubleshoot

```bash
git log --oneline develop..main
```

## Fix

```bash
git merge -q --no-ff --no-edit hotfix/1.1.1 && git branch -d -q hotfix/1.1.1
grep latte prices.txt
git log --oneline develop..main | wc -l
```

## Practice challenge

```bash
cd ~/git-practice/lesson-58
git switch -q -c feature/mocha develop && echo mocha >> menu.txt && git commit -q -am "Add mocha"
git switch -q develop && git merge -q --no-ff --no-edit feature/mocha
git log --oneline --no-merges main..develop
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-58
```
