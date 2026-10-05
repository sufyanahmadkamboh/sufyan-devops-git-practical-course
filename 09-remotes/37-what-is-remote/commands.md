<!-- generated from README.md by tools/lesson_files.py: edit README.md, not this file -->
# Lesson 37 · What is a remote? · commands

> Every command of the lesson, in order. The explanations: [README.md](README.md)

## Lab setup

```bash
bash scripts/new-lab.sh lesson-37 remote
cd ~/git-practice/lesson-37
ls
```

## Demonstration

```bash
cd ada
git remote -v
```

```bash
git branch -a
git log --oneline --graph --all
```

## Hands-on exercise

```bash
cd ~/git-practice/lesson-37/grace
git remote show origin
```

## Break it

```bash
echo "Open 8-18" >> README.md && git commit -q -am "Add opening hours" && git push -q
cd ../ada
git log --oneline -1 origin/main
```

## Fix

```bash
git fetch
git log --oneline -1 origin/main
```

## Practice challenge

```bash
cd ~/git-practice/lesson-37/ada
git ls-remote origin main
git rev-parse origin/main
```

## Cleanup

```bash
cd ~ && rm -rf ~/git-practice/lesson-37
```
