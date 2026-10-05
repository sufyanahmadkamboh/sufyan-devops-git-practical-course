<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 21 · Branch visualization · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-21 basic
cd ~/git-practice/lesson-21
```

## Demonstration

```bash
git branch feature
git log --oneline --graph --all
```

```bash
git switch -q feature
echo "green tea" >> menu.txt && git commit -q -am "Add green tea"
git log --oneline --graph --all
```

```bash
git switch -q main
echo "Open 8-18" > hours.txt && git add hours.txt && git commit -q -m "Add hours"
git log --oneline --graph --all
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-21
git merge-base main feature | cut -c1-7
```

## Break it

```bash
echo "chai: black tea, spices, milk" > chai.txt && git add chai.txt && git commit -q -m "Add chai"
git log --oneline --graph --all | head -4
```

## Fix

```bash
git switch -q feature
git cherry-pick main > /dev/null
git switch -q main
git reset -q --hard HEAD~1
git log --oneline --graph --all
```

## Practice challenge

```bash
cd ~/git-practice/lesson-21
git switch -q -c experiment feature
echo "oat milk" >> menu.txt && git commit -q -am "Try oat milk"
git log --oneline --graph --all
```

## Cleanup

```bash
rm -rf ~/git-practice/lesson-21
```
